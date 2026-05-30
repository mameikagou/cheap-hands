# Diátaxis Quick Reference

A practical guide to the four documentation types. Use this to decide what to write.

## The Decision Flowchart

```
                    What does the reader need?
                          |
          +---------------+---------------+
          |                               |
    Learning something?           Accomplishing something?
          |                               |
     TUTORIAL                    HOW-TO GUIDE
     (Learning-oriented)          (Goal-oriented)
          |                               |
          +---------------+---------------+
                          |
          +---------------+---------------+
          |                               |
    Understanding why?            Looking up facts?
          |                               |
     EXPLANATION                   REFERENCE
     (Understanding-oriented)      (Information-oriented)
```

## The Four Types at a Glance

| | Tutorial | How-to Guide | Explanation | Reference |
|---|---|---|---|---|
| **Question** | "How do I learn this?" | "How do I solve X?" | "Why does it work this way?" | "What is the Y?" |
| **Goal** | Acquire skill | Complete a task | Gain understanding | Find information |
| **Tone** | Friendly, encouraging | Direct, efficient | Thoughtful, discursive | Neutral, precise |
| **Structure** | Step-by-step sequence | Step-by-step for specific goal | Thematic, flexible | Structured, consistent |
| **Analogy** | Cooking lesson with a chef | Recipe card | Food science article | Ingredient encyclopedia |

## Tutorial

**Purpose**: Get a beginner from point A to point B. Teach through doing.

**Key Rules**:
- Assume the reader knows nothing about your tool
- Every step must be verifiable (reader can check they did it right)
- Never explain alternative approaches — one clear path only
- Always produce a meaningful result, not just "Hello World"
- Include expected output at key milestones

**Template Structure**:
```
1. Prerequisites (what to install first)
2. Goal statement (what you'll build)
3. Step 1: Setup (verify it works)
4. Step 2: First action (simple, clear)
5. Step 3: Add complexity (build on previous)
6. Step 4: Complete the task
7. Verify the result (how to check it worked)
8. Next steps (link to how-to guides for variations)
```

**Example Opening**:
> By the end of this tutorial, you will have a working web scraper that
> extracts product prices from any e-commerce page and saves them to CSV.
> You'll learn the basics of HTTP requests, HTML parsing, and data export.

**Never in a Tutorial**:
- Multiple ways to do the same thing
- Deep explanations of how things work internally
- Prerequisites that aren't essential
- Options, flags, or configuration choices

## How-to Guide

**Purpose**: Help someone who already knows the basics solve a specific problem.

**Key Rules**:
- Start with a clear problem statement
- Address a real-world goal, not a product feature
- Assume basic competence — skip "click File > Open"
- Include troubleshooting for the most common failure modes
- End with verification steps

**Template Structure**:
```
1. Problem: "You need to X because Y"
2. Prerequisites: what you need before starting
3. Solution overview (2-3 sentences)
4. Step-by-step instructions
5. Verification (how to confirm it worked)
6. Troubleshooting (2-3 common issues)
7. Related guides (links to similar problems)
```

**Good Title Pattern**: "How to [solve specific problem]"

Examples:
- "How to handle timeout errors in API calls"
- "How to migrate from MySQL 5.7 to 8.0 without downtime"
- "How to set up automated backups to S3"

**Bad Title Pattern**: "Using the [Feature]" or "[Feature] Guide"

**Never in a How-to Guide**:
- Teaching basic concepts
- Explaining how the feature works internally
- Covering multiple unrelated problems
- Reference-style lists of all options

## Explanation

**Purpose**: Deepen understanding. Explain the "why" behind design decisions.

**Key Rules**:
- Answer questions that start with "Why" or "How does...work"
- Make connections between concepts
- Provide historical context and trade-off analysis
- Use analogies to make abstract concepts concrete
- It's okay to be discursive — this is for reading, not following along

**Template Structure**:
```
1. The question or concept being explained
2. Context: why this matters
3. Core explanation (the "why")
4. How it relates to other parts of the system
5. Trade-offs and design decisions
6. Common misconceptions
7. Further reading
```

**Good Topics**:
- "Why we chose eventual consistency over strong consistency"
- "How the authentication flow works"
- "Understanding the caching strategy"
- "The reasoning behind our database schema"

**Good Analogy Pattern**:
> "Think of the message queue like a restaurant kitchen's order ticket system.
> Waiters (producers) write orders on tickets and place them on a rail.
> Cooks (consumers) pull tickets from the rail and prepare the food.
> If the kitchen gets busy, tickets pile up on the rail rather than
> overwhelming the cooks."

**Never in an Explanation**:
- Step-by-step instructions
- Lists of commands or API parameters
- "You should do X" advice
- Pure reference material without context

## Reference

**Purpose**: Provide accurate, complete, look-up information.

**Key Rules**:
- Be exhaustive and precise
- Use consistent formatting throughout
- Organize for scan-ability (tables, alphabetical, grouped)
- Include type information, defaults, constraints
- No explanations of why — just what

**Template Structure**:
```
1. Name/Signature
2. Description (one sentence)
3. Parameters/Arguments table
4. Return value
5. Exceptions/Errors
6. Examples (minimal, illustrative)
```

**Good Examples**:
- API endpoint documentation
- Configuration option lists
- CLI command reference
- Database schema definitions
- Error code lists

**Never in Reference**:
- Tutorial-style walkthroughs
- Explanations of design decisions
- "Getting started" content
- Subjective recommendations

## Cross-Linking Between Types

Always connect related documents:

```markdown
<!-- In a Tutorial, link to How-to Guides -->
Now that you understand the basics, see:
- [How to customize the output format](how-to-customize.md)
- [How to handle errors](how-to-handle-errors.md)

<!-- In a How-to Guide, link to Explanation and Reference -->
For details on why this approach works, see
[Understanding the caching strategy](explanation-caching.md).
For all available options, see the [API Reference](reference-api.md).

<!-- In Explanation, link to practical docs -->
To put this into practice, see the tutorial
[Getting started with X](tutorial-getting-started.md).

<!-- In Reference, link to explanatory context -->
For when to use this function vs. alternatives, see
[Choosing the right approach](explanation-approaches.md).
```

## Quick Checklist

Before publishing, verify your document:

**Tutorial Checklist**
- [ ] Every step produces a verifiable result
- [ ] No alternatives or choices offered
- [ ] Prerequisites are minimal and essential
- [ ] A beginner can follow without asking questions
- [ ] Links to relevant how-to guides at the end

**How-to Guide Checklist**
- [ ] Starts with a specific, real-world problem
- [ ] Steps are minimal (no unnecessary clicks)
- [ ] Includes troubleshooting for common failures
- [ ] Ends with verification steps
- [ ] Links to explanation docs for curious readers

**Explanation Checklist**
- [ ] Answers a "why" or "how does it work" question
- [ ] Makes connections to related concepts
- [ ] Includes trade-off analysis
- [ ] Uses at least one analogy or concrete example
- [ ] Doesn't contain step-by-step instructions

**Reference Checklist**
- [ ] Complete and accurate (every option listed)
- [ ] Consistent formatting throughout
- [ ] Organized for quick lookup
- [ ] Includes type information and constraints
- [ ] No tutorial or explanatory content mixed in
