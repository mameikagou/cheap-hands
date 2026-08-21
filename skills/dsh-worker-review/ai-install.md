# Auto-Install Instructions for AI Agents

> YOU ARE AN AI AGENT. These instructions are for you, not for a human.
> The user has asked you to install the "dsh-worker-review" skill.
> Follow each step in order. Do not skip steps. Do not ask for confirmation
> unless a step explicitly says to.

## Pre-flight Checks

1. Verify you have file write access to the user's home directory
2. Check if `$HOME/.claude/skills/dsh-worker-review/` already exists
   - If YES: Ask the user "Skill 'dsh-worker-review' already installed. Overwrite? (y/n)"
   - If NO: Proceed

## Security Declaration

This installation will:
- CREATE directory: `$HOME/.claude/skills/dsh-worker-review/`
- CREATE file: `$HOME/.claude/skills/dsh-worker-review/SKILL.md`
- CREATE file: `$HOME/.claude/skills/dsh-worker-review/references/setup.md`
- CREATE file: `$HOME/.claude/skills/dsh-worker-review/scripts/run_worker.py`
- MODIFY: Nothing. No existing files will be changed.

## Installation Steps

### Step 1: Run install script

Run the following command to download and execute the installer:

```bash
curl -fsSL "https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/dsh-worker-review/install.sh" | bash
```

This script will:
- Create `$HOME/.claude/skills/dsh-worker-review/` directory
- Download all skill files from GitHub
- Verify the installation


### Ensure skills directory is registered

Read `$HOME/.claude/settings.json`. Check if the `"skills"` array contains
a path that covers `$HOME/.claude/skills/`. If not, add `"$HOME/.claude/skills"`
to the array.

### Verify installation

Read `$HOME/.claude/skills/dsh-worker-review/SKILL.md` and confirm:
- YAML frontmatter has valid `name` and `description` fields
- File content is not empty or corrupted

### Report to user

Tell the user:
"dsh-worker-review installed successfully!
- Location: ~/.claude/skills/dsh-worker-review/
- Trigger: Run a bounded coding or PR implementation through local DeepSeek Harness in the exact workspace selected by the reviewin
- To uninstall: delete the ~/.claude/skills/dsh-worker-review/ directory"

## Rollback

If ANY step fails:
1. Delete the `$HOME/.claude/skills/dsh-worker-review/` directory if it was created
2. Tell the user exactly which step failed and why
3. Do NOT leave partial installations behind
