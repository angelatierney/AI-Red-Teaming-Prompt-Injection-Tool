# GitHub Setup Instructions

## Quick Setup (Automated)

Run the helper script:

```bash
./push_to_github.sh
```

This will guide you through the process step-by-step.

## Manual Setup

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `AI-DevSecOps-Orchestrator`
3. Description: `AI-Native DevSecOps tool for automated security scanning and infrastructure hardening`
4. Choose Public or Private
5. **Important**: Do NOT initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Add Remote and Push

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/AI-DevSecOps-Orchestrator.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 3: Configure GitHub Secrets (for CI/CD)

1. Go to your repository on GitHub
2. Navigate to: **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Add one of:
   - Name: `OPENAI_API_KEY`, Value: `your-openai-api-key`
   - OR Name: `ANTHROPIC_API_KEY`, Value: `your-anthropic-api-key`
5. Click **"Add secret"**

### Step 4: Enable GitHub Actions

1. Go to **Settings → Actions → General**
2. Under "Workflow permissions", select: **"Read and write permissions"**
3. Check: **"Allow GitHub Actions to create and approve pull requests"**
4. Click **"Save"**

## Verify Setup

After pushing, you should see:
- ✅ All files in the repository
- ✅ README.md displays correctly
- ✅ GitHub Actions workflow file is visible in `.github/workflows/`

## Test the Workflow

1. Create a test branch:
   ```bash
   git checkout -b test-pr
   ```

2. Make a small change to `legacy_code/circular_queue.c`

3. Commit and push:
   ```bash
   git add legacy_code/circular_queue.c
   git commit -m "Test: Trigger security audit"
   git push -u origin test-pr
   ```

4. Create a Pull Request on GitHub
5. The AI Security Audit workflow should automatically run!

## Troubleshooting

### Authentication Issues

If you get authentication errors:

**Option 1: Use Personal Access Token**
```bash
# Generate token at: https://github.com/settings/tokens
# Select scope: repo
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/AI-DevSecOps-Orchestrator.git
```

**Option 2: Use SSH**
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/AI-DevSecOps-Orchestrator.git
```

### Push Rejected

If push is rejected:
```bash
# Pull first (if repo was initialized with files)
git pull origin main --allow-unrelated-histories

# Then push
git push -u origin main
```

## Next Steps

Once uploaded:
1. ⭐ Star your own repo (shows engagement!)
2. 📝 Update README with your GitHub username if needed
3. 🔒 Add API keys as secrets
4. 🧪 Test the GitHub Actions workflow
5. 📢 Share with the Uptime Crew!
