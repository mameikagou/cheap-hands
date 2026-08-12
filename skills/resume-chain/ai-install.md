# Auto-Install Instructions for AI Agents

> YOU ARE AN AI AGENT. These instructions are for you, not for a human.
> The user has asked you to install the "resume-chain" skill.
> Follow each step in order. Do not skip steps. Do not ask for confirmation
> unless a step explicitly says to.

## Pre-flight Checks

1. Verify you have file write access to the user's home directory
2. Check if `$HOME/.claude/skills/resume-chain/` already exists
   - If YES: Ask the user "Skill 'resume-chain' already installed. Overwrite? (y/n)"
   - If NO: Proceed

## Security Declaration

This installation will:
- CREATE directory: `$HOME/.claude/skills/resume-chain/`
- CREATE file: `$HOME/.claude/skills/resume-chain/SKILL.md`
- MODIFY: Nothing. No existing files will be changed.

## Installation Steps

### Step 1: Create skill directory

Run: `mkdir -p $HOME/.claude/skills/resume-chain`

### Step 2: Write SKILL.md

Write the following content to `$HOME/.claude/skills/resume-chain/SKILL.md`:

```
---
name: resume-chain
description: 把零散的真实项目经历改写成强势、具体、可深挖的技术链路，并生成简历要点、项目详述和面试追问稿。用户要求包装项目、补技术链路、写项目经历、强化 owner 感、准备项目面试，或提供代码、文档、工作记录让 Codex 提炼项目叙事时使用。
---

# 链路简历

把项目写成一条请求如何进入系统、经过哪些处理、如何处理失败、最终产出什么的完整链路。目标是提高信息密度和责任感，不靠堆名词。

## 工作流

### 1. 盘点事实

先从用户材料、代码和文档中提取：

- 项目和团队背景
- 用户本人负责的模块、设计、代码与推进工作
- 输入、关键状态、处理步骤和输出
- 分支、失败、重试、降级、恢复等异常路径
- 可核验的结果和数字

信息不足时明确列出缺口。不要把猜测写成事实。

### 2. 划清归属

把素材分成三层，写作时不要混用：

1. **平台背景**：大项目解决什么问题、覆盖什么业务。
2. **团队成果**：团队或平台整体取得的规模和指标。
3. **个人贡献**：用户亲自设计、开发、推动或验证的内容。

可以用大项目名交代背景，但不要把团队成果改写成个人独立成果。若项目归属、Owner 身份或数字没有依据，标为“待核实”，不得补造。

### 3. 写技术链路

优先写成 5 至 8 个连续节点：

`触发/输入 → 识别或解析 → 决策/路由 → 核心处理 → 状态或数据流转 → 校验 → 输出`

按实际情况补三类细节：

- 1 至 3 个真实的内部对象名，例如入口、接口、任务类型、数据结构、核心函数或服务名。
- 至少一条异常路径，例如超时重试、失败降级、断点恢复、幂等或回滚。
- 一个关键取舍：原方案为何不够、为何选现在的方案、代价是什么。

不要只列技术栈。每个节点都要说明谁接收什么、做什么处理、把什么交给下一步。

### 4. 接入结果

按可信度使用结果：

- **本人实测**：可直接写，保留口径、时间范围和样本量。
- **平台或团队数据**：明确写成“平台覆盖”“团队结果”或“所在业务规模”。
- **合理估算**：只用于内部草稿，并标出计算方法；不得伪装成正式统计。
- **没有数据**：写功能变化、交付范围或故障减少的具体事实，不生成假数字。

避免“显著提升”“大幅优化”等空话。

### 5. 强化责任表达

根据证据选择动词：

- 独立决定核心方案并推进落地：`主导`
- 负责一个完整模块：`负责`
- 与他人共同完成：`参与设计并实现` 或 `协同推进`
- 只接入或使用平台：`接入`、`基于`、`支撑`

不要用“主导”“Owner”“核心作者”掩盖实际边界。责任范围越大，面试追问稿必须越完整。

## 默认交付物

除非用户只要求其中一种，否则依次输出：

1. **一句话定位**：项目背景 + 个人责任边界。
2. **简历版**：2 至 4 条，每条为“动作 + 技术链路 + 结果”。
3. **技术链路版**：把完整链路用箭头展开，并解释每一步。
4. **深挖准备**：列出架构取舍、最大故障、指标口径和重做方案。
5. **主张核验表**：每个强主张对应证据；缺证据的标红并给出补做办法。

## 写作模板

```text
[项目/模块名]｜[本人真实角色]

背景：[谁]在[什么场景]遇到[具体问题]。
责任：本人负责[明确边界]；[导师/团队]负责[评审、上下游或其他边界]。
链路：[输入] → [解析] → [路由/决策] → [核心处理] → [校验/异常处理] → [输出]。
取舍：旧方案[问题]；选择[方案]是因为[原因]，代价是[代价]。
结果：[个人实测结果]；平台背景为[团队规模，明确归属]。
```

## 禁止事项

- 不编造任职、项目归属、代码贡献、业务数字或第三方背书。
- 不把自写文档说成独立证据；可称“项目复盘”或“个人技术说明”。
- 不生成用于躲避背景调查或欺骗面试官的口径。
- 不用大段术语替代真实链路。

遇到材料不足时，仍然给出最强的可证实版本，并单列“要让这句话成立还需要补什么”。

```


### Ensure skills directory is registered

Read `$HOME/.claude/settings.json`. Check if the `"skills"` array contains
a path that covers `$HOME/.claude/skills/`. If not, add `"$HOME/.claude/skills"`
to the array.

### Verify installation

Read `$HOME/.claude/skills/resume-chain/SKILL.md` and confirm:
- YAML frontmatter has valid `name` and `description` fields
- File content is not empty or corrupted

### Report to user

Tell the user:
"resume-chain installed successfully!
- Location: ~/.claude/skills/resume-chain/
- Trigger: 把零散的真实项目经历改写成强势、具体、可深挖的技术链路，并生成简历要点、项目详述和面试追问稿。用户要求包装项目、补技术链路、写项目经历、强化 owner 感、准备项目面试，或提供代码、文档、工作记录让 Codex 提炼项目叙事时使用。
- To uninstall: delete the ~/.claude/skills/resume-chain/ directory"

## Rollback

If ANY step fails:
1. Delete the `$HOME/.claude/skills/resume-chain/` directory if it was created
2. Tell the user exactly which step failed and why
3. Do NOT leave partial installations behind
