# Luna Worker Delegation Contract

Use every section that materially applies. Omit irrelevant details, but never omit the allowed boundary, protected work, minimal implementation rule, acceptance evidence, or main-agent intervention rule for repository tasks.

## Role and ownership

State that Luna is the primary executor for the assigned responsibility while the main agent remains an active technical owner. Say whether Luna may spawn subagents; default to no. Tell Luna that other people and agents may edit the same workspace.

Use this rule:

```text
You own implementation and verification for <responsibility/files>. The main agent owns direction, integration, critical fixes, and final acceptance. You are not alone in the repository. Never revert, overwrite, restage, or reformat changes you did not create. The main agent may patch the shared worktree; preserve those edits and continue around them.
```

## Outcome and current state

Include the exact user-visible or runtime outcome, repository and worktree paths, branch and base, relevant commits, dirty files, current processes or services, data coverage, already completed work, known test evidence, failed attempts, and the first unfinished requirement. Do not make Luna rediscover facts already verified by the main agent.

## Instructions to read

List exact repository instructions, plans, schemas, architecture contracts, and skills. Require complete reads before edits.

## Allowed change boundary

Name the files, directories, modules, and responsibilities Luna owns. Name the existing entrypoints and dependencies it must reuse, any allowed new files, permitted runtime write roots, and whether it may create commits. Prefer exact paths over broad phrases.

## Protected boundary

List unrelated dirty files, other worktrees, user and parent changes, protected planning, canonical data, promoted results, credentials, ports, and services. Name destructive commands that are forbidden or require approval. Name architectural surfaces that are forbidden, including new top-level packages, CLI roots, databases, registries, compatibility layers, one-off scripts, duplicate pipelines, and unrelated refactors.

## Minimal implementation rule

Include:

```text
Modify the existing live path first. Implement the smallest complete change that fixes the observed path. Do not generalize for hypothetical future providers, formats, markets, or modes. Do not add a framework, manager, adapter hierarchy, compatibility path, config layer, helper package, report system, or unrelated refactor unless you first prove the current path cannot satisfy the requirement. Before adding a new surface, report the verified gap, reader, owner, lifecycle, replacement target, and smallest acceptance test.
```

Name the approved framework or engine when one exists and forbid alternatives. Do not let validation, hashes, documentation, or safety scaffolding become the main deliverable.

## Execution sequence

Give an ordered, outcome-driven sequence. Each step must end in evidence, not only an edit. Include safe recovery for interrupted operations. For data work, distinguish probe, raw ingestion, canonical build, inventory refresh, and consumer validation. For code work, distinguish focused reproduction, smallest fix, targeted tests, and integration verification.

## Acceptance evidence

Specify exact tests, live commands, expected behavior, data counts and date ranges, manifests, inventory, API responses, screenshots, git diff, status, commits, and architecture checks that apply. Mocks can prove code paths but cannot replace required real runtime or real data evidence.

## Stop and escalation rules

Require Luna to stop and report on destructive or irreversible work, missing permission or credential, paid services, repeated identical external failure, required changes outside its boundary, a new top-level architecture surface, conflict with protected edits, or an internally inconsistent objective. The report must include the exact command, error, attempts, preserved state, and smallest decision needed.

## Progress and handoff

At meaningful boundaries require Luna to report changed files, commands, real evidence, tests, commit, unresolved risks, and next action. Before committing a broad diff, it must show the diff and justify every new surface. Unless explicitly assigned, Luna reports to the main agent rather than messaging the end user.

## Main-agent intervention

Always include:

```text
The main agent will inspect the shared worktree while you run. If your implementation becomes over-designed, drifts from the approved path, or is materially low quality, the main agent may directly modify or replace the affected code and will tell you. Do not revert those edits. Continue around them, then take the next assigned implementation or verification task.
```

## Final deliverable

Require the achieved outcome or exact blocker, files and behavior changed, commits, tests and real runtime evidence, data or artifact lifecycle, confirmation that protected work is untouched, remaining risks and user decisions, and what the main agent must verify independently.
