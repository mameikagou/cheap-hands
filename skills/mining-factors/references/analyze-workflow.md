# Analyze factor-research workflow

Use this reference only after reading the applicable repository `AGENTS.md` files. The live CLI help is authoritative; inspect it before writing a command because planned interfaces have changed in the past.

## Working directory and environment

Run Python project commands from:

```bash
cd /home/admin/mrlonely-code/analyze/apps/quant-qlib
```

Use `uv run`. Do not print database connection strings, create a SQLite fallback, or start a second registry. In the native owner environment, use the same trusted PostgreSQL configuration as the production backend through the repository's established environment path.

## Data inventory

Inspect the available interface:

```bash
uv run qrant-qlib data inventory --help
uv run qrant-qlib data inventory status --json
```

Request only fields relevant to the proposed factor and always state the scope:

```bash
uv run qrant-qlib data inventory context \
  --scope <scope_id> \
  --fields <comma-separated-fields> \
  --universe <universe_id> \
  --json
```

Use `--symbols` instead of `--universe` for an explicit list. Validate the frozen structured requirement before factor registration or execution:

```bash
uv run qrant-qlib data inventory validate \
  --requirement <requirement.json> \
  --json
```

Refresh only when the inventory status says the snapshot is missing, dirty, stale, or failed:

```bash
uv run qrant-qlib data inventory refresh --force --json
```

Do not browse Parquet paths as a substitute for the inventory contract. Do not lower thresholds or fetch replacement data at factor runtime.

## Unified research entrypoint

The current official surface is:

```bash
uv run qrant-qlib research --help
uv run qrant-qlib research --market <a_share|us|crypto> <command> --help
```

Current lifecycle commands include `create`, `lock-contract`, `candidate-add`, `candidate-result`, `validation-lock`, `validation-reveal`, `register`, `run`, `evaluate`, `status`, `promote`, `reject`, and `cleanup`. Use the help for the selected command rather than copying a planned historical command.

The research run supports only the approved engine identifiers exposed by the CLI. Choose the engine from repository rules and the task layer:

- A-share research and formal portfolio evaluation: Qlib.
- Crypto research portfolio evaluation: VectorBT Pro with `engine=vectorbtpro` and `RESEARCH_ONLY` provenance.
- Approved formal crypto or U.S. execution validation: NautilusTrader with `engine=nautilus`.

Never use community `vectorbt`, a handwritten portfolio return, or an external shadow account.

## Protected-sample readiness

Before `validation-lock` or `validation-reveal`, verify:

- the mining process cannot query validation or final rows with its current identity;
- progress and product read paths do not expose protected metrics;
- PostgreSQL reveal counts are zero;
- candidate IDs, directions, transforms, model or weights, universe, labels, costs, rules, code hash, and data snapshot are frozen;
- the reveal is atomic and cannot be repeated or overwritten.

The existing lifecycle command is not by itself proof of machine isolation. Require an access-denied test using the same identity as the mining process. If protected data was already seen, record contamination rather than resetting a campaign ID.

## Mainline verification

Trace:

```text
inventory/data lake -> qrant-qlib research -> PostgreSQL -> public target_weights
-> approved engine -> PostgreSQL API -> existing frontend
```

Check the scoped diff and tests for a second CLI, registry, database, artifact root, backtester, account, fee ledger, runtime download, or page that scans files for state. Preserve historical planning and failures while removing replaced active paths.

## Minimum dry runs

Before a full campaign, exercise the live provider and selected engine on bounded data that covers:

- expression parsing and finite output;
- point-in-time availability and future-reference rejection;
- sparse late starts and empty results;
- cross-year partitions and terminal calendar boundaries;
- missing required execution price with no fallback;
- `HOLD`, `HOLD_COST`, and `BLOCKED` decisions producing zero orders;
- unchanged membership producing no hidden equal-weight rebalancing;
- resource peak and failure cleanup.

These checks validate the implementation. They do not count as factor evidence.
