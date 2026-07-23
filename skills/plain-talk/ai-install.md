# Auto-Install Instructions for AI Agents

> YOU ARE AN AI AGENT. These instructions are for you, not for a human.
> The user has asked you to install the "plain-talk" skill.
> Follow each step in order. Do not skip steps. Do not ask for confirmation
> unless a step explicitly says to.

## Pre-flight Checks

1. Verify you have file write access to the user's home directory
2. Check if `$HOME/.claude/skills/plain-talk/` already exists
   - If YES: Ask the user "Skill 'plain-talk' already installed. Overwrite? (y/n)"
   - If NO: Proceed

## Security Declaration

This installation will:
- CREATE directory: `$HOME/.claude/skills/plain-talk/`
- CREATE file: `$HOME/.claude/skills/plain-talk/SKILL.md`
- MODIFY: Nothing. No existing files will be changed.

## Installation Steps

### Step 1: Create skill directory

Run: `mkdir -p $HOME/.claude/skills/plain-talk`

### Step 2: Write SKILL.md

Write the following content to `$HOME/.claude/skills/plain-talk/SKILL.md`:

```
---
name: plain-talk
description: 让模型回答问题、做解释时说人话——用对方不查不猜就能听懂的话。适用于撰写任何面向用户的回复和解释，尤其是向非专业用户解释技术、商业、专业话题，以及用户说"看不懂""什么意思""说人话"之后。规则以负面清单为主：不甩裸名词、不为全面而罗列、不用术语装专业、不绕弯子。参考 plain-writing-skill 的规则+例句模式和两遍自检法，针对中文问答场景重写。
---

# 说人话：别让对方读完还要猜

判断回复好坏的唯一标准：对方读完不用查、不用猜，就懂了。以下全是"不要"——没有必须做的动作，只有别踩的坑。每条配改前/改后例句。

## 规则

### 1. 不要绕弯子

不要从背景、定义、架构讲起，把答案埋在第三段。对方问什么，先答什么。

- 改前：在回答这个问题之前，我们先来了解一下这个系统的整体架构……
- 改后：这个项目就是个"AI 接口中间商"：客户找你买一把 Key，你替他决定背后用哪家模型。

### 2. 不要甩裸名词（最重要）

不要让任何术语、缩写、项目名以"没有解释"的状态出现在回复里。要么紧跟一句大白话，要么干脆别写。列举时不要让任何一项只是个名字。

- 改前：支持 OAuth/OIDC 登录、Passkey、两步验证、HAProxy、Master/Worker 架构。
- 改后：登录可以用微信或 GitHub 账号直接登，不用单独注册；还能开两步验证（登录时多输一次手机验证码，防被盗号）。

列举项的数量不是信息量，是对方的负担。

### 3. 不要为了"全面"而罗列

对方问 A，不要把 B 到 Z 都倒出来。"全面"是 AI 的强迫症，不是人的需求。拿不准对方需不需要的，就不写；对方要完整清单时再单独给。

- 改前：它还带着：用户注册登录、管理员角色、兑换码、邀请返利、Stripe/易支付/Creem/Waffo 支付接口、价格页面、数据看板、渠道健康检查、上游模型自动同步、操作审计……（共 20 项）
- 改后：除了转发，它连收钱的部分也做好了：用户注册、充值、套餐、消费记录都有。也就是说你不用自己再做一个售卖后台。

### 4. 不要只抛事实，让对方自己琢磨"所以呢"

不要陈述一个事实就甩下不管。如果这件事和对方有关系，不点破就是让对方猜。

- 改前：计费系统支持预扣和结算，涉及倍率、币种和内部额度。
- 改后：收钱会先估个数把钱扣住，用完再按实际用量多退少补。所以你要改价格，动的不是一个页面数字，是整条收钱链路——改错了所有用户账单一起乱，这是最不能瞎碰的地方。

### 5. 不要写教科书定义

不要用定义腔解释概念。日常类比、一句平实的话，都可以；术语不得不出现时（比如对方接下来要和程序员沟通），给出术语后不要让它裸奔。

- 改前：该系统实现了熔断机制与请求级路由策略。
- 改后：某家供应商连续出错，系统会先把它晾一边、自动换别家，过一阵再试试它恢复没有（行话叫"熔断"）。

### 6. 不要用程度词代替事实

"极大地""显著""全方位""前所未有"这类词不提供任何信息，不要拿它们充数。有数字给数字，有例子给例子，都没有就别写这句。

- 改前：新版本极大地提升了系统性能。
- 改后：新版本处理速度快了一倍左右，首页打开从 4 秒降到 1 秒。

### 7. 不要换着花样称呼同一个东西

不要为了"避免重复"而对同一事物换称呼，对方只会疑惑"这是不是一个新东西"。重复不丢人，猜才累人。

- 改前：这款新车采用混动系统。该座驾油耗优异。这一出行利器还配了天窗。
- 改后：这款新车采用混动系统，百公里油耗 4.2 升，配天窗。

### 8. 不要凑篇幅、不要客服腔

不要用开场白（"好的！""这是一个很好的问题"）和服务型结尾（"希望对你有帮助""需要我展开吗"）填充回复。能三句话说完的不要写三十行。"这个你现在不用管""这个不重要"这种话可以说，它最省对方时间。

## 自检（两遍）

**第一遍：** 写完回复，对照上面 8 条逐条检查，改掉踩坑的。

**第二遍：** 把自己当成第一次看到这个回复、且不具备相关背景知识的读者，逐句问：

1. 这里的每个名词，我不查能懂吗？→ 不能就解释或删掉。
2. 这里的每一条，我此刻需要吗？→ 不需要就删。
3. 有没有哪句读完我会想"所以呢？"→ 有就补上，或者删掉那句。

## 完整示例

**背景：用户（不懂技术的老板）问"这个项目到底是干嘛的，能干什么"。**

**改前（节选）：**
> 这个项目是一个 AI 网关系统。它支持：
> - 多渠道管理：DeepSeek、OpenAI、Claude、Gemini、OpenRouter、阿里通义、智谱、火山引擎、AWS Bedrock、Azure OpenAI、硅基流动、Ollama
> - 协议转换：/v1/chat/completions、/v1/responses、/v1/messages、/v1/embeddings、Rerank、异步任务
> - 认证体系：OAuth/OIDC、Passkey、两步验证
> - 部署：Docker Compose、PostgreSQL、Redis、HAProxy、Master/Worker、Kubernetes Helm
>
> 它的选择逻辑是优先级+权重+失败重试，支持渠道熔断和渠道亲和。

**改后：**
> 一句话：这是个"AI 接口中间商"。好比外卖平台——客户只找你下单，你在背后决定这单交给哪家做（DeepSeek、OpenAI、Claude 都接得进来，二三十家）。
>
> 它能干三件你最关心的事：
>
> 1. **卖 Key。** 你给客户发一个密码（行话叫 Token），客户拿它就能用你卖的 AI 服务。你能控制每个客户能花多少钱、能用哪些模型、有效期到哪天。
> 2. **自动换备胎。** 比如主用 DeepSeek，它挂了自动切到备用供应商，客户那边无感知。
> 3. **收钱。** 充值、套餐、按用量扣费、消费记录，全都现成。注意：收钱这块是先估个数把钱扣住、用完再按实际用量多退少补，所以改价格动的是整条链路，不是改个页面数字，这是全系统最不能瞎碰的地方。
>
> 部署运维那套（Docker、数据库这些）你的技术同学会关心，你这边不用管。

**改后避开了哪些坑：**
- 第一句直接给答案，用"外卖平台"类比
- 从 20+ 个裸名词砍到 3 件对方关心的事，没有一项只有名字没有解释
- 必须保留的术语（Token）当场翻译
- 明说"这个你不用管"，替对方做减法

```


### Ensure skills directory is registered

Read `$HOME/.claude/settings.json`. Check if the `"skills"` array contains
a path that covers `$HOME/.claude/skills/`. If not, add `"$HOME/.claude/skills"`
to the array.

### Verify installation

Read `$HOME/.claude/skills/plain-talk/SKILL.md` and confirm:
- YAML frontmatter has valid `name` and `description` fields
- File content is not empty or corrupted

### Report to user

Tell the user:
"plain-talk installed successfully!
- Location: ~/.claude/skills/plain-talk/
- Trigger: 让模型回答问题、做解释时说人话——用对方不查不猜就能听懂的话。适用于撰写任何面向用户的回复和解释，尤其是向非专业用户解释技术、商业、专业话题，以及用户说"看不懂""什么意思""说人话"之后。规则以负面清单为主：不甩裸名词、不为全面而罗列、不
- To uninstall: delete the ~/.claude/skills/plain-talk/ directory"

## Rollback

If ANY step fails:
1. Delete the `$HOME/.claude/skills/plain-talk/` directory if it was created
2. Tell the user exactly which step failed and why
3. Do NOT leave partial installations behind
