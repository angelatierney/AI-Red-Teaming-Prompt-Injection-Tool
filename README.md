# Python-Automation-and-Analysis-Toolkit

This repository contains a collection of small Python scripts designed to automate everyday tasks and analyze system or data files. The goal of this toolkit is to demonstrate scripting, data handling, and logic building.

### 🔹 File Renamer
Automatically renames or organizes files by extension, date, or keyword patterns. Useful for managing large collections of evidence files, images, or reports.

### 🔹 Log Analyzer
Parses system or network log files to identify patterns, suspicious activity, or common error types. Includes text searching, filtering, and summary output.

### 🔹 Hash Checker
Generates and verifies **MD5** or **SHA256** hashes to check file integrity or detect duplicates.

### 🔹 CSV Analyzer *(optional)*
Reads .csv data (like exported reports or metadata) and summarizes trends or anomalies.

---

## 🛡️ AI Red Teaming & Prompt Injection Tool (PoC)

### Overview
An automated red teaming script designed to test LLM endpoints for prompt injection vulnerabilities. Built for deployment on Raspberry Pi as a portable AI pentesting device. References **OWASP LLM01: Prompt Injection**.

### Features
- **12+ Attack Templates**: Includes DAN variants, Base64 encoding, payload splitting, ASCII art, dialogue injection, and more
- **Success Evaluation**: Regex-based detection with optional secondary LLM evaluation
- **CSV Logging**: Wireshark-style data capture for post-analysis
- **Stealth Mode**: Randomized timing to avoid rate limiting and basic WAF detection
- **Raspberry Pi Optimized**: Headless operation, ARM64 compatible, systemd integration

### Installation

#### 1. Prerequisites
```bash
# On Raspberry Pi OS (64-bit)
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

#### 2. Setup Virtual Environment (Recommended)
```bash
# Using uv (faster, modern)
curl -LsSf https://astral.sh/uv/install.sh | sh
cd Python-Automation-and-Analysis-Toolkit
uv venv
source .venv/bin/activate

# Or using pip
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
# Using uv
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

#### 4. Make Script Executable
```bash
chmod +x pi-redteam.py
```

### Usage

#### Basic Usage
```bash
python3 pi-redteam.py \
  --target-url https://api.openai.com/v1/chat/completions \
  --api-key sk-your-api-key-here
```

#### With Stealth Mode
```bash
python3 pi-redteam.py \
  --target-url https://api.example.com/v1/chat \
  --api-key your-api-key \
  --stealth \
  --output results.csv
```

#### Command-Line Arguments
- `--target-url` (required): Target LLM API endpoint URL
- `--api-key` (required): API key for authentication
- `--stealth`: Enable randomized delays (2-8 seconds) to avoid detection
- `--output`: Output CSV file path (default: `redteam_results.csv`)

### Attack Library

The tool includes 12+ attack templates in `attacks.json`:

1. **DAN (Do Anything Now) - Classic**: Role-play jailbreak
2. **DAN 5.2 - White Paper Pretext**: Academic research pretext
3. **Base64 Encoded Instruction**: Encoding-based bypass
4. **Payload Splitting Attack**: Fragmentation technique
5. **ASCII Art Bypass**: Visual encoding attack
6. **Dialogue Injection Attack (DIA)**: Context manipulation
7. **Embedded Jailbreak Template**: Semantic rewriting
8. **Unicode Tag Smuggling**: Hidden instruction injection
9. **Refusal Quelling Technique**: Persuasion-based bypass
10. **Hypothetical Scenario Bypass**: Context manipulation
11. **System Prompt Extraction**: Information disclosure
12. **Multi-Layered Injection**: Fragmented attack

### Results Analysis

Results are saved to CSV with the following columns:
- `timestamp`: ISO format timestamp
- `attack_id`: Unique attack identifier
- `attack_name`: Human-readable attack name
- `category`: Attack category (role_play, encoding, fragmentation, etc.)
- `status`: VULNERABLE or DEFENDED
- `vulnerable`: Boolean flag
- `reason`: Evaluation reason
- `response_preview`: First 200 characters of response
- `response_length`: Full response length

Analyze results with pandas:
```python
import pandas as pd
df = pd.read_csv('redteam_results.csv')
vulnerable = df[df['vulnerable'] == True]
print(vulnerable[['attack_name', 'reason']])
```

### Systemd Service (Auto-Start)

#### 1. Edit Service File
```bash
nano redteam.service
# Update YOUR_TARGET_URL and YOUR_API_KEY
# Update WorkingDirectory and ExecStart paths if needed
```

#### 2. Install Service
```bash
sudo cp redteam.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable redteam.service
sudo systemctl start redteam.service
```

#### 3. Check Status
```bash
sudo systemctl status redteam.service
sudo journalctl -u redteam.service -f
```

#### 4. Stop/Disable
```bash
sudo systemctl stop redteam.service
sudo systemctl disable redteam.service
```

### Security Considerations

⚠️ **Ethical Use Only**: This tool is for authorized security testing only. Unauthorized use against systems you don't own or have explicit permission to test is illegal.

- Only test endpoints you own or have written authorization to test
- Respect rate limits and API terms of service
- Use stealth mode responsibly to avoid overwhelming target systems
- Review and comply with local cybersecurity laws

### API Compatibility

The tool is designed for OpenAI-compatible APIs. For other API formats, modify the `_send_payload()` method in `pi-redteam.py`:

```python
# Adjust data structure in _send_payload() based on your API:
data = {
    "model": "your-model-name",
    "messages": [{"role": "user", "content": payload}],
    # ... other API-specific parameters
}
```

### Future Integrations

The tool is prepared for integration with:
- **garak** (NVIDIA's vulnerability scanner): Uncomment in `requirements.txt`
- **PyRIT** (Microsoft's red teaming toolkit): Uncomment in `requirements.txt`

### Troubleshooting

#### "attacks.json not found"
- Ensure `attacks.json` is in the same directory as `pi-redteam.py`

#### "Request failed" errors
- Check network connectivity
- Verify API endpoint URL and authentication
- Review API rate limits
- Check firewall rules on Raspberry Pi

#### Service won't start
- Verify paths in `redteam.service` are correct
- Check permissions: `sudo chown -R pi:pi /home/pi/Python-Automation-and-Analysis-Toolkit`
- Review logs: `sudo journalctl -u redteam.service`

### References

- **OWASP LLM Top 10**: [LLM01: Prompt Injection](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **Research Papers**: Dialogue Injection Attack (DIA), Embedded Jailbreak Templates (EJT), AutoDAN
- **Attack Techniques**: ASCII Art Bypass, Unicode Tag Smuggling, Base64 Encoding

### License

This tool is provided for educational and authorized security testing purposes only.
