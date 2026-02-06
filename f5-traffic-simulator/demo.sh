#!/bin/bash
# Demo script for F5 Traffic Simulator
# This script demonstrates the complete workflow

set -e

CONFIG_FILE="${1:-configs/load_balancer.yaml}"
LB_TYPE="${2:-nginx}"

echo "=========================================="
echo "F5 Traffic Simulator - Demo Workflow"
echo "=========================================="
echo ""
echo "Configuration: $CONFIG_FILE"
echo "Load Balancer: $LB_TYPE"
echo ""

# Step 1: Pre-flight validation
echo "Step 1: Pre-flight Validation"
echo "----------------------------"
python3 scripts/preflight_validator.py "$CONFIG_FILE"
VALIDATION_EXIT=$?

if [ $VALIDATION_EXIT -ne 0 ]; then
    echo "❌ Validation failed! Please fix configuration errors."
    exit 1
fi

echo ""
echo "✅ Validation passed!"
echo ""

# Step 2: Show what would be deployed (dry run)
echo "Step 2: Ansible Dry Run (Check Mode)"
echo "-------------------------------------"
cd ansible
ansible-playbook playbook.yml --check --diff \
    -e "lb_type=$LB_TYPE" \
    -e "config_file=../$CONFIG_FILE" || {
    echo "⚠️  Dry run completed (some errors expected in check mode)"
}

echo ""
echo "=========================================="
echo "Demo Complete!"
echo "=========================================="
echo ""
echo "To actually deploy, run:"
echo "  cd ansible"
echo "  ansible-playbook playbook.yml -e 'lb_type=$LB_TYPE' -e 'config_file=../$CONFIG_FILE'"
echo ""
