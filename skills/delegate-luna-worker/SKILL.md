---
name: delegate-luna-worker
description: Delegate clearly bounded work to the configured luna-worker Agent running GPT-5.6 Luna with max reasoning. Use when the user explicitly asks Luna, Luna Max, luna-worker, or a Luna subagent to handle a task.
---

# Delegate Luna Worker

Use the custom Agent defined at `~/.codex/agents/luna-worker.toml`. This skill coordinates the delegation; the Agent configuration owns the model, reasoning effort, and worker behavior.

## Prepare the delegation

Delegate only when the user's request explicitly authorizes Luna or subagent work. Convert the requested work into a compact task contract containing:

- The concrete outcome and stopping condition.
- Owned files, modules, or read-only responsibility.
- Relevant constraints and out-of-scope boundaries.
- Required validation and expected handoff.
- A reminder that other agents may be editing the workspace and their changes must be preserved.

Resolve details from the current context when safe. Ask the user only if an unresolved choice would materially change the result or ownership boundary.

## Spawn the worker

Call `spawn_agent` with:

- `agent_type: "luna-worker"`
- `fork_turns: "none"`
- A short snake_case `task_name`
- The complete task contract in `message`

Do not pass a model or reasoning-effort override. Do not use a full-history fork with a custom Agent type; the runtime rejects that combination. Include every fact the worker needs in the message because it receives no conversation history.

If the runtime reports `unknown agent_type 'luna-worker'`, the current task's Agent registry is stale. Tell the user to start a new task or restart Codex so the newly installed Agent is loaded. Do not silently substitute a generic worker or a different model.

## Coordinate and verify

Continue independent local work while Luna runs when useful and conflict-free. Otherwise wait for its handoff, preferring a longer bounded wait over repeated polling.

Check the returned outcome, changed files or evidence, validation results, and remaining risks against the task contract. Use `followup_task` on the same Agent for a narrowly scoped correction when needed. Do not duplicate work already completed by the worker. Report that Luna was used and summarize the verified result; distinguish the worker's claims from validation performed by the orchestrator.
