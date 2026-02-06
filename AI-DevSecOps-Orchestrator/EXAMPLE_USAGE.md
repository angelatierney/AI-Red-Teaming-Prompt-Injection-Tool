# Example Usage

## Basic Scan

```bash
# Scan a C file for vulnerabilities
python src/agent.py legacy_code/circular_queue.c --provider openai
```

## Generate Refactored Code

```bash
# Scan and generate refactored secure version
python src/agent.py legacy_code/circular_queue.c --refactor --output output/
```

## Using Different Providers

```bash
# Use OpenAI
python src/agent.py legacy_code/circular_queue.c --provider openai

# Use Anthropic Claude
python src/agent.py legacy_code/circular_queue.c --provider anthropic
```

## Custom Output Directory

```bash
python src/agent.py legacy_code/circular_queue.c --output my_results/
```

## Expected Output Structure

After running the agent, you'll get:

```
output/
├── vulnerabilities.json    # JSON list of all vulnerabilities
├── Dockerfile              # Hardened Dockerfile
├── RISK_NOTE.md            # Comprehensive risk assessment
└── refactored_code.c       # Secure refactored version (if --refactor used)
```

## Example Output Files

### vulnerabilities.json
```json
{
  "vulnerabilities": [
    {
      "type": "buffer_overflow",
      "severity": "high",
      "line": 50,
      "description": "strcpy() used without bounds checking. CWE-120.",
      "cwe": "CWE-120"
    },
    {
      "type": "memory_leak",
      "severity": "medium",
      "line": 80,
      "description": "Queue allocated but never freed",
      "cwe": "CWE-401"
    }
  ]
}
```

### RISK_NOTE.md
The risk note includes:
- Executive summary
- Detailed threat analysis
- CVSS scores (if applicable)
- Mitigation steps
- NIST/OWASP compliance notes

## Integration with CI/CD

The GitHub Action automatically:
1. Scans changed C files on PR
2. Posts results as PR comment
3. Uploads artifacts for download

No manual intervention needed!
