# Question Patterns for Codebase Learning

This reference provides concrete question templates organized by learning goal.
Use these patterns to maintain Socratic dialogue that builds understanding.

## The Six Socratic Categories (Adapted for Code)

### 1. Clarification Questions
**Purpose**: Ensure shared understanding of terms and concepts

```
"What do you mean when you say 'the service handles auth'?
 Can you point to where that happens?"

"When you say 'it validates,' what specifically is being checked?"

"You mentioned 'the cache invalidates'—walk me through the trigger."
```

### 2. Assumption-Probing Questions
**Purpose**: Surface hidden beliefs that may be incorrect

```
"What are you assuming about the input format here?"

"You expect this to be called with a user object—is that documented
 anywhere, or inferred?"

"What would happen if your assumption about thread safety is wrong?"
```

### 3. Evidence Questions
**Purpose**: Demand reasoning based on what's actually in the code

```
"What in the code makes you think this is thread-safe?"

"Where do you see evidence that this function is pure?"

"Show me the line that handles the error case you mentioned."
```

### 4. Viewpoint Questions
**Purpose**: Introduce alternative perspectives and approaches

```
"Another developer might use events here instead of direct calls—
 why do you think polling was chosen?"

"In the other service, they used a factory pattern. Why not here?"

"What would a security reviewer say about this approach?"
```

### 5. Implication Questions
**Purpose**: Explore consequences and downstream effects

```
"If we changed this to async, what downstream code would break?"

"What happens to dependent services if this throws?"

"If this cache TTL doubles, what's the user-visible impact?"
```

### 6. Meta Questions
**Purpose**: Encourage reflection on the learning process itself

```
"Why is understanding this particular function important for your goal?"

"What would you need to know to feel confident modifying this?"

"How does this connect to what you learned about middleware?"
```

---

## Code-Specific Question Patterns

### Prediction Questions
**Use when**: Before showing code behavior

```
BEFORE SHOWING CODE:
"Looking at just the function name `calculateShippingCost` and its
 parameters `(order, destination)`, what do you think it returns?"

BEFORE TRACING EXECUTION:
"For input [3, 1, 4, 1, 5], what output do you predict?"

BEFORE REVEALING DESIGN:
"Given this is in the `handlers/` directory, what role do you
 expect this class to play in the architecture?"
```

### Trace Questions
**Use when**: Walking through execution step-by-step

```
"What's the value of `count` after the second loop iteration?"

"This promise chain has three `.then()` calls. What's the value
 passed into the second one?"

"The request hits this middleware first. Walk me through what
 happens before it reaches the controller."

"Line 45 throws if validation fails. Trace what catches it."
```

### Design Reasoning Questions
**Use when**: Understanding architectural choices

```
"Why do you think this was extracted into a separate service
 rather than kept in the controller?"

"This could have been a simple function, but it's a class with
 dependency injection. What problem does that solve?"

"The team chose eventual consistency here. What would strict
 consistency cost them?"

"Why is this interface so narrow when the implementation
 supports more?"
```

### Comparison Questions
**Use when**: Distinguishing similar concepts

```
"How would behavior change if we used `map` instead of `forEach`
 on line 23?"

"This service uses callbacks, but the new one uses async/await.
 What's the practical difference for error handling?"

"Compare this validation approach to the one in UserService.
 Which is more maintainable, and why?"
```

### Error Prediction Questions
**Use when**: Anticipating edge cases and failure modes

```
"What happens if `user` is null at line 67?"

"This API call has no timeout. What failure mode does that create?"

"The retry logic runs 3 times. What if the error is a validation
 error that will always fail?"

"Where would you add a try-catch if this fetch fails?"
```

### Historical Reasoning Questions
**Use when**: Understanding why code evolved this way

```
"Looking at git blame, this was rewritten 6 months ago. What
 problem do you think the old version had?"

"This TODO has been here for 2 years. Why might it never get done?"

"The PR that added this mentions 'performance.' What was slow before?"
```

---

## Graduated Hint Templates

### Level 1: Conceptual Hint
```
"Not quite—remember that [relevant concept]. How does that change
 your answer?"

"Think about what happens when [condition]. Does that affect the
 return value?"

"You're on the right track with [correct part], but consider
 [missing aspect]."
```

### Level 2: Narrowed Options
```
"Is it (a) [option], (b) [option], or (c) [option]?
 Look at line [N] for a clue."

"The answer involves either [X] or [Y]. Which one handles
 [specific case]?"

"It's one of these patterns: [list]. The method name gives it away."
```

### Level 3: Fill-in-the-Blank
```
"The function returns the _____ of all elements. The word is in
 the docstring on line 12."

"This middleware runs _____ the route handler. The order is set
 in server.ts line 18."

"The error gets caught by _____ because of [hint about scope/chain]."
```

---

## Question Sequences by Learning Goal

### Goal: Understand a New Module

1. "What does the folder name suggest about its responsibility?"
2. "Looking at the exports in index.ts, what's the public API?"
3. "Pick one export—what do you predict it does?"
4. [Show code] "Were you right? What surprised you?"
5. "How does this connect to other modules you've seen?"

### Goal: Understand Data Flow

1. "Where does this data originate? (User input? Database? External API?)"
2. "Trace it through the first transformation. What changes?"
3. "What validation happens along the way?"
4. "Where is it persisted or sent out?"
5. "What would break if [middle step] failed?"

### Goal: Understand a Bug

1. "Before looking at the fix, what do you think causes this?"
2. "Where would you add a console.log to verify?"
3. [After they hypothesize] "Let's check. Read [relevant lines]."
4. "Now that you see the actual cause, how would you fix it?"
5. "How would you prevent this class of bug in the future?"

### Goal: Prepare for Contributing

1. "What patterns do existing contributions follow?"
2. "Where would you add a new [feature type]?"
3. "What tests would you write first?"
4. "What documentation needs updating?"
5. "Who would review this, based on git history?"

---

## Anti-Pattern Questions (Avoid These)

❌ "Does that make sense?"
   → Too vague, invites "yes" without verification

❌ "Any questions?"
   → Puts burden on learner to know what they don't know

❌ "Do you understand [X]?"
   → Binary answer doesn't reveal depth

✅ INSTEAD: "Explain [X] back to me in your own words."

✅ INSTEAD: "How would you apply [X] to [new situation]?"

✅ INSTEAD: "What's still fuzzy about [X]?"

## 面试题改编题库：Agent 项目（2026-08-10 pi-core 会话沉淀）

考教一体模式：一次一题，先让学生用自己的话答，再按答案补讲。题全部由真实面试题改编（字节抖音直播 Agent 开发面经等）。

### Q1. 预测题：agent loop 至少要管哪几件事？
- 问：agent-loop.ts（几百行），不翻代码先猜——一个 agent loop 在代码层面至少要管哪几件事？
- 考察点：loop 职责边界 vs 上下文组装边界（学生常答"查工具/查 skill/看记忆"——都对，但那是每轮开始前的准备，属于 harness 层）
- 答案要点：loop 本体 = 生成 → 判停 → 执行工具 → 结果回填 → 再生成；终止条件
- 教学衔接：答完接 Q2

### Q2. 追踪题：ReAct 循环在代码里的三连问
- 问：① 模型回复完之后，代码怎么知道下一步是"继续调模型"还是"去执行工具"？② 工具执行完，结果往哪放？放完接着干什么？③ 这个 while 什么时候停下来？至少说两个条件。
- 考察点：ReAct（思考→行动→观察）的代码形态；停止原因机制
- 答案要点：① 回复里的 toolCall 字段；② 结果塞回上下文消息列表，再调模型（内层循环 hasMoreToolCalls）；③ 模型正常说干完（stopReason=agent_finished）/ 出错（error）/ 中断（aborted）/ 输出被 token 上限截断（length）
- 面试价值：length 截断时失败全部工具调用（不执行参数可能坏掉的调用）——"工程对模型输出的防御"，能讲出来是加分项

### Q3. 面试题改编：怎么保证 agent 不会无限循环？
- 问："你的 agent 会不会无限循环？怎么保证它会停下来？"
- 考察点：停止是模型驱动的，不是固定轮数
- 答案要点：① 模型每次回复带停止标记（正常/出错/截断）；② 工具可以自己声明"干完了就终止"（result.terminate，全部工具都声明终止则停）；③ 截断时失败全部工具调用；④ 外层循环只在用户补发新消息时接续，不空转
- 教学提示：先让学生答，答不全再补；强调"停止权在模型回复里，程序只是裁判"

## 犯错记录（2026-08-10 pi-core 会话，用户要求记录）

本用户（前端出身，求职 Agent 开发岗）的明确要求，违反即被打回：
- ❌ 代码细节抠题（"agent loop 至少要管哪几件事"）→ 用户："太细节了，要面试中能吹的"
- ❌ 一次甩多张话术卡 → 用户："塞这么多读集贸，看不懂"
- ❌ 当面试官反问用户开场题 → 用户："不是让你教我面试吗？"
- ✅ 正确模式：考教一体，一次一题，先教后考、考完补讲；题用面试题改编；内容要架构级、能吹的
