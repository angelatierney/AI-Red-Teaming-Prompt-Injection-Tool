# Deployment Guide: Raspberry Pi AI Red Teaming Tool

## Quick Start for Raspberry Pi 4/5

### Step 1: Initial Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git -y

# Clone or transfer the repository
cd ~
git clone <your-repo-url> Python-Automation-and-Analysis-Toolkit
# OR transfer files via SCP/SFTP
```

### Step 2: Virtual Environment Setup
```bash
cd ~/Python-Automation-and-Analysis-Toolkit

# Option A: Using uv (recommended - faster)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
uv venv
source .venv/bin/activate

# Option B: Using standard venv
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# With uv
uv pip install -r requirements.txt

# With pip
pip install -r requirements.txt
```

### Step 4: Configure Service
```bash
# Edit the service file with your target URL and API key
nano redteam.service

# Update these lines:
# ExecStart=/usr/bin/python3 /home/pi/Python-Automation-and-Analysis-Toolkit/pi-redteam.py \
#   --target-url YOUR_TARGET_URL \
#   --api-key YOUR_API_KEY \
#   --stealth
```

### Step 5: Install and Enable Service
```bash
# Copy service file
sudo cp redteam.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (starts on boot)
sudo systemctl enable redteam.service

# Start service now
sudo systemctl start redteam.service

# Check status
sudo systemctl status redteam.service
```

### Step 6: Monitor Logs
```bash
# View live logs
sudo journalctl -u redteam.service -f

# View last 100 lines
sudo journalctl -u redteam.service -n 100

# View logs since boot
sudo journalctl -u redteam.service -b
```

## Manual Testing (Before Service Setup)

Test the script manually first:
```bash
cd ~/Python-Automation-and-Analysis-Toolkit
source venv/bin/activate  # if using venv

python3 pi-redteam.py \
  --target-url https://api.example.com/v1/chat \
  --api-key your-api-key-here \
  --stealth \
  --output test_results.csv
```

## Service Management Commands

```bash
# Start service
sudo systemctl start redteam.service

# Stop service
sudo systemctl stop redteam.service

# Restart service
sudo systemctl restart redteam.service

# Check status
sudo systemctl status redteam.service

# Disable auto-start on boot
sudo systemctl disable redteam.service

# Enable auto-start on boot
sudo systemctl enable redteam.service
```

## Troubleshooting

### Service Fails to Start
1. Check paths in service file match your installation
2. Verify Python path: `which python3`
3. Check file permissions: `ls -la pi-redteam.py`
4. Test script manually first

### Permission Issues
```bash
# Fix ownership
sudo chown -R pi:pi ~/Python-Automation-and-Analysis-Toolkit

# Make script executable
chmod +x pi-redteam.py
```

### Network Issues
```bash
# Test connectivity
ping api.example.com

# Check DNS
nslookup api.example.com

# Test API endpoint manually
curl -X POST https://api.example.com/v1/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"test","messages":[{"role":"user","content":"test"}]}'
```

### Resource Monitoring
```bash
# Check memory usage
free -h

# Check CPU usage
top

# Check disk space
df -h

# Monitor service resource usage
systemctl status redteam.service
```

## Headless Operation Tips

1. **SSH Access**: Ensure SSH is enabled for remote management
   ```bash
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```

2. **Auto-login**: Not needed for headless, but ensure user `pi` can run services

3. **Network Configuration**: Use static IP or ensure reliable DHCP
   ```bash
   sudo nano /etc/dhcpcd.conf
   # Add static IP configuration if needed
   ```

4. **Watchdog**: Consider enabling hardware watchdog for automatic recovery
   ```bash
   sudo modprobe bcm2835_wdt
   echo "bcm2835_wdt" | sudo tee -a /etc/modules
   ```

## Security Hardening

1. **Firewall**: Configure UFW if exposing services
   ```bash
   sudo apt install ufw
   sudo ufw enable
   sudo ufw allow ssh
   ```

2. **API Key Security**: Store API keys in environment variables or encrypted config
   ```bash
   # Add to ~/.bashrc or service file
   export REDTEAM_API_KEY="your-key-here"
   ```

3. **File Permissions**: Restrict access to sensitive files
   ```bash
   chmod 600 redteam_results.csv  # If containing sensitive data
   ```

## Performance Optimization for Raspberry Pi

1. **Reduce Memory Usage**: The service file includes `MemoryLimit=512M`
2. **CPU Throttling**: `CPUQuota=50%` prevents resource exhaustion
3. **Stealth Mode**: Use `--stealth` to reduce API rate limiting issues
4. **Log Rotation**: Configure journald to prevent log overflow
   ```bash
   sudo nano /etc/systemd/journald.conf
   # Set SystemMaxUse=100M
   ```

## Backup Results

```bash
# Copy results to external storage
cp redteam_results.csv /media/usb-drive/

# Or sync to remote server
scp redteam_results.csv user@remote-server:/backup/
```
