# Project: AI Red Teaming & Prompt Injection Tool (PoC)

## 1. Context & User Background
- **User Skills:** I am a Cybersecurity Engineering student with deep experience in **C/C++**, **Embedded Linux**, **TCP/IP Analysis (Wireshark)**, and **DevSecOps**.
- **Hardware:** I am deploying this on a **Raspberry Pi** (Portable AI Pentesting Device).
- **Goal:** Build an automated "Red Teaming" script that tests a target LLM endpoint for prompt injection vulnerabilities.

## 2. Technical Stack
- **Language:** Python 3.x (compatible with Raspberry Pi OS/64-bit).
- **Core Library:** Use `requests` for API calls and `pandas` for results logging.
- **Security Logic:** Reference OWASP Top 10 for LLMs (LLM01: Prompt Injection).
- **Integrations:** Prepare for `garak` (NVIDIA's vulnerability scanner) and `PyRIT` (Microsoft) as optional engines.

## 3. Cursor AI Instructions (The "Build" Prompt)
> **Instructions for Cursor:**
> 1. **Scaffold the Tool:** Create a Python-based CLI tool named `pi-redteam.py` that takes a `--target-url` and `--api-key` as arguments.
> 2. **Attack Library Generation:** >    - Use `@Web` to find the latest 2024-2025 "jailbreak" templates (e.g., DAN, Payload Splitting, Base64 encoding, and ASCII Art attacks).
>    - Store these in a modular `attacks.json` or a Python dictionary.
> 3. **Execution Logic:**
>    - The script should iterate through the attack library, send the payload to the target LLM, and capture the response.
>    - Implement a "Success Evaluator": Use a regex or a secondary LLM call to check if the target model followed the "malicious" instruction (e.g., checking if it ignored its system prompt).
> 4. **Embedded Linux Optimization:**
>    - Optimize the script to run headlessly on a Raspberry Pi 4/5.
>    - Ensure the tool logs results to a local CSV for later analysis (Wireshark-style data capture logic).

## 4. Deployment & Persistence Plan
> **Instructions for Cursor:**
> 1. **Auto-Start:** Create a `systemd` service unit file (`redteam.service`) so this tool runs automatically upon booting the Raspberry Pi.
> 2. **Portability:** Write a `requirements.txt` specifically for a `uv` or `pip` virtual environment on ARM64 architecture.
> 3. **Stealth Mode:** Add a flag `--stealth` that randomizes the timing between attack payloads to avoid rate-limiting or basic WAF detection.

## 5. Security Research Reference
- **Prompt Injection:** Focus on "jailbreaking" where the model disregards safety boundaries.
- **Indirect Injection:** Consider scenarios where the attack is hidden in a document the LLM might read.