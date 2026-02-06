# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Validate Configuration

```bash
python3 scripts/preflight_validator.py configs/load_balancer.yaml
```

Expected output:
```
============================================================
Pre-flight Configuration Validation Report
============================================================
File: configs/load_balancer.yaml

✅ Configuration is valid!
============================================================
```

### 3. Deploy Load Balancer

**NGINX:**
```bash
cd ansible
ansible-playbook playbook.yml -e "lb_type=nginx" -e "config_file=../configs/load_balancer.yaml"
```

**HAProxy:**
```bash
cd ansible
ansible-playbook playbook.yml -e "lb_type=haproxy" -e "config_file=../configs/load_balancer.yaml"
```

### 4. Verify Deployment

**NGINX:**
```bash
sudo systemctl status nginx
sudo nginx -t
curl http://localhost/health
```

**HAProxy:**
```bash
sudo systemctl status haproxy
sudo haproxy -f /etc/haproxy/haproxy.cfg -c
curl http://localhost:8404/stats
```

## 📋 Interview Checklist

Before your interview, make sure you can explain:

- ✅ **Infrastructure as Code**: How Ansible automates configuration
- ✅ **Jinja2 Templates**: How templates generate dynamic configs
- ✅ **Pre-flight Validation**: Why validation before deployment matters
- ✅ **Load Balancing**: Round-robin, least connections, IP hash
- ✅ **Health Checks**: How they prevent traffic to unhealthy servers
- ✅ **Frontend/Backend**: The architecture pattern used

## 💡 Key Commands to Remember

```bash
# Validate config
python3 scripts/preflight_validator.py configs/load_balancer.yaml

# Dry run (test without changes)
cd ansible && ansible-playbook playbook.yml --check -e "lb_type=nginx"

# Deploy
cd ansible && ansible-playbook playbook.yml -e "lb_type=nginx"

# View generated config
cat /etc/nginx/conf.d/load_balancer.conf  # NGINX
cat /etc/haproxy/haproxy.cfg              # HAProxy
```
