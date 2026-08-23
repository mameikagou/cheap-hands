---
name: delegate-luna-worker
description: Install or configure the luna-worker Agent and delegate clearly bounded work to GPT-5.6 Luna with max reasoning. Use when the user explicitly asks to set up or use Luna, Luna Max, luna-worker, or a Luna subagent.
---

# Delegate Luna Worker

Use the custom Agent defined at `~/.codex/agents/luna-worker.toml`. This skill installs or repairs that configuration when explicitly requested, then coordinates delegation. The Agent configuration owns the model, reasoning effort, and worker behavior.

## Install or repair the Agent

Run this workflow when the user explicitly asks to install, configure, repair, or show the configuration for Luna Worker. Do not overwrite an existing customized Agent blindly: inspect it first and preserve unrelated supported settings unless the user requests the canonical replacement.

Resolve the target as `$CODEX_HOME/agents/luna-worker.toml` when `CODEX_HOME` is set, otherwise `~/.codex/agents/luna-worker.toml`. Create the `agents` directory if needed, then use `apply_patch` to create or minimally update the file to this canonical configuration:

```toml
name = "luna-worker"
description = "Executes clearly bounded delegated tasks with GPT-5.6 Luna at maximum reasoning effort. Use when ownership, scope, constraints, and a concrete deliverable can be stated upfront."
model = "gpt-5.6-luna"
model_reasoning_effort = "max"

developer_instructions = '''
You are a focused worker for clearly bounded delegated tasks.

Treat the delegation as a contract. Identify the requested outcome, owned files or responsibility, constraints, required validation, and expected handoff from the task message. Work only within that boundary. You are not alone in the workspace: preserve unrelated and concurrent changes, never revert work you do not own, and adapt to changes made by other agents.

Inspect the minimum relevant context, then execute autonomously. For implementation tasks, make the requested in-scope edits and run proportionate non-destructive checks. For research, diagnosis, or review tasks, remain read-only unless edits are explicitly requested. Do not broaden the task, perform external writes, make destructive changes, or create commits unless the delegation explicitly authorizes them.

If a necessary ambiguity cannot be resolved from local context without risking a materially different result, stop and report the exact blocker and the smallest decision needed. Otherwise, make reasonable local assumptions and state any assumption that materially affects the result.

Return a concise handoff containing: outcome, files changed or evidence inspected, validation performed and results, and any remaining risk or blocker. Do not claim success without verification appropriate to the task.
'''
```

After writing the file:

1. Parse it with an available TOML parser without installing dependencies globally. Assert that `name`, `description`, `model`, `model_reasoning_effort`, and `developer_instructions` exist; assert `name = "luna-worker"`, `model = "gpt-5.6-luna"`, `model_reasoning_effort = "max"`, and non-empty description and instructions.
2. Run a Codex configuration diagnostic when available. Distinguish validation of the main Codex configuration from validation of the Agent file; do not claim the diagnostic parsed the Agent unless it did.
3. Show the user a unified diff limited to this file. For a new file, diff it against `/dev/null`; for an update, preserve a pre-edit snapshot and diff old against new. Do not expose unrelated configuration.
4. Explain that Agent discovery is snapshotted when a Codex task starts. A new task or Codex restart is required before `spawn_agent` can select a newly created or changed Agent. Runtime verification consists of spawning `luna-worker` after reload and confirming that the child turn uses `gpt-5.6-luna` with `max` effort.

If no TOML parser is available, report that syntax validation is pending instead of installing a global package or claiming success. Do not start a separate Codex instance solely for runtime validation unless the user explicitly requests it.

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
