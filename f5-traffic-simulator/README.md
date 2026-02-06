# F5 Traffic Simulator - Load Balancer Configuration Generator

A comprehensive Infrastructure as Code (IaC) solution for automating load balancer configuration using Ansible, Jinja2 templates, and Python validation scripts. This project demonstrates how to manage traffic distribution and health monitoring similar to F5 Big-IP using NGINX or HAProxy.

## 🎯 Project Overview

This project automates the setup and configuration of load balancers by:
- **Ansible Playbooks**: Automate installation and configuration
- **Jinja2 Templates**: Generate dynamic configuration files from YAML/JSON
- **Python Pre-flight Validation**: Validate configuration syntax before deployment
- **Multi-Platform Support**: Works with NGINX and HAProxy

## 📁 Project Structure

```
f5-traffic-simulator/
├── ansible/
│   ├── playbook.yml              # Main Ansible playbook
│   ├── hosts.ini                 # Inventory file
│   └── roles/
│       ├── nginx-lb/             # NGINX load balancer role
│       │   ├── tasks/
│       │   ├── templates/
│       │   └── defaults/
│       └── haproxy-lb/           # HAProxy load balancer role
│           ├── tasks/
│           ├── templates/
│           └── defaults/
├── configs/
│   ├── load_balancer.yaml        # Sample YAML configuration
│   └── load_balancer.json        # Sample JSON configuration
├── scripts/
│   └── preflight_validator.py    # Python validation script
├── requirements.txt              # Python dependencies
├── ansible.cfg                   # Ansible configuration
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Ansible 6.0+
- sudo/root access (for installing packages)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd f5-traffic-simulator
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ansible (if not already installed):**
   ```bash
   pip install ansible
   ```

### Usage

#### Step 1: Validate Configuration (Pre-flight Check)

Before running Ansible, validate your configuration file:

```bash
# Validate YAML configuration
python3 scripts/preflight_validator.py configs/load_balancer.yaml

# Validate JSON configuration
python3 scripts/preflight_validator.py configs/load_balancer.json
```

The validator checks for:
- ✅ File existence
- ✅ JSON/YAML syntax correctness
- ✅ Required configuration keys
- ✅ Data type validation
- ⚠️ Missing optional fields (warnings)

#### Step 2: Deploy Load Balancer

**For NGINX:**
```bash
cd ansible
ansible-playbook playbook.yml -e "lb_type=nginx" -e "config_file=../configs/load_balancer.yaml"
```

**For HAProxy:**
```bash
cd ansible
ansible-playbook playbook.yml -e "lb_type=haproxy" -e "config_file=../configs/load_balancer.yaml"
```

## 📝 Configuration File Format

### YAML Example (`configs/load_balancer.yaml`)

```yaml
frontend:
  name: "web_frontend"
  protocol: "http"
  port: 80

backend_pools:
  - name: "web_servers"
    load_balancing_method: "round_robin"
    servers:
      - name: "web1"
        address: "192.168.1.10"
        port: 8080
        weight: 1

health_checks:
  enabled: true
  interval: 10
  timeout: 5
  path: "/health"
```

### Configuration Options

#### Frontend
- `name`: Frontend name identifier
- `protocol`: `http` or `https`
- `port`: Listening port (default: 80)
- `server_name`: Server name for NGINX (optional)
- `ssl_certificate`: Path to SSL certificate (for HTTPS)
- `ssl_key`: Path to SSL private key (for HTTPS)

#### Backend Pools
- `name`: Pool identifier
- `load_balancing_method`: 
  - NGINX: `round_robin`, `least_conn`, `ip_hash`
  - HAProxy: `roundrobin`, `leastconn`, `source`
- `path`: URL path to route to this pool (optional)
- `servers`: List of backend servers
  - `name`: Server identifier
  - `address`: IP address or hostname
  - `port`: Server port
  - `weight`: Server weight (higher = more traffic)
  - `max_fails`: Maximum failures before marking down (NGINX)
  - `fail_timeout`: Timeout period (NGINX)
  - `backup`: Mark as backup server (optional)

#### Health Checks
- `enabled`: Enable health checks (default: true)
- `interval`: Check interval in seconds
- `timeout`: Request timeout in seconds
- `path`: Health check endpoint path
- `expected_status`: Expected HTTP status code

## 🔧 Ansible Roles

### NGINX Load Balancer Role

**Features:**
- Installs NGINX if not present
- Generates upstream configuration for backend pools
- Configures load balancing methods
- Sets up health check endpoints
- Validates configuration before applying

**Generated Config Location:** `/etc/nginx/conf.d/load_balancer.conf`

### HAProxy Load Balancer Role

**Features:**
- Installs HAProxy if not present
- Generates frontend/backend configuration
- Configures load balancing algorithms
- Sets up health checks with HTTP checks
- Includes statistics page (port 8404)

**Generated Config Location:** `/etc/haproxy/haproxy.cfg`

## 🧪 Testing

### Test Configuration Validation

```bash
# Test with valid configuration
python3 scripts/preflight_validator.py configs/load_balancer.yaml

# Test with invalid configuration (should fail)
python3 scripts/preflight_validator.py configs/invalid.yaml
```

### Test Ansible Playbook (Dry Run)

```bash
cd ansible
ansible-playbook playbook.yml --check --diff -e "lb_type=nginx"
```

### Verify Load Balancer

**NGINX:**
```bash
# Check status
sudo systemctl status nginx

# Test configuration
sudo nginx -t

# Check generated config
cat /etc/nginx/conf.d/load_balancer.conf
```

**HAProxy:**
```bash
# Check status
sudo systemctl status haproxy

# Test configuration
sudo haproxy -f /etc/haproxy/haproxy.cfg -c

# View statistics (if enabled)
curl http://localhost:8404/stats
```

## 🎓 Interview Talking Points

This project demonstrates:

1. **Infrastructure as Code (IaC)**: Configuration is version-controlled and repeatable
2. **Automation**: Ansible automates the entire deployment process
3. **Template-Driven Configuration**: Jinja2 templates enable dynamic config generation
4. **Pre-flight Validation**: Python script ensures configuration integrity before deployment
5. **Multi-Platform Support**: Same configuration works with NGINX and HAProxy
6. **Load Balancing Concepts**: 
   - Frontend/Backend architecture
   - Multiple load balancing algorithms
   - Health checks and failover
   - Server weighting
7. **DevOps Best Practices**:
   - Configuration validation
   - Idempotent deployments
   - Service management
   - Configuration testing

## 🔍 Key Features

- ✅ **Pre-flight Validation**: Python script validates JSON/YAML before Ansible runs
- ✅ **Jinja2 Templates**: Dynamic configuration generation from variables
- ✅ **Multiple Load Balancers**: Support for NGINX and HAProxy
- ✅ **Health Checks**: Configurable health monitoring
- ✅ **Load Balancing Methods**: Round-robin, least connections, IP hash
- ✅ **Server Weighting**: Distribute traffic based on server capacity
- ✅ **Idempotent**: Safe to run multiple times
- ✅ **Configuration Testing**: Validates configs before applying

## 📚 Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [NGINX Load Balancing](https://nginx.org/en/docs/http/load_balancing.html)
- [HAProxy Configuration](http://www.haproxy.org/#docs)
- [Jinja2 Template Syntax](https://jinja.palletsprojects.com/)

## 🤝 Contributing

Feel free to extend this project with:
- Additional load balancer types (Traefik, Envoy, etc.)
- More sophisticated health check strategies
- SSL/TLS certificate management
- Monitoring and alerting integration
- Multi-environment support (dev/staging/prod)

## 📄 License

This project is provided as-is for educational and interview demonstration purposes.

---

**Good luck with your interview! 🚀**
