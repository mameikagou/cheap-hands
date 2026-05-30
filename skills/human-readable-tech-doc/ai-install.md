# Auto-Install Instructions for AI Agents

> YOU ARE AN AI AGENT. These instructions are for you, not for a human.
> The user has asked you to install the "human-readable-tech-doc" skill.
> Follow each step in order. Do not skip steps. Do not ask for confirmation
> unless a step explicitly says to.

## Pre-flight Checks

1. Verify you have file write access to the user's home directory
2. Check if `$HOME/.claude/skills/human-readable-tech-doc/` already exists
   - If YES: Ask the user "Skill 'human-readable-tech-doc' already installed. Overwrite? (y/n)"
   - If NO: Proceed

## Security Declaration

This installation will:
- CREATE directory: `$HOME/.claude/skills/human-readable-tech-doc/`
- CREATE directory: `$HOME/.claude/skills/human-readable-tech-doc/references/`
- CREATE file: `$HOME/.claude/skills/human-readable-tech-doc/SKILL.md`
- CREATE file: `$HOME/.claude/skills/human-readable-tech-doc/references/patterns.md`
- CREATE file: `$HOME/.claude/skills/human-readable-tech-doc/references/diataxis-cheatsheet.md`
- MODIFY: Nothing. No existing files will be changed.

## Installation Steps

### Step 1: Create skill directory

Run: `mkdir -p $HOME/.claude/skills/human-readable-tech-doc/references`

### Step 2: Write SKILL.md

Write the following content to `$HOME/.claude/skills/human-readable-tech-doc/SKILL.md`:

```
---
name: human-readable-tech-doc
description: Generate human-readable technical documentation that helps readers quickly understand code core logic and system architecture. Use when asked to write, generate, or improve technical documentation including code comments, architecture docs, README files, API docs, design docs, code walkthroughs, system overviews, or any technical writing where human comprehension is the priority. Also use when reviewing or refactoring existing documentation to make it clearer.
---

# Human-Readable Technical Documentation

Write technical documentation that humans can read and understand quickly. Focus on clarity over completeness, structure over decoration.

## Core Principles

1. **Human-first**: Write for the reader, not the machine. Every sentence must earn its place.
2. **Structure before content**: Decide the document type and information architecture before writing.
3. **Macro before micro**: Start with the big picture (why and what), then drill into details (how).
4. **Show, don't just tell**: Use diagrams, examples, and analogies. Code speaks louder than words.
5. **Concrete over abstract**: Replace vague descriptions with specific examples. "The function retries failed requests up to 3 times with exponential backoff" not "Implements robust error handling mechanism."

## Determine Document Type (Diátaxis Compass)

Before writing, identify which type of document the reader needs. Ask: what is the reader trying to do?

| Reader's Goal | Document Type | Key Question Answered |
|---|---|---|
| Learn something new | **Tutorial** | "How do I learn this?" |
| Get something done | **How-to Guide** | "How do I solve this problem?" |
| Understand why/how it works | **Explanation** | "Why is it designed this way?" |
| Look up facts | **Reference** | "What is the API signature?" |

**One document, one purpose.** Never mix tutorial with reference, or how-to with explanation. If content serves multiple goals, split into separate documents and cross-link them.

## Code Documentation Workflow

When documenting code (functions, classes, modules), follow this workflow:

### Step 1: Answer Three Questions First

Before writing any code comment or doc, answer:

1. **What does this code do?** — One sentence, human language, no jargon.
2. **Why does it exist?** — What problem does it solve? Why this approach?
3. **How do I use it?** — Minimal working example.

If you cannot answer all three clearly, the code may need refactoring before documenting.

### Step 2: Write the "Why" Comment

Every non-trivial code block needs a "why" comment at the top explaining the intent:

```python
# Why: Batch process user records to generate monthly billing reports.
# Trade-off: Uses streaming to handle files larger than available memory.
# Called by: BillingService.generate_monthly_report()
def process_billing_records(input_file, output_file):
    ...
```

Rules for code comments:
- Comment the **why**, not the **what** (the code shows what)
- Explain **trade-offs** and **design decisions**
- Note **callers** and **side effects** when non-obvious
- Keep comments within 80 characters per line
- Update comments when code changes — stale comments are worse than none

### Step 3: Write the "How" Documentation

For modules and services, provide a quick-start guide:

```markdown
## Quick Start

```python
from billing import BillingService

# Initialize with default config
service = BillingService()

# Generate report for current month
report = service.generate_monthly_report(
    month="2024-01",
    output_path="/reports/january.csv"
)
```

**Core Logic**: The service streams records from the database in batches of 1000,
transforms each record through the pricing pipeline, and writes aggregated
results to CSV. See [Architecture](#architecture) for the data flow diagram.
```

### Step 4: Add the Architecture Context

Always connect the code to the bigger system. Use a C4-style diagram description:

```markdown
## Where This Fits

```
[User] --requests report--> [Billing API]
[Billing API] --streams records--> [Database]
[Billing API] --writes CSV--> [File Storage]
[File Storage] --notifies--> [User Email]
```

This module implements the [Billing API] box above. It handles steps 2-3 of
the data flow: database streaming and CSV generation.
```

## Architecture Documentation Workflow

When documenting system architecture, use the C4 Model approach:

### Level 1: System Context (1 sentence per box)

Who uses the system? What external systems does it interact with?

```
[User] --> [Our System] --> [Payment Gateway]
                     --> [Email Service]
                     --> [Analytics Platform]
```

Write one line per arrow describing the interaction. Keep it under 50 words total.

### Level 2: Container Diagram (the "what runs where")

What are the deployable units? Web app? API? Database? Message queue?

```
[Web App : React] --API calls--> [API Server : FastAPI]
[API Server] --reads/writes--> [Database : PostgreSQL]
[API Server] --publishes events--> [Message Queue : Redis]
[Worker : Celery] --consumes from--> [Message Queue]
[Worker] --writes to--> [File Storage : S3]
```

Label each box with: Name : Technology. Add one sentence describing each box's responsibility.

### Level 3: Component Diagram (only when needed)

Break down complex containers into components. Only create this if the container has internal complexity that needs explaining.

### Level 4: Code (skip unless critical)

Only document code-level details for the most complex or critical algorithms. Link to the code instead of duplicating it.

### Architecture Decision Records (ADRs)

For each significant decision, write a one-page ADR:

```markdown
# ADR-003: Choose Redis over RabbitMQ for message queue

## Context
We need a message queue for async task processing. Expected volume: 10K messages/day.

## Decision
Use Redis (List/Stream) instead of RabbitMQ.

## Why
- Team already uses Redis for caching — one less service to operate
- Message volume is low; Redis Streams is sufficient
- Simpler deployment (no additional infrastructure)

## Trade-offs
- **Con**: No persistent messaging — messages lost on Redis restart
- **Mitigation**: Tasks are idempotent; can be re-triggered manually

## Status
Accepted (2024-01-15)
```

## Language and Style Rules

1. **Active voice, present tense**: "The function validates input" not "Input is validated by the function"
2. **Short sentences**: Under 25 words. Break long sentences into two.
3. **One idea per paragraph**: If you need "additionally" or "furthermore", start a new paragraph.
4. **Define acronyms on first use**: "Content Delivery Network (CDN)"
5. **Use "you" for the reader**: "You can configure this by..."
6. **Code in backticks**: `function_name`, never "function_name" or 'function_name'
7. **Avoid**: "simply", "just", "obviously", "easily" — these make readers feel stupid

## The Golden Checklist

Before delivering any document, verify:

- [ ] Can a new team member understand the core logic in 2 minutes?
- [ ] Does the document answer "why" before "how"?
- [ ] Are all diagrams described in text (for accessibility)?
- [ ] Is there a runnable example (for code docs)?
- [ ] Would the document still make sense if read on a phone screen?
- [ ] Have I removed every sentence that doesn't add new information?

## References

- **Detailed patterns and examples**: See [references/patterns.md](references/patterns.md) for complete document templates, before/after examples, and common anti-patterns.
- **Diátaxis quick reference**: See [references/diataxis-cheatsheet.md](references/diataxis-cheatsheet.md) for the four document types with decision flowchart.
```

### Step 3: Download reference files

Run these commands to download the reference files:

```bash
curl -fsSL "https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/human-readable-tech-doc/references/patterns.md" -o "$HOME/.claude/skills/human-readable-tech-doc/references/patterns.md"
curl -fsSL "https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/human-readable-tech-doc/references/diataxis-cheatsheet.md" -o "$HOME/.claude/skills/human-readable-tech-doc/references/diataxis-cheatsheet.md"
```

### Step 4: Verify installation

Check that all files exist:
- `$HOME/.claude/skills/human-readable-tech-doc/SKILL.md`
- `$HOME/.claude/skills/human-readable-tech-doc/references/patterns.md`
- `$HOME/.claude/skills/human-readable-tech-doc/references/diataxis-cheatsheet.md`

Confirm the SKILL.md file starts with `---` (valid YAML frontmatter).

### Step 5: Report success

Tell the user: "Skill 'human-readable-tech-doc' installed successfully to ~/.claude/skills/human-readable-tech-doc/"
