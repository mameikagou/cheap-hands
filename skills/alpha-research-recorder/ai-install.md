# Auto-Install Instructions for AI Agents

> YOU ARE AN AI AGENT. These instructions are for you, not for a human.
> The user has asked you to install the "alpha-research-recorder" skill.
> Follow each step in order. Do not skip steps. Do not ask for confirmation
> unless a step explicitly says to.

## Pre-flight Checks

1. Verify you have file write access to the user's home directory
2. Check if `$HOME/.claude/skills/alpha-research-recorder/` already exists
   - If YES: Ask the user "Skill 'alpha-research-recorder' already installed. Overwrite? (y/n)"
   - If NO: Proceed

## Security Declaration

This installation will:
- CREATE directory: `$HOME/.claude/skills/alpha-research-recorder/`
- CREATE file: `$HOME/.claude/skills/alpha-research-recorder/SKILL.md`
- CREATE file: `$HOME/.claude/skills/alpha-research-recorder/templates/final_summary.md.template`
- CREATE file: `$HOME/.claude/skills/alpha-research-recorder/templates/round_NNNN.yml.template`
- CREATE file: `$HOME/.claude/skills/alpha-research-recorder/templates/session_metadata.yml.template`
- MODIFY: Nothing. No existing files will be changed.

## Installation Steps

### Step 1: Run install script

Run the following command to download and execute the installer:

```bash
curl -fsSL "https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/alpha-research-recorder/install.sh" | bash
```

This script will:
- Create `$HOME/.claude/skills/alpha-research-recorder/` directory
- Download all skill files from GitHub
- Verify the installation


### Ensure skills directory is registered

Read `$HOME/.claude/settings.json`. Check if the `"skills"` array contains
a path that covers `$HOME/.claude/skills/`. If not, add `"$HOME/.claude/skills"`
to the array.

### Verify installation

Read `$HOME/.claude/skills/alpha-research-recorder/SKILL.md` and confirm:
- YAML frontmatter has valid `name` and `description` fields
- File content is not empty or corrupted

### Report to user

Tell the user:
"alpha-research-recorder installed successfully!
- Location: ~/.claude/skills/alpha-research-recorder/
- Trigger: |
- To uninstall: delete the ~/.claude/skills/alpha-research-recorder/ directory"

## Rollback

If ANY step fails:
1. Delete the `$HOME/.claude/skills/alpha-research-recorder/` directory if it was created
2. Tell the user exactly which step failed and why
3. Do NOT leave partial installations behind
