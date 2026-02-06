#!/bin/bash
# Script to create GitHub repo and push code

set -e

REPO_NAME="AI-DevSecOps-Orchestrator"
USERNAME="angelatierney"
GITHUB_URL="https://github.com/$USERNAME/$REPO_NAME"

echo "🚀 Creating and pushing $REPO_NAME to GitHub..."
echo ""

# Check if repo already exists
if curl -s -o /dev/null -w "%{http_code}" "https://github.com/$USERNAME/$REPO_NAME" | grep -q "200"; then
    echo "✓ Repository already exists on GitHub"
else
    echo "📦 Repository needs to be created on GitHub first"
    echo ""
    echo "Please do ONE of the following:"
    echo ""
    echo "OPTION 1: Create via Web Browser (Easiest)"
    echo "  1. Go to: https://github.com/new"
    echo "  2. Repository name: $REPO_NAME"
    echo "  3. Description: AI-Native DevSecOps tool for automated security scanning"
    echo "  4. Choose Public or Private"
    echo "  5. DO NOT initialize with README/gitignore (we have them)"
    echo "  6. Click 'Create repository'"
    echo "  7. Then run this script again, or run: git push -u origin main"
    echo ""
    echo "OPTION 2: Create via GitHub CLI (if installed)"
    echo "  gh repo create $REPO_NAME --public --source=. --remote=origin --push"
    echo ""
    echo "OPTION 3: Create via API (requires personal access token)"
    echo "  Set GITHUB_TOKEN environment variable and run this script"
    echo ""
    
    # Try to create via API if token is available
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "🔑 GitHub token found, attempting to create repository..."
        RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/user/repos \
            -d "{\"name\":\"$REPO_NAME\",\"description\":\"AI-Native DevSecOps tool for automated security scanning and infrastructure hardening\",\"private\":false}")
        
        HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
        if [ "$HTTP_CODE" = "201" ]; then
            echo "✅ Repository created successfully!"
        else
            echo "❌ Failed to create repository (HTTP $HTTP_CODE)"
            echo "Response: $(echo "$RESPONSE" | head -n-1)"
            exit 1
        fi
    else
        read -p "Press Enter after you've created the repository on GitHub, or Ctrl+C to exit..."
    fi
fi

echo ""
echo "📤 Pushing code to GitHub..."

# Push to GitHub
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🔗 Repository: $GITHUB_URL"
echo ""
echo "📝 Next steps:"
echo "  1. Add API keys as GitHub Secrets:"
echo "     Settings → Secrets and variables → Actions"
echo "     Add: OPENAI_API_KEY or ANTHROPIC_API_KEY"
echo "  2. Enable GitHub Actions in repository settings"
