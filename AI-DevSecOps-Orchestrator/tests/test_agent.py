"""
Unit tests for the AI-DevSecOps-Orchestrator agent.
Ensures 100% reliability for high-uptime environments.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent import SecurityAgent, LLMProvider, SecurityScanResult


class TestLLMProvider:
    """Test LLM provider with mocked API calls."""
    
    @pytest.fixture
    def mock_openai_client(self):
        """Mock OpenAI client."""
        with patch('agent.OpenAI') as mock:
            client_instance = MagicMock()
            mock.return_value = client_instance
            
            # Mock response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = '{"vulnerabilities": [], "summary": "Test"}'
            client_instance.chat.completions.create.return_value = mock_response
            
            yield client_instance
    
    @pytest.fixture
    def provider(self, mock_openai_client):
        """Create LLM provider with mocked client."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            return LLMProvider(provider="openai", api_key="test-key")
    
    def test_provider_initialization(self, provider):
        """Test provider initializes correctly."""
        assert provider.provider == "openai"
        assert provider.api_key == "test-key"
    
    def test_scan_code_valid_json(self, provider, mock_openai_client):
        """Test code scanning returns valid JSON."""
        test_code = "int main() { return 0; }"
        result = provider.scan_code(test_code)
        
        assert isinstance(result, dict)
        assert "vulnerabilities" in result
        assert "summary" in result
    
    def test_scan_code_handles_invalid_json(self, provider, mock_openai_client):
        """Test code scanning handles invalid JSON gracefully."""
        # Mock invalid JSON response
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Invalid JSON response"
        
        test_code = "int main() { return 0; }"
        result = provider.scan_code(test_code)
        
        # Should return default structure on error
        assert isinstance(result, dict)
        assert "vulnerabilities" in result
    
    def test_generate_dockerfile(self, provider, mock_openai_client):
        """Test Dockerfile generation."""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "FROM alpine:latest"
        
        dockerfile = provider.generate_dockerfile("test.c", [])
        assert isinstance(dockerfile, str)
        assert len(dockerfile) > 0
    
    def test_generate_dockerfile_fallback(self, provider, mock_openai_client):
        """Test Dockerfile fallback on API failure."""
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
        
        dockerfile = provider.generate_dockerfile("test.c", [])
        assert isinstance(dockerfile, str)
        assert "FROM" in dockerfile  # Should have fallback content
    
    def test_generate_risk_note(self, provider, mock_openai_client):
        """Test risk note generation."""
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "# Risk Note\nTest content"
        
        vulnerabilities = [
            {"type": "buffer_overflow", "severity": "high", "line": 10, "description": "Test"}
        ]
        risk_note = provider.generate_risk_note(vulnerabilities, "test.c")
        
        assert isinstance(risk_note, str)
        assert len(risk_note) > 0
    
    def test_api_retry_logic(self, provider, mock_openai_client):
        """Test exponential backoff retry logic."""
        # First two calls fail, third succeeds
        mock_openai_client.chat.completions.create.side_effect = [
            Exception("Network error"),
            Exception("Timeout"),
            MagicMock(choices=[MagicMock(message=MagicMock(content='{"vulnerabilities": []}'))])
        ]
        
        result = provider.scan_code("test code")
        assert isinstance(result, dict)
        assert mock_openai_client.chat.completions.create.call_count == 3


class TestSecurityAgent:
    """Test main security agent."""
    
    @pytest.fixture
    def agent(self):
        """Create security agent with mocked LLM."""
        with patch('agent.LLMProvider') as mock_provider_class:
            mock_provider = MagicMock()
            mock_provider.scan_code.return_value = {
                "vulnerabilities": [
                    {"type": "buffer_overflow", "severity": "high", "line": 10, "description": "Test vuln"}
                ],
                "summary": "Test summary"
            }
            mock_provider.generate_dockerfile.return_value = "FROM alpine:latest"
            mock_provider.generate_risk_note.return_value = "# Risk Note\nTest"
            mock_provider.suggest_refactoring.return_value = "int main() { return 0; }"
            mock_provider_class.return_value = mock_provider
            
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                yield SecurityAgent(provider="openai")
    
    def test_scan_file_success(self, agent):
        """Test successful file scan."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write("int main() { return 0; }")
            temp_path = f.name
        
        try:
            result = agent.scan_file(temp_path)
            
            assert isinstance(result, SecurityScanResult)
            assert len(result.vulnerabilities) > 0
            assert result.dockerfile is not None
            assert result.risk_note is not None
        finally:
            os.unlink(temp_path)
    
    def test_scan_file_not_found(self, agent):
        """Test file not found error handling."""
        with pytest.raises(FileNotFoundError):
            agent.scan_file("/nonexistent/file.c")
    
    def test_scan_file_with_refactoring(self, agent):
        """Test file scan with refactoring enabled."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write("int main() { return 0; }")
            temp_path = f.name
        
        try:
            result = agent.scan_file(temp_path, generate_refactored=True)
            assert result.refactored_code is not None
        finally:
            os.unlink(temp_path)
    
    def test_save_results(self, agent):
        """Test saving results to files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write("int main() { return 0; }")
            temp_path = f.name
        
        try:
            result = agent.scan_file(temp_path)
            
            with tempfile.TemporaryDirectory() as output_dir:
                agent.save_results(result, output_dir)
                
                # Check files were created
                assert (Path(output_dir) / "vulnerabilities.json").exists()
                assert (Path(output_dir) / "Dockerfile").exists()
                assert (Path(output_dir) / "RISK_NOTE.md").exists()
        finally:
            os.unlink(temp_path)


class TestErrorHandling:
    """Test error handling for high uptime."""
    
    def test_missing_api_key(self):
        """Test graceful handling of missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="API key not found"):
                LLMProvider(provider="openai")
    
    def test_unsupported_provider(self):
        """Test error for unsupported provider."""
        with patch.dict(os.environ, {'TEST_API_KEY': 'key'}):
            with pytest.raises(ValueError, match="Unsupported provider"):
                LLMProvider(provider="test")
    
    def test_network_failure_graceful(self):
        """Test graceful handling of network failures."""
        with patch('agent.OpenAI') as mock:
            client_instance = MagicMock()
            mock.return_value = client_instance
            client_instance.chat.completions.create.side_effect = Exception("Network error")
            
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                provider = LLMProvider(provider="openai", api_key="test-key")
                
                # Should raise after retries exhausted
                with pytest.raises(Exception):
                    provider.scan_code("test")


class TestIntegration:
    """Integration tests with real file structure."""
    
    def test_legacy_code_scan(self):
        """Test scanning the actual legacy code file."""
        legacy_file = Path(__file__).parent.parent / "legacy_code" / "circular_queue.c"
        
        if not legacy_file.exists():
            pytest.skip("Legacy code file not found")
        
        # Mock LLM to avoid API calls in tests
        with patch('agent.LLMProvider') as mock_provider_class:
            mock_provider = MagicMock()
            mock_provider.scan_code.return_value = {
                "vulnerabilities": [
                    {"type": "buffer_overflow", "severity": "high", "line": 50, "description": "strcpy usage"}
                ],
                "summary": "Multiple vulnerabilities found"
            }
            mock_provider.generate_dockerfile.return_value = "FROM alpine:latest\nUSER appuser"
            mock_provider.generate_risk_note.return_value = "# Risk Note\nBuffer overflow detected"
            mock_provider_class.return_value = mock_provider
            
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                agent = SecurityAgent(provider="openai")
                result = agent.scan_file(str(legacy_file))
                
                assert isinstance(result, SecurityScanResult)
                assert len(result.vulnerabilities) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
