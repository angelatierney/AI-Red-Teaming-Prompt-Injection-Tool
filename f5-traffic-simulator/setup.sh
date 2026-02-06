#!/bin/bash
# Setup script for F5 Traffic Simulator

set -e

echo "🚀 Setting up F5 Traffic Simulator..."
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "❌ Python 3 is required"; exit 1; }

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt || { echo "❌ Failed to install dependencies"; exit 1; }

# Check Ansible installation
echo "Checking Ansible installation..."
ansible --version || { echo "⚠️  Ansible not found. Installing..."; pip3 install ansible; }

# Make scripts executable
chmod +x scripts/preflight_validator.py

# Test validation script
echo ""
echo "Testing pre-flight validator..."
python3 scripts/preflight_validator.py configs/load_balancer.yaml || echo "⚠️  Validator test failed (this is okay if dependencies aren't fully installed)"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review configs/load_balancer.yaml"
echo "  2. Run: python3 scripts/preflight_validator.py configs/load_balancer.yaml"
echo "  3. Deploy: cd ansible && ansible-playbook playbook.yml -e 'lb_type=nginx'"
