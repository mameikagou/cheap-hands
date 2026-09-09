---
name: route-openmemory
description: Route, classify, store, query, import, deduplicate, and migrate personal OpenMemory records across three canonical projects and five memory sectors. Use whenever the user asks to remember, save, import, recall, search, reinforce, delete, or reorganize OpenMemory content, or when an agent is about to persist agent-development, workplace-learning, or investment-learning context.
---

# Route OpenMemory

Use exactly three project IDs:

| Main line | Canonical `project_id` | Content |
|---|---|---|
| Agent development | `agent-development` | Agent architecture, orchestration, evals, prompts, skills, MCP, coding agents, reusable AI engineering methods |
| Work capability | `work-capability` | Workplace context, MT/LD, performance, communication, project ownership, status reporting, career development |
| Investment learning | `investment-learning` | Trading, investing, quant research, factors, backtests, books, papers, market observations |

Never create an ad-hoc project ID. Retired aliases include `brain-work`, `meituan-career`, `meituan_career`, `agent_dev`, and `investment`; never write new memories to them.

## Route before writing

1. Honor an explicit main line named by the user.
2. Otherwise route by the memory's primary purpose.
3. Split mixed content:
   - Job-specific AI project coordination goes to `work-capability`.
   - Reusable Agent implementation knowledge goes to `agent-development`.
   - Agent tooling used to obtain trading or factor conclusions goes to `investment-learning`; reusable tooling itself goes to `agent-development`.
4. Ask only when the primary purpose genuinely cannot be inferred.

## Choose the memory sector

Treat the OpenMemory sector separately from `project_id`. Put an explicit sector only in `metadata.sector`; never put it in the top-level storage `type` field.

The writing agent must classify every contextual memory from its meaning and conversation context before calling OpenMemory. Do not delegate sector selection to OpenMemory's regex classifier.

Honor a sector explicitly named by the user. Otherwise choose the best-supported primary sector:

- `episodic`: a specific event, meeting, dated progress update, or account of what happened;
- `semantic`: a stable fact, definition, concept, or reference statement;
- `procedural`: a reusable method, workflow, checklist, instruction, or how-to;
- `emotional`: a feeling, reaction, like, dislike, or preference whose emotional content is the point;
- `reflective`: a lesson, review, insight, interpretation, evaluation, or conclusion drawn from experience.

Always pass the chosen primary sector as `metadata.sector`. If two or more sectors materially apply, split the source into coherent memories when that preserves the original meaning. Otherwise choose the dominant primary sector and optionally preserve the remaining model judgments in `metadata.model_secondary_sectors`. Do not omit `metadata.sector` to make OpenMemory guess, and do not ask the user merely to resolve internal classification uncertainty.

Classify from the full meaning, not from a weak keyword match. OpenMemory currently indexes only the explicit primary sector; `metadata.model_secondary_sectors` is provenance, not an indexed additional sector.

## Preserve the source

Default to primary-source storage:

- Store the user's wording or the source excerpt, not an assistant summary.
- Do not turn speculation into a fact.
- Keep one coherent idea per memory.
- Keep each Chinese chunk near 80–250 characters. Split longer material at paragraph or sentence boundaries.
- Do not silently omit profanity, uncertainty, dates, or qualifications.

Use contextual project storage by default. Attach:

```json
{
  "source_type": "codex_conversation_raw | claude_conversation_raw | brain_file_raw | screenshot_transcription",
  "source_path": "when available",
  "source_date": "YYYY-MM-DD when known",
  "verbatim": true,
  "raw_text": "exact original chunk",
  "canonical_project": "one of the three canonical IDs",
  "chunk_index": 1,
  "chunk_total": 1
}
```

Use tags for retrieval, not to replace the original text.

If the user explicitly asks to save an interpretation or summary, label it:

```json
{
  "verbatim": false,
  "derived": true,
  "source_memory_ids": ["..."],
  "canonical_project": "..."
}
```

Never present derived text as the user's original statement.

## Write workflow

1. Query the canonical project using a distinctive sentence from the source.
2. Fetch plausible matches and compare `metadata.raw_text` or full content.
3. If an exact match exists, reinforce it instead of creating a duplicate.
4. Store with the canonical project ID, source metadata, and the model-chosen `metadata.sector`.
5. Fetch the returned ID and verify:
   - `metadata.raw_text` equals the original chunk;
   - `metadata.canonical_project` is correct;
   - `primary_sector` equals the requested sector when `metadata.sector` was set;
   - content is not empty or truncated.
6. If content is empty or truncated, delete that new memory, split the source into smaller chunks, and retry.

Do not claim success before verification.

## Query workflow

1. Search the most relevant canonical project first.
2. Treat project filters defensively: global or unrelated results may still appear.
3. Fetch candidate IDs and require matching `metadata.canonical_project`.
4. Search a second main line only when the request crosses domains.
5. Prefer `metadata.raw_text` when the user asks what they originally said.
6. Clearly label any later interpretation as interpretation.

## Migration workflow

OpenMemory may deduplicate identical content across project IDs. Therefore, copying first and deleting later can leave the memory attached to the old project.

For each memory in a retired project:

1. Fetch and retain its full content, tags, user ID, and metadata.
2. Delete the exact old ID.
3. Store it under the canonical project with:
   - preserved `raw_text`;
   - `migrated_from_project`;
   - `migrated_from_id`;
   - `migrated_at`;
   - `canonical_project`.
4. Fetch and verify the new memory.
5. If storage or verification fails, immediately restore the old memory to its original project.

Delete only exact IDs already captured for migration. Never bulk-delete a project using an unverified search result.

## Canonical examples

- “记录一下 MT、LD、绩效和项目推进” → `work-capability`
- “保存 Agent eval、轨迹诊断和 tool orchestration 方法” → `agent-development`
- “导入交易书、因子论文、回测结论和交易复盘” → `investment-learning`
- “美团 AI 项目的汇报与分工” → `work-capability`
- “从美团项目抽出的通用 Agent 评测框架” → `agent-development`

## Tool fallback

Use the OpenMemory MCP query, get, store-project, reinforce, and delete tools. If they are unavailable, report the missing capability; do not imitate persistence by writing to an unrelated project or silently creating a local substitute.
