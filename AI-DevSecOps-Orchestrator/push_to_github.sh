#!/bin/bash
# Helper script to push AI-DevSecOps-Orchestrator to GitHub

set -e

REPO_NAME="AI-DevSecOps-Orchestrator"
GITHUB_USERNAME=""

echo "🚀 GitHub Upload Helper for $REPO_NAME"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

# Check if remote already exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "✓ Remote 'origin' already exists"
    REMOTE_URL=$(git remote get-url origin)
    echo "  Current remote: $REMOTE_URL"
    read -p "Do you want to update it? (y/n): " UPDATE_REMOTE
    if [ "$UPDATE_REMOTE" = "y" ]; then
        git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    fi
else
    echo "📡 Adding GitHub remote..."
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
fi

echo ""
echo "📋 Next steps:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: $REPO_NAME"
echo "   - Description: AI-Native DevSecOps tool for automated security scanning and infrastructure hardening"
echo "   - Visibility: Public or Private (your choice)"
echo "   - DO NOT initialize with README, .gitignore, or license (we already have these)"
echo ""
read -p "Press Enter after you've created the repository on GitHub..."

echo ""
echo "📤 Pushing to GitHub..."
echo ""

# Push to GitHub
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🔗 Your repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "📝 Don't forget to:"
echo "   1. Add your API keys as GitHub Secrets:"
echo "      - Settings → Secrets and variables → Actions"
echo "      - Add: OPENAI_API_KEY or ANTHROPIC_API_KEY"
echo "   2. Enable GitHub Actions in repository settings"
echo "   3. Update README if needed with your repo URL"
