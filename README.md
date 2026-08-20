# skill-forge

A collection of Claude Code skills. Install any skill by pasting one line into Claude Code.

## Install Skills

Copy any line below into your Claude Code conversation. Claude will fetch the instructions and install the skill automatically.

### suization（酥化）

Turns real project notes into strong, interview-ready technical chains, resume bullets, and deep-dive preparation without inventing ownership or metrics.

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/suization/ai-install.md and follow the instructions inside.
```

### sanity

Reviews quantitative research ideas and systems against the frozen business contract, local knowledge, prior results, and external evidence before implementation. It keeps weak-factor combination research permissive while guarding against leakage, fake breadth, and execution errors.

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/sanity/ai-install.md and follow the instructions inside.
```

### mainline-drift-audit

Audits plans and implementations for parallel systems, duplicated truth, directory-scanned state, unbounded artifacts, and database or data-lake bypasses.

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/mainline-drift-audit/ai-install.md and follow the instructions inside.
```

### sandbox-dev-environment

Uses the BotMux development environment correctly, distinguishing native owner sessions from Podman guests and covering the data lake, staging/publish flow, approved books, review skills, and network diagnostics.

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/sandbox-dev-environment/ai-install.md and follow the instructions inside.
```

### opencode-coder

Delegates code generation to cheap external models (MiniMax-M2.7, GPT-5.3-Codex) for 95% cost savings. Claude reads, dispatches, and reviews; the external model writes code.

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/opencode-coder/ai-install.md and follow the instructions inside.
```

### write-skill

Skill architect that helps you create new Claude Code skills conforming to Anthropic's spec. Extracts requirements through minimal interaction and outputs compliant SKILL.md files.

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/write-skill/ai-install.md and follow the instructions inside.
```

### skill-auto-installer

Packages any existing skill into a zero-friction auto-install bundle (ai-install.md). Supports GitHub Raw, npm, and local distribution channels.

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/skill-auto-installer/ai-install.md and follow the instructions inside.
```

### learn-codebase

Socratic codebase tutor that uses prediction, evidence-based questioning, active recall, and a learning journal to turn unfamiliar code into understanding you can defend in review or interviews. Based on [`ktaletsk/learn-codebase`](https://github.com/ktaletsk/learn-codebase).

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/learn-codebase/ai-install.md and follow the instructions inside.
```

### code-graph

Builds a local LSP code graph so Claude can efficiently read large codebases without traversing every source file. (Work in progress)

```
Fetch https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/code-graph/ai-install.md and follow the instructions inside.
```

## Install All Skills at Once

Paste this into Claude Code to install every skill in one go:

```
Fetch the following URLs one by one and follow the instructions inside each:
1. https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/suization/ai-install.md
2. https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/opencode-coder/ai-install.md
3. https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/write-skill/ai-install.md
4. https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/skill-auto-installer/ai-install.md
5. https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/code-graph/ai-install.md
6. https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/learn-codebase/ai-install.md
7. https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/mainline-drift-audit/ai-install.md
8. https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/sandbox-dev-environment/ai-install.md
```

## npm (opencode-coder only)

```
Run 'npx @skill-forge/opencode-coder init-skill' and follow the output.
```

## Uninstall

Delete the skill directory:

```bash
rm -rf ~/.claude/skills/{skill-name}
```
