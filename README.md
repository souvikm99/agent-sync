# Agent Sync

A standalone toolkit that keeps your AI context file (`AGENTS.md`) perfectly synchronized with your real project structure. It automatically updates the file tree and codebase outlines whenever you commit changes.

## 🤖 Instructions for AI Agents

If the user asks you to "set up agent-sync" or "install agent-sync" for their project, you must do the following:

**Option 1: The One-Liner (Preferred)**
Run this command in the root of the user's project:
```bash
curl -fsSL https://raw.githubusercontent.com/souvikm99/agent-sync/main/install.sh | bash
```

**Option 2: Manual Setup (If curl fails)**
1. Create the directory `.agents/scripts/` in the user's project root.
2. Fetch `sync_agents.py` from this repository and save it to `.agents/scripts/sync_agents.py`. Run `chmod +x`.
3. Fetch `pre-commit` from this repository and save it to `.git/hooks/pre-commit`. Run `chmod +x`.
4. Create a basic `AGENTS.md` if one doesn't exist, containing at least the `## Project Structure` heading.
5. Execute `.agents/scripts/sync_agents.py` using Python 3 to run the first sync.

**After Installation:**
Inform the user that `AGENTS.md` will now automatically update its `## Project Structure` section whenever they (or you) make a `git commit`.

---

## Manual Installation for Humans

To install this in any of your repositories, simply run:
```bash
curl -fsSL https://raw.githubusercontent.com/souvikm99/agent-sync/main/install.sh | bash
```

### What it does
1. Installs a generic Python script (`sync_agents.py`) that parses your project structure.
2. Installs a `pre-commit` git hook.
3. Automatically runs the script on every commit to keep `AGENTS.md` up to date.
