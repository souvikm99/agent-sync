#!/usr/bin/env bash
# Install script for agent-sync
# Usage: curl -fsSL https://raw.githubusercontent.com/<YOUR_USERNAME>/agent-sync/main/install.sh | bash

set -e

REPO_URL="https://raw.githubusercontent.com/souvikm99/agent-sync/main"

echo "Installing agent-sync into current repository..."

mkdir -p .agents/scripts

# Download generalized sync script
curl -fsSL "$REPO_URL/sync_agents.py" -o .agents/scripts/sync_agents.py
chmod +x .agents/scripts/sync_agents.py

# Set up pre-commit hook
if [ -d .git ]; then
    mkdir -p .git/hooks
    curl -fsSL "$REPO_URL/pre-commit" -o .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "✓ Installed git pre-commit hook"
else
    echo "⚠ Not a git repository, skipping pre-commit hook"
fi

# Ensure AGENTS.md exists
if [ ! -f AGENTS.md ]; then
    echo -e "# Repository Guidelines\n\n## Project Structure\n\n\`\`\`text\n\`\`\`\n" > AGENTS.md
    echo "✓ Created base AGENTS.md"
fi

# Run initial sync
if command -v python3 &>/dev/null; then
    python3 .agents/scripts/sync_agents.py
else
    python .agents/scripts/sync_agents.py
fi

echo "✓ Installation complete! AGENTS.md will now auto-update on commit."
