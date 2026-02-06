#!/bin/bash
# Setup script for AI-DevSecOps-Orchestrator

set -e

echo "🔧 Setting up AI-DevSecOps-Orchestrator..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for API keys
echo ""
echo "🔑 Checking API keys..."
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  WARNING: No API keys found in environment"
    echo "   Set one of: OPENAI_API_KEY or ANTHROPIC_API_KEY"
    echo "   Example: export OPENAI_API_KEY='your-key-here'"
else
    if [ -n "$OPENAI_API_KEY" ]; then
        echo "✓ OPENAI_API_KEY is set"
    fi
    if [ -n "$ANTHROPIC_API_KEY" ]; then
        echo "✓ ANTHROPIC_API_KEY is set"
    fi
fi

# Run tests
echo ""
echo "🧪 Running tests..."
pytest tests/ -v || echo "⚠️  Some tests may require API keys to pass"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the agent:"
echo "  source venv/bin/activate"
echo "  python src/agent.py legacy_code/circular_queue.c"
