# Auto-Install Instructions for AI Agents

> YOU ARE AN AI AGENT. These instructions are for you, not for a human.
> The user has asked you to install the `mainline-drift-audit` skill.

## Pre-flight

1. Verify that `$HOME/.claude/skills/` is writable.
2. If `$HOME/.claude/skills/mainline-drift-audit/` already exists, ask before replacing it.

## Security declaration

The installer creates only:

- `$HOME/.claude/skills/mainline-drift-audit/SKILL.md`
- `$HOME/.claude/skills/mainline-drift-audit/agents/openai.yaml`
- `$HOME/.claude/skills/mainline-drift-audit/scripts/scan_repo.py`

It does not modify project repositories or user settings.

## Install

Run:

```bash
curl -fsSL https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/mainline-drift-audit/install.sh | bash
```

Then verify that `SKILL.md` is non-empty and its YAML frontmatter contains `name: mainline-drift-audit`.

If installation fails, delete the partial `$HOME/.claude/skills/mainline-drift-audit/` directory and report the failed step.
