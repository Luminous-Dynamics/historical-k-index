#!/usr/bin/env bash
#
# Setup script to create and push the historical-k-index repository to GitHub
#
# Usage: ./SETUP_GITHUB.sh
#

set -e  # Exit on error

echo "=========================================="
echo "Historical K-Index GitHub Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "CITATION.cff" ]; then
    echo "❌ Error: Not in repository root directory"
    echo "Please cd to historical-k-index-repo/ first"
    exit 1
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

# Check git config
if ! git config user.name > /dev/null 2>&1; then
    echo ""
    echo "⚠️  Git user.name not set. Please configure:"
    echo "   git config --global user.name \"Your Name\""
    echo "   git config --global user.email \"your.email@example.com\""
    exit 1
fi

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .
echo "✓ Files added"

# Create initial commit
echo ""
echo "💾 Creating initial commit..."
if git rev-parse HEAD > /dev/null 2>&1; then
    echo "✓ Repository already has commits"
else
    git commit -m "Initial commit: Historical K-Index replication package

- Complete data collection pipeline (191,913 data points)
- Validated H₇ component (2,352 observations, 159 countries, 1996-2021)
- Supplementary materials generation scripts
- Reproducible environment (Nix + Poetry)
- Full documentation

Key finding: Validated H₇ yields -7.0% more conservative K(t) than
demographic proxies, demonstrating empirical rigor over methodological
optimism.

Ready for Nature Sustainability submission."
    echo "✓ Initial commit created"
fi

# Instructions for GitHub
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "   Repository name: historical-k-index"
echo "   Description: Global Coordination Infrastructure 1810-2020"
echo "   Public repository"
echo "   ☐ Do NOT initialize with README, .gitignore, or license"
echo ""
echo "2. After creating the repository, run these commands:"
echo ""
echo "   git remote add origin https://github.com/Luminous-Dynamics/historical-k-index.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Create v1.0 release:"
echo "   - Go to repository → Releases → Create a new release"
echo "   - Tag: v1.0.0"
echo "   - Title: \"Historical K-Index v1.0 - Nature Submission\""
echo "   - Description: Copy from README.md key findings section"
echo ""
echo "4. Link to Zenodo:"
echo "   - Go to https://zenodo.org/account/settings/github/"
echo "   - Enable historical-k-index repository"
echo "   - Create new release on GitHub (this triggers Zenodo DOI)"
echo "   - Copy DOI and update README.md + CITATION.cff"
echo ""
echo "=========================================="
echo "Ready to push! 🚀"
echo "=========================================="
