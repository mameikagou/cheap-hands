# Auto-Install Instructions for AI Agents

> YOU ARE AN AI AGENT. These instructions are for you, not for a human.
> The user has asked you to install the "sanity" skill.
> Follow each step in order. Do not skip steps. Do not ask for confirmation
> unless a step explicitly says to.

## Pre-flight Checks

1. Verify you have file write access to the user's home directory
2. Check if `$HOME/.claude/skills/sanity/` already exists
   - If YES: Ask the user "Skill 'sanity' already installed. Overwrite? (y/n)"
   - If NO: Proceed

## Security Declaration

This installation will:
- CREATE directory: `$HOME/.claude/skills/sanity/`
- CREATE file: `$HOME/.claude/skills/sanity/SKILL.md`
- CREATE file: `$HOME/.claude/skills/sanity/agents/openai.yaml`
- MODIFY: Nothing. No existing files will be changed.

## Installation Steps

### Step 1: Run install script

Run the following command to download and execute the installer:

```bash
curl -fsSL "https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/sanity/install.sh" | bash
```

This script will:
- Create `$HOME/.claude/skills/sanity/` directory
- Download all skill files from GitHub
- Verify the installation


### Ensure skills directory is registered

Read `$HOME/.claude/settings.json`. Check if the `"skills"` array contains
a path that covers `$HOME/.claude/skills/`. If not, add `"$HOME/.claude/skills"`
to the array.

### Verify installation

Read `$HOME/.claude/skills/sanity/SKILL.md` and confirm:
- YAML frontmatter has valid `name` and `description` fields
- File content is not empty or corrupted

### Report to user

Tell the user:
"sanity installed successfully!
- Location: ~/.claude/skills/sanity/
- Trigger: 对量化点子、研究计划与系统主线做有证据的常识审查与裁决：核对已冻结合同、检索 Brain/书籍/论文/知识库与可靠网络资料、判定致命问题（未来数据、样本外污染、不可成交、决定被账户层改写）、做 campaign 深度审计、守卫主线与系统熵增
- To uninstall: delete the ~/.claude/skills/sanity/ directory"

## Rollback

If ANY step fails:
1. Delete the `$HOME/.claude/skills/sanity/` directory if it was created
2. Tell the user exactly which step failed and why
3. Do NOT leave partial installations behind
