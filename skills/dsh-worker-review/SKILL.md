---
name: dsh-worker-review
description: Run a bounded coding or PR implementation through local DeepSeek Harness in the exact workspace selected by the reviewing agent, then review its diff and tests. Use when the user asks DSH, Ox Alpha, OpenRouter free models, or cheap external coding models to write code under Sol, Codex, or Claude review.
metadata:
  version: 0.1.0
  author: mrlonely
  category: coding-workflow
---

# DSH Worker Review

Keep the current reviewing agent responsible for task scope, acceptance criteria, review, and the final workspace change. Treat DSH output as untrusted code from an external worker.

Prerequisites are Git, Python 3.11+, and an executable DeepSeek Harness CLI. Ori is optional for OpenRouter setup.

## Suitable work

Delegate implementations with a narrow file scope and observable acceptance criteria: tests, boilerplate, localized fixes, mechanical refactors, and independent small features. Keep security-sensitive changes, credentials, destructive migrations, production operations, and architectural decisions in the reviewing agent unless the user explicitly asks to delegate them.

Never send secrets, `.env` contents, production data, or credentials to the worker. DSH may read outside the workspace or use the network, depending on the local DSH configuration.

The caller owns workspace selection. Run DSH in the exact directory supplied by the reviewing agent. Never create, remove, switch, or prune a Git worktree; Sol, Codex, or the user may prepare one manually before invoking this skill.

## Workflow

1. Locate the exact Git workspace selected by the reviewing agent. For PR work, confirm it is the intended PR branch or user-prepared checkout. Do not substitute another checkout or create a worktree.
2. Run the preflight and inspect its JSON:

   ```bash
   python3 <skill-root>/scripts/run_worker.py preflight --workspace <workspace>
   ```

3. If `dsh` is missing, `model_present_in_catalog` is false, or `headless_openrouter_plugin_installed` is false, read [setup.md](references/setup.md). Ori is optional. Do not install software, open a login flow, or change the global DSH model without the user's authorization.
4. Write a task that includes the exact goal, allowed file scope, acceptance checks, and commands the worker should run. Do not delegate a task whose success cannot be reviewed from a diff and deterministic checks.
5. Run the worker:

   ```bash
   python3 <skill-root>/scripts/run_worker.py run \
     --workspace <workspace> \
     --model stealth/ox-alpha \
     --task <task>
   ```

   The runner records the Git state before and after DSH runs. A dirty workspace is allowed because the reviewing agent owns it, but existing and worker changes may be mixed in the final diff; prefer a clean workspace when attribution matters.
6. Open the returned `manifest.json`, `before-status.txt`, `after-status.txt`, `before.patch`, `after.patch`, `worker-output.txt`, and `worker-error.txt`. Review every changed file in the selected workspace. Run relevant tests yourself there; do not accept the worker's claimed test result without checking.
7. Accept or revise the in-place edits only after review. Never commit, merge, reset, revert, or clean the workspace automatically.
8. On rejection, provide one concrete critique and allow at most one retry unless the user asks for more. Preserve the first bundle for comparison.

## PR handoff

For PR work, this skill ends after the implementation has passed review and local validation. It never creates branches, commits, pushes, opens a PR, or changes PR state. The reviewing agent may perform those actions through the repository's normal GitHub workflow only when the user has authorized them.

## Review gate

Before accepting, check requirements, unintended files, generated or vendored artifacts, error handling, security impact, regression tests, and `git diff --check`. Report the worker model as requested and distinguish local catalog/plugin checks from cryptographic provider verification; DSH owns the active provider configuration.

The runner stores a temporary review bundle containing before/after evidence. It does not copy the repository or manage worktrees. Remove the bundle only after the user no longer needs that evidence and normal destructive-action checks have been satisfied.
