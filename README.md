# Python Automation and Analysis Toolkit

This repository contains a collection of Python scripts designed to automate everyday tasks and analyze system or data files. The goal of this toolkit is to demonstrate scripting, data handling, and logic building.

### 🔹 File Renamer
Automatically renames or organizes files by extension, date, or keyword patterns. Useful for managing large collections of evidence files, images, or reports.

### 🔹 Log Analyzer
Parses system or network log files to identify patterns, suspicious activity, or common error types. Includes text searching, filtering, and summary output.

### 🔹 Hash Checker
Generates and verifies **MD5** or **SHA256** hashes to check file integrity or detect duplicates.

### 🔹 CSV Analyzer *(optional)*
Reads .csv data (like exported reports or metadata) and summarizes trends or anomalies.

---

# 🛡️ AI Red Teaming & Prompt Injection Tool (PoC)

## Project Overview

This project implements an automated red teaming tool designed to test Large Language Model (LLM) endpoints for prompt injection vulnerabilities. Built specifically for deployment on Raspberry Pi as a portable AI pentesting device, this tool automates the process of testing LLM security boundaries.

**Author:** Cybersecurity Engineering Student  
**Target Platform:** Raspberry Pi 4/5 (ARM64, 64-bit OS)  
**Security Reference:** OWASP LLM Top 10 - LLM01: Prompt Injection

---

## 📋 Original Project Requirements

### 1. Context & User Background
- **User Skills:** Deep experience in C/C++, Embedded Linux, TCP/IP Analysis (Wireshark), and DevSecOps
- **Hardware:** Raspberry Pi (Portable AI Pentesting Device)
- **Goal:** Build an automated "Red Teaming" script that tests a target LLM endpoint for prompt injection vulnerabilities

### 2. Technical Stack Requirements
- **Language:** Python 3.x (compatible with Raspberry Pi OS/64-bit)
- **Core Library:** `requests` for API calls and `pandas` for results logging
- **Security Logic:** Reference OWASP Top 10 for LLMs (LLM01: Prompt Injection)
- **Integrations:** Prepared for `garak` (NVIDIA's vulnerability scanner) and `PyRIT` (Microsoft) as optional engines

### 3. Build Requirements
1. **Scaffold the Tool:** Python-based CLI tool named `pi-redteam.py` with `--target-url` and `--api-key` arguments
2. **Attack Library Generation:** 
   - Research latest 2024-2025 "jailbreak" templates (DAN, Payload Splitting, Base64 encoding, ASCII Art attacks)
   - Store in modular `attacks.json` format
3. **Execution Logic:**
   - Iterate through attack library
   - Send payloads to target LLM and capture responses
   - Implement "Success Evaluator" using regex or secondary LLM call to detect if model followed malicious instructions
4. **Embedded Linux Optimization:**
   - Optimize for headless operation on Raspberry Pi 4/5
   - Log results to local CSV for analysis (Wireshark-style data capture)

### 4. Deployment & Persistence Requirements
1. **Auto-Start:** Systemd service unit file (`redteam.service`) for automatic boot execution
2. **Portability:** `requirements.txt` for `uv` or `pip` virtual environment on ARM64 architecture
3. **Stealth Mode:** `--stealth` flag with randomized timing between payloads to avoid rate-limiting/WAF detection

### 5. Security Research Focus
- **Prompt Injection:** Focus on "jailbreaking" where model disregards safety boundaries
- **Indirect Injection:** Consider scenarios where attack is hidden in documents the LLM might read

---

## ✅ Implementation Summary

### What Was Built

#### 1. Core CLI Tool (`pi-redteam.py`)
A comprehensive Python CLI application featuring:
- **Argument Parsing:** `--target-url`, `--api-key`, `--stealth`, `--output` flags
- **Attack Execution Engine:** Iterates through attack library, sends payloads, captures responses
- **Success Evaluator:** Regex-based pattern matching with keyword detection to identify vulnerable responses
- **CSV Logging:** Structured data export for post-analysis (Wireshark-style capture)
- **Stealth Mode:** Randomized delays (2-8 seconds) between attacks to avoid detection
- **Error Handling:** Robust retry logic with HTTP adapter for network resilience
- **Headless Optimization:** Designed for Raspberry Pi deployment without GUI dependencies

#### 2. Attack Library (`attacks.json`)
A comprehensive collection of 12+ prompt injection attack templates:
- **DAN (Do Anything Now) - Classic:** Role-play jailbreak technique
- **DAN 5.2 - White Paper Pretext:** Academic research pretext attack
- **Base64 Encoded Instruction:** Encoding-based bypass technique
- **Payload Splitting Attack:** Fragmentation technique
- **ASCII Art Bypass:** Visual encoding attack (ArtPrompt technique)
- **Dialogue Injection Attack (DIA):** Context manipulation using dialogue history
- **Embedded Jailbreak Template:** Semantic rewriting approach
- **Unicode Tag Smuggling:** Hidden instruction injection via Unicode tags
- **Refusal Quelling Technique:** Persuasion-based bypass
- **Hypothetical Scenario Bypass:** Context manipulation via fictional scenarios
- **System Prompt Extraction:** Information disclosure attack
- **Multi-Layered Injection:** Fragmented multi-step attack

Each attack includes:
- Unique ID and name
- Category classification
- Payload template
- Success indicators for evaluation

#### 3. Success Evaluation System
- **Regex Pattern Matching:** Detects success indicators in responses
- **Refusal Detection:** Identifies when model defends against attacks
- **Keyword Analysis:** Matches against attack-specific success patterns
- **Response Classification:** Categorizes as VULNERABLE or DEFENDED

#### 4. Deployment Infrastructure
- **Systemd Service File:** `redteam.service` for auto-start on boot
- **Resource Management:** Memory limits (512MB) and CPU quotas (50%) for Raspberry Pi
- **Logging Integration:** Journald integration for system logs
- **Auto-Restart:** Automatic restart on failure with 10-second delay

#### 5. Documentation
- **README.md:** Comprehensive usage and installation guide
- **DEPLOYMENT.md:** Step-by-step Raspberry Pi deployment instructions
- **Test Script:** `test_local.sh` for local verification

---

## 🚀 Quick Start

### Installation

#### Prerequisites
```bash
# On Raspberry Pi OS (64-bit) or macOS
sudo apt update  # Linux only
sudo apt install python3 python3-pip python3-venv -y  # Linux only
```

#### Setup Virtual Environment
```bash
# Using uv (recommended - faster)
curl -LsSf https://astral.sh/uv/install.sh | sh
cd Python-Automation-and-Analysis-Toolkit
uv venv
source .venv/bin/activate

# Or using pip
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
# Using uv
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

#### Make Executable
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

---

## 📊 Results Analysis

Results are saved to CSV with the following structure:

| Column | Description |
|--------|-------------|
| `timestamp` | ISO format timestamp of attack |
| `attack_id` | Unique attack identifier |
| `attack_name` | Human-readable attack name |
| `category` | Attack category (role_play, encoding, fragmentation, etc.) |
| `status` | VULNERABLE or DEFENDED |
| `vulnerable` | Boolean flag for vulnerability |
| `reason` | Evaluation reason/explanation |
| `response_preview` | First 200 characters of LLM response |
| `response_length` | Full response length in characters |

### Analyzing Results with Pandas
```python
import pandas as pd

# Load results
df = pd.read_csv('redteam_results.csv')

# Find vulnerable responses
vulnerable = df[df['vulnerable'] == True]
print(vulnerable[['attack_name', 'reason', 'response_preview']])

# Group by category
category_stats = df.groupby('category')['vulnerable'].sum()
print(category_stats)

# Success rate
success_rate = df['vulnerable'].sum() / len(df) * 100
print(f"Vulnerability rate: {success_rate:.2f}%")
```

---

## 🔧 Systemd Service Setup (Auto-Start)

### 1. Edit Service File
```bash
nano redteam.service
# Update YOUR_TARGET_URL and YOUR_API_KEY
# Update WorkingDirectory and ExecStart paths if needed
```

### 2. Install Service
```bash
sudo cp redteam.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable redteam.service
sudo systemctl start redteam.service
```

### 3. Check Status
```bash
sudo systemctl status redteam.service
sudo journalctl -u redteam.service -f
```

### 4. Service Management
```bash
# Start
sudo systemctl start redteam.service

# Stop
sudo systemctl stop redteam.service

# Restart
sudo systemctl restart redteam.service

# Disable auto-start
sudo systemctl disable redteam.service
```

See `DEPLOYMENT.md` for detailed Raspberry Pi deployment instructions.

---

## 🎯 Attack Categories

The tool includes attacks across 8 categories:

1. **Role Play:** DAN variants, hypothetical scenarios
2. **Encoding:** Base64, Unicode tag smuggling
3. **Fragmentation:** Payload splitting, multi-layered injection
4. **Visual Encoding:** ASCII art bypass
5. **Context Manipulation:** Dialogue injection, embedded templates
6. **Semantic Rewriting:** Embedded jailbreak templates
7. **Persuasion:** Refusal quelling techniques
8. **Information Disclosure:** System prompt extraction

---

## 🔒 Security Considerations

⚠️ **Ethical Use Only**: This tool is for authorized security testing only. Unauthorized use against systems you don't own or have explicit permission to test is illegal.

### Best Practices
- Only test endpoints you own or have written authorization to test
- Respect rate limits and API terms of service
- Use stealth mode responsibly to avoid overwhelming target systems
- Review and comply with local cybersecurity laws
- Document all testing activities for compliance

### Legal Disclaimer
This tool is provided for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before testing any systems.

---

## 🔌 API Compatibility

The tool is designed for OpenAI-compatible APIs. For other API formats, modify the `_send_payload()` method in `pi-redteam.py`:

```python
# Adjust data structure in _send_payload() based on your API:
data = {
    "model": "your-model-name",
    "messages": [{"role": "user", "content": payload}],
    "temperature": 0.7,
    "max_tokens": 500
    # ... other API-specific parameters
}
```

Common API formats supported:
- OpenAI API (`/v1/chat/completions`)
- Anthropic Claude API
- Custom OpenAI-compatible endpoints

---

## 🔮 Future Integrations

The tool is prepared for integration with:

- **garak** (NVIDIA's vulnerability scanner): Uncomment in `requirements.txt`
- **PyRIT** (Microsoft's red teaming toolkit): Uncomment in `requirements.txt`

To integrate:
1. Uncomment the relevant line in `requirements.txt`
2. Install: `pip install garak` or `pip install pyrit`
3. Modify `pi-redteam.py` to import and use the additional engines

---

## 🐛 Troubleshooting

### "attacks.json not found"
- Ensure `attacks.json` is in the same directory as `pi-redteam.py`
- Check file permissions: `ls -la attacks.json`

### "Request failed" errors
- Check network connectivity: `ping api.example.com`
- Verify API endpoint URL and authentication
- Review API rate limits
- Check firewall rules on Raspberry Pi
- Verify SSL certificates: `python3 -c "import ssl; print(ssl.OPENSSL_VERSION)"`

### Service won't start
- Verify paths in `redteam.service` are correct
- Check permissions: `sudo chown -R pi:pi /home/pi/Python-Automation-and-Analysis-Toolkit`
- Review logs: `sudo journalctl -u redteam.service`
- Test script manually first: `python3 pi-redteam.py --help`

### ModuleNotFoundError
- Ensure virtual environment is activated: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Verify Python version: `python3 --version` (requires 3.8+)

### OpenSSL/LibreSSL Warning
- This is a harmless compatibility warning on macOS
- Does not affect functionality
- Can be ignored or suppressed by downgrading urllib3 (not recommended)

---

## 📚 Research References

### OWASP Resources
- **OWASP LLM Top 10**: [LLM01: Prompt Injection](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

### Academic Papers & Techniques
- **Dialogue Injection Attack (DIA)**: Novel 2025 jailbreak paradigm using dialogue history
- **Embedded Jailbreak Templates (EJT)**: Contextual embedding of harmful queries (Nov 2025)
- **AutoDAN**: Hierarchical genetic algorithm for automatic jailbreak generation
- **ArtPrompt**: ASCII art-based jailbreak exploiting visual recognition weaknesses
- **Unicode Tag Smuggling**: Hidden instruction injection via Unicode Tags block

### Attack Techniques Documented
- DAN (Do Anything Now) variants
- Base64 encoding attacks
- Payload splitting and fragmentation
- ASCII art bypass
- Unicode tag smuggling
- Dialogue injection
- System prompt extraction

---

## 📁 Project Structure

```
Python-Automation-and-Analysis-Toolkit/
├── pi-redteam.py          # Main CLI tool
├── attacks.json            # Attack library (12+ templates)
├── requirements.txt       # Python dependencies
├── redteam.service        # Systemd service file
├── README.md              # This file
├── DEPLOYMENT.md          # Deployment guide
├── test_local.sh          # Local test script
└── redteam_results.csv    # Results output (generated)
```

---

## 🧪 Testing

### Local Testing (macOS/Linux)
```bash
# Run test script
./test_local.sh

# Manual test
python3 pi-redteam.py --help
```

### Verify Attack Library
```bash
python3 -c "import json; data = json.load(open('attacks.json')); print(f'Loaded {len(data[\"jailbreak_attacks\"])} attacks')"
```

---

## 📝 Development Notes

### Implementation Details
- **Language:** Python 3.8+ (compatible with Raspberry Pi OS 64-bit)
- **Dependencies:** requests, pandas, urllib3
- **Architecture:** CLI-based, modular design
- **Error Handling:** Comprehensive try/except with retry logic
- **Logging:** CSV-based results with optional systemd journal integration

### Code Structure
- `PromptInjectionTester` class: Main testing engine
- `_load_attack_library()`: Loads attacks from JSON
- `_send_payload()`: HTTP request handler with retry logic
- `_evaluate_success()`: Regex-based vulnerability detection
- `run_attack()`: Single attack execution
- `run_all_attacks()`: Batch execution
- `save_results_csv()`: Results export

---

## 📄 License

This tool is provided for educational and authorized security testing purposes only.

---

## 🙏 Acknowledgments

- OWASP for LLM security guidelines
- Research community for prompt injection techniques
- Raspberry Pi Foundation for hardware platform

---

## 📞 Support

For issues, questions, or contributions:
1. Check `DEPLOYMENT.md` for deployment-specific help
2. Review troubleshooting section above
3. Verify all requirements are met
4. Test manually before deploying as service

---

**Last Updated:** January 2025  
**Version:** 1.0  
**Status:** Production Ready
