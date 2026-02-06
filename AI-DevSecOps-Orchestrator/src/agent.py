#!/usr/bin/env python3
"""
AI-DevSecOps-Orchestrator Agent
Uses LLM to scan C code for security vulnerabilities, generate Dockerfiles, and create risk notes.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import time

# LLM API imports
try:
    import openai
    from openai import OpenAI
except ImportError:
    openai = None
    OpenAI = None

try:
    import anthropic
    from anthropic import Anthropic
except ImportError:
    anthropic = None
    Anthropic = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SecurityScanResult:
    """Container for security scan results."""
    vulnerabilities: list
    dockerfile: str
    risk_note: str
    refactored_code: Optional[str] = None


class LLMProvider:
    """Abstract interface for LLM providers."""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        
        if not self.api_key:
            raise ValueError(f"API key not found. Set {provider.upper()}_API_KEY environment variable.")
        
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the LLM client based on provider."""
        if self.provider == "openai":
            if not openai:
                raise ImportError("openai package not installed. Run: pip install openai")
            self._client = OpenAI(api_key=self.api_key)
        elif self.provider == "anthropic":
            if not anthropic:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            self._client = Anthropic(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_llm(self, prompt: str, model: str = None, max_retries: int = 3) -> str:
        """Make LLM API call with retry logic for high uptime."""
        if self.provider == "openai":
            model = model or "gpt-4-turbo-preview"
            for attempt in range(max_retries):
                try:
                    response = self._client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    logger.warning(f"LLM API call failed (attempt {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise
        elif self.provider == "anthropic":
            model = model or "claude-3-opus-20240229"
            for attempt in range(max_retries):
                try:
                    response = self._client.messages.create(
                        model=model,
                        max_tokens=4096,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return response.content[0].text
                except Exception as e:
                    logger.warning(f"LLM API call failed (attempt {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                    else:
                        raise
        return ""
    
    def scan_code(self, code: str) -> Dict:
        """Scan C code for security vulnerabilities."""
        prompt = f"""You are a security expert analyzing C code for vulnerabilities. Analyze the following C code and identify:
1. Buffer overflows (stack/heap)
2. Memory leaks
3. Use-after-free vulnerabilities
4. Integer overflows
5. Format string vulnerabilities
6. Race conditions
7. Missing input validation

Return a JSON object with this structure:
{{
    "vulnerabilities": [
        {{
            "type": "buffer_overflow",
            "severity": "high|medium|low",
            "line": <line_number>,
            "description": "<detailed description>",
            "cwe": "<CWE number if applicable>"
        }}
    ],
    "summary": "<overall security assessment>"
}}

Code to analyze:
```c
{code}
```

Return ONLY valid JSON, no markdown formatting."""
        
        try:
            response = self._call_llm(prompt)
            # Clean response (remove markdown code blocks if present)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Response was: {response[:500]}")
            return {"vulnerabilities": [], "summary": "Error parsing LLM response"}
        except Exception as e:
            logger.error(f"Error during code scan: {e}")
            return {"vulnerabilities": [], "summary": f"Error: {str(e)}"}
    
    def generate_dockerfile(self, code_path: str, vulnerabilities: list) -> str:
        """Generate a hardened, non-root Dockerfile."""
        vuln_summary = "\n".join([f"- {v.get('type', 'unknown')}: {v.get('description', '')}" for v in vulnerabilities[:5]])
        
        prompt = f"""Generate a secure, production-ready Dockerfile for a C application with the following considerations:

1. Use a non-root user (create a dedicated user)
2. Use minimal base image (Alpine or distroless)
3. Enable security features (no-new-privileges, read-only filesystem where possible)
4. Set appropriate resource limits
5. Use multi-stage build to minimize image size
6. Address these known vulnerabilities in the build process:
{vuln_summary}

The source code is located at: {code_path}

Return ONLY the Dockerfile content, no explanations or markdown formatting."""
        
        try:
            response = self._call_llm(prompt)
            # Clean response
            response = response.strip()
            if response.startswith("```dockerfile"):
                response = response[13:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating Dockerfile: {e}")
            return self._default_dockerfile(code_path)
    
    def generate_risk_note(self, vulnerabilities: list, code_path: str) -> str:
        """Generate a Markdown risk note summarizing threats and mitigations."""
        high_severity = [v for v in vulnerabilities if v.get('severity') == 'high']
        medium_severity = [v for v in vulnerabilities if v.get('severity') == 'medium']
        low_severity = [v for v in vulnerabilities if v.get('severity') == 'low']
        
        prompt = f"""Generate a comprehensive security risk note in Markdown format for the following vulnerabilities found in {code_path}:

High Severity ({len(high_severity)}):
{json.dumps(high_severity, indent=2)}

Medium Severity ({len(medium_severity)}):
{json.dumps(medium_severity, indent=2)}

Low Severity ({len(low_severity)}):
{json.dumps(low_severity, indent=2)}

The risk note should include:
1. Executive Summary
2. Threat Analysis
3. Risk Assessment (CVSS scores if applicable)
4. Mitigation Steps
5. Remediation Priority
6. Compliance Considerations (NIST, OWASP)

Format as professional Markdown suitable for security teams and compliance officers."""
        
        try:
            return self._call_llm(prompt)
        except Exception as e:
            logger.error(f"Error generating risk note: {e}")
            return self._default_risk_note(vulnerabilities, code_path)
    
    def suggest_refactoring(self, code: str, vulnerabilities: list) -> str:
        """Generate refactored code with security fixes."""
        vuln_details = json.dumps(vulnerabilities, indent=2)
        
        prompt = f"""Refactor the following C code to fix all identified security vulnerabilities. Apply best practices:
1. Use safe string functions (strncpy, snprintf instead of strcpy, sprintf)
2. Add bounds checking
3. Proper memory management
4. Input validation
5. Error handling

Vulnerabilities to fix:
{vuln_details}

Original code:
```c
{code}
```

Return the refactored code with comments explaining the security fixes. Return ONLY the code block, no additional explanation."""
        
        try:
            response = self._call_llm(prompt)
            # Extract code block
            if "```c" in response:
                start = response.find("```c") + 4
                end = response.find("```", start)
                return response[start:end].strip()
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                return response[start:end].strip()
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating refactored code: {e}")
            return code  # Return original if refactoring fails
    
    def _default_dockerfile(self, code_path: str) -> str:
        """Fallback Dockerfile if LLM generation fails."""
        return f"""# Multi-stage build for security and size optimization
FROM gcc:latest AS builder

WORKDIR /build
COPY {code_path} .
RUN gcc -Wall -Wextra -Werror -O2 -static -o app *.c

# Production stage with non-root user
FROM alpine:latest

RUN addgroup -g 1000 appuser && \\
    adduser -D -u 1000 -G appuser appuser

WORKDIR /app
COPY --from=builder /build/app .

# Security hardening
RUN chmod 755 /app/app && \\
    chown appuser:appuser /app/app

USER appuser

# Disable privilege escalation
RUN --security=no-new-privileges

ENTRYPOINT ["/app/app"]
"""
    
    def _default_risk_note(self, vulnerabilities: list, code_path: str) -> str:
        """Fallback risk note if LLM generation fails."""
        return f"""# Security Risk Note: {code_path}

## Executive Summary
{len(vulnerabilities)} security vulnerabilities identified in the codebase.

## Vulnerabilities
{json.dumps(vulnerabilities, indent=2)}

## Recommended Actions
1. Review all high-severity vulnerabilities immediately
2. Implement secure coding practices
3. Add automated security scanning to CI/CD pipeline
4. Conduct security code review
"""


class SecurityAgent:
    """Main security agent orchestrator."""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.llm = LLMProvider(provider, api_key)
        logger.info(f"Initialized SecurityAgent with {provider} provider")
    
    def scan_file(self, file_path: str, generate_refactored: bool = False) -> SecurityScanResult:
        """Scan a C file and generate security artifacts."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        logger.info(f"Scanning file: {file_path}")
        
        # Read source code
        with open(file_path, 'r') as f:
            code = f.read()
        
        # Scan for vulnerabilities
        scan_result = self.llm.scan_code(code)
        vulnerabilities = scan_result.get('vulnerabilities', [])
        
        logger.info(f"Found {len(vulnerabilities)} vulnerabilities")
        
        # Generate Dockerfile
        dockerfile = self.llm.generate_dockerfile(str(file_path), vulnerabilities)
        
        # Generate risk note
        risk_note = self.llm.generate_risk_note(vulnerabilities, str(file_path))
        
        # Optionally generate refactored code
        refactored_code = None
        if generate_refactored:
            refactored_code = self.llm.suggest_refactoring(code, vulnerabilities)
        
        return SecurityScanResult(
            vulnerabilities=vulnerabilities,
            dockerfile=dockerfile,
            risk_note=risk_note,
            refactored_code=refactored_code
        )
    
    def save_results(self, result: SecurityScanResult, output_dir: str = "output"):
        """Save scan results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save vulnerabilities as JSON
        with open(output_path / "vulnerabilities.json", 'w') as f:
            json.dump(result.vulnerabilities, f, indent=2)
        
        # Save Dockerfile
        with open(output_path / "Dockerfile", 'w') as f:
            f.write(result.dockerfile)
        
        # Save risk note
        with open(output_path / "RISK_NOTE.md", 'w') as f:
            f.write(result.risk_note)
        
        # Save refactored code if available
        if result.refactored_code:
            with open(output_path / "refactored_code.c", 'w') as f:
                f.write(result.refactored_code)
        
        logger.info(f"Results saved to {output_path}")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI-DevSecOps Security Agent")
    parser.add_argument("file", help="Path to C file to scan")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai",
                       help="LLM provider to use")
    parser.add_argument("--api-key", help="API key (overrides environment variable)")
    parser.add_argument("--output", default="output", help="Output directory for results")
    parser.add_argument("--refactor", action="store_true", help="Generate refactored code")
    
    args = parser.parse_args()
    
    try:
        agent = SecurityAgent(provider=args.provider, api_key=args.api_key)
        result = agent.scan_file(args.file, generate_refactored=args.refactor)
        agent.save_results(result, args.output)
        
        print(f"\n✓ Scan complete!")
        print(f"  - Vulnerabilities found: {len(result.vulnerabilities)}")
        print(f"  - Results saved to: {args.output}/")
        
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
