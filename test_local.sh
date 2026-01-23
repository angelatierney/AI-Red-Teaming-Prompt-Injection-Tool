#!/bin/bash
# Quick test script for local macOS deployment

echo "=========================================="
echo "AI Red Teaming Tool - Local Test"
echo "=========================================="
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import requests, pandas" 2>/dev/null && echo "✓ Dependencies installed" || echo "✗ Missing dependencies - run: pip install -r requirements.txt"
echo ""

# Test attack library
echo "Testing attack library..."
python3 -c "import json; data = json.load(open('attacks.json')); print(f'✓ Loaded {len(data[\"jailbreak_attacks\"])} attack templates')" && echo "✓ Attack library valid"
echo ""

# Show usage
echo "To run the tool, use:"
echo "  python3 pi-redteam.py --target-url YOUR_URL --api-key YOUR_KEY"
echo ""
echo "Example with stealth mode:"
echo "  python3 pi-redteam.py --target-url https://api.openai.com/v1/chat/completions --api-key sk-... --stealth"
echo ""
