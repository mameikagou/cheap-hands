# Auto-Install Instructions for AI Agents

> YOU ARE AN AI AGENT. These instructions are for you, not for a human.
> The user has asked you to install the "sandbox-dev-environment" skill.
> Follow each step in order. Do not skip steps. Do not ask for confirmation
> unless a step explicitly says to.

## Pre-flight Checks

1. Verify you have file write access to the user's home directory
2. Check if `$HOME/.claude/skills/sandbox-dev-environment/` already exists
   - If YES: Ask the user "Skill 'sandbox-dev-environment' already installed. Overwrite? (y/n)"
   - If NO: Proceed

## Security Declaration

This installation will:
- CREATE directory: `$HOME/.claude/skills/sandbox-dev-environment/`
- CREATE file: `$HOME/.claude/skills/sandbox-dev-environment/SKILL.md`
- MODIFY: Nothing. No existing files will be changed.

## Installation Steps

### Step 1: Create skill directory

Run: `mkdir -p $HOME/.claude/skills/sandbox-dev-environment`

### Step 2: Write SKILL.md

Write the following content to `$HOME/.claude/skills/sandbox-dev-environment/SKILL.md`:

```
---
name: sandbox-dev-environment
description: Use the BotMux development environment correctly. Distinguishes native owner sessions from Podman guests, and covers the data lake, staging/publish flow, approved books, default review skills, and network diagnostics.
---

# BotMux Shared Development Environment

This skill describes the runtime contract supplied by BotMux. Treat the paths and
environment variables below as the authority for the current session; do not
guess a host path or create a second data/publish system.

## Runtime boundary

First read the host-decided mode. Do not infer authority from paths that happen
to exist:

```bash
printf 'mode=%s can_openmemory=%s\n' "$BOTMUX_EXECUTION_MODE" "$BOTMUX_CAN_OPENMEMORY"
```

When `BOTMUX_EXECUTION_MODE=native`, this is the computer owner's native WSL
session, not a guest sandbox. It may use the normal host workspace and may read
`/home/admin/mrlonely-code/brain`. When `BOTMUX_CAN_OPENMEMORY=1`, OpenMemory is
also allowed through the preconfigured `openmemory` MCP server or the
`route-openmemory` skill. Never search for or print the underlying OpenMemory
API key; BotMux supplies a session-scoped gate capability. Native mode does not
grant permission to copy owner material into a guest Pod or another user's
session.

The remaining container paths and restrictions in this skill apply when
`BOTMUX_EXECUTION_MODE=podman` (or when the mode marker is absent and the fixed
guest paths below are present).

Guest sessions run in a rootless Podman container. The container has one topic's
workspace, home, transcript state, outbox, staging area, and the selected
harness credential. A V4 guest user may reuse one user Pod for several topics,
but each topic still gets its own `/workspace`, `/home/dev`, `/session/outbox`,
and staging bind. Do not inspect sibling sessions, Pod metadata, Podman sockets,
or host process state.

The fixed paths are:

| Purpose | Path | Access |
| --- | --- | --- |
| topic workspace | `/workspace` (project at `/workspace/analyze`) | read/write |
| session home/state | `/home/dev` | read/write, private to this topic |
| relay outbox | `/session/outbox` | read/write, use the BotMux relay contract |
| canonical data lake | `/shared/quant-data` | read-only |
| current topic data staging | `/shared/quant-data/staging` | read/write only for this topic |
| approved investment books | `/knowledge/investment-books` | read-only |

`/workspace/analyze/apps/quant-qlib/data` is a symlink to
`/shared/quant-data`. The nested `data/staging` mount is the only writable
exception and points to this topic's private staging area. Do not remove the
symlink, write around it, or write directly into canonical/raw/marts/provider
directories.

The image contains the fixed CLI selected by the BotMux bot. Do not switch
harnesses by invoking another CLI binary. Credentials are injected only at the
child process boundary; never print, persist, or place keys in source, config,
outbox, artifacts, or commit history.

## Approved skills and knowledge

Every new instance receives these four read-only skill leaves from the host:

- `mainline-drift-audit`
- `sanity`
- `quant-ui-sync`
- `sandbox-dev-environment` (this skill)

The database freezes the skill list when a new topic is created. Existing topics
keep their original snapshot. The investment books are available only through
`/knowledge/investment-books`; Brain is not mounted and must not be searched by
path, symlink, archive, or alternate spelling.

OpenMemory is not available to guest sessions. Do not probe `8181`, discover a
host gateway, or attempt to reuse an owner memory configuration. An owner-only
memory capability, when explicitly present in a native/owner session, is not a
guest permission.

## Inspect before pulling data

Run commands from `/workspace/analyze` and use the existing qrant-qlib entrypoint:

```bash
cd /workspace/analyze
uv run qrant-qlib --help
uv run qrant-qlib data --help
uv run qrant-qlib data inventory status --json
uv run qrant-qlib data inventory context --scope <scope> --fields <field1,field2> --json
```

The inventory is the capability and coverage check. If a factor has a formal
requirement file, validate it before research:

```bash
uv run qrant-qlib data inventory validate --requirement /absolute/path/to/requirement.json --json
```

Do not silently call a provider from a factor or backtest module. If the
inventory is missing or stale, use its explicit refresh command and inspect the
result:

```bash
uv run qrant-qlib data inventory refresh --force --json
```

## Pull and refresh data

Use the registered data source CLI and check its help for the selected endpoint.
For Tushare, the supported lifecycle is dry-run, real backfill, coarse refresh,
status, and canonical build:

```bash
uv run qrant-qlib data tushare dry-run --endpoint <endpoint> --start <YYYYMMDD> --end <YYYYMMDD>
uv run qrant-qlib data tushare backfill --endpoint <endpoint> --start <YYYYMMDD> --end <YYYYMMDD> --resume
uv run qrant-qlib data tushare sync --endpoint <endpoint> --end <YYYYMMDD>
uv run qrant-qlib data tushare status --endpoint <endpoint>
uv run qrant-qlib data tushare build-canonical --endpoint <endpoint> --start <YYYYMMDD> --end <YYYYMMDD> --validate-only
```

Run the real backfill only after reviewing the dry-run window and provider
budget. `build-canonical` must pass its raw-manifest completeness checks before
writing canonical data. Other registered sources (AkShare, yfinance, Binance,
and the crypto data domains) are exposed under `qrant-qlib data --help`; use
their existing subcommands rather than writing a one-off downloader.

## Write staging and publish

Put candidate files under a request directory below the current session staging
root. The host injects the exact roots and envelope values; prefer these
variables over path guessing:

```bash
printf '%s\n' "$QRANT_SESSION_STAGING_ROOT" "$QRANT_SESSION_OUTBOX_DIR" "$QRANT_SESSION_HASH"
request_dir="$QRANT_SESSION_STAGING_ROOT/<request-id>"
mkdir -p "$request_dir/payload"
```

The request directory must contain `submission.toml` and data files under
`payload/`. Allowed payloads are Parquet/CSV/JSON/JSONL/NDJSON (and compressed
data accepted by the current publisher). Do not put Python, shell, notebooks,
pickle, binaries, symlinks, or executables in `payload/`. Declare the dataset
and requested partitions/base hashes in `submission.toml`; copy or transform
data into the private request directory before submitting.

Submit only through BotMux's filesystem-only relay command. It reads the
single-use turn capability from the current outbox; never invent a capability,
pass a secret on the command line, or connect to PostgreSQL from the container:

```bash
botmux data-publish submit \
  --dataset-id <dataset_id> \
  --staging-dir "$request_dir"
```

This invokes qrant-qlib's file-only publisher through the BotMux relay, writes
one immutable request to the session outbox, and computes the payload and base
hashes. The host watcher validates the session/owner/turn/capability, then
inserts a PostgreSQL `lake_publish_jobs` row. `LakePublisher` claims jobs
with a lease and `FOR UPDATE SKIP LOCKED`; a per-dataset advisory lock makes
same-dataset writers serial while different datasets can proceed in parallel.

Publication is optimistic-concurrency controlled. If the canonical partition
changed since the submitted base hash and the incoming result is not identical,
the job becomes `CONFLICT`; it never overwrites someone else's data. Inspect
the conflict, refresh/read the new canonical version, merge or regenerate your
request in a new staging directory, and resubmit. Do not edit an accepted
outbox request or retry by copying it into the central lake.

## Query the dashboard API

Guests receive no PostgreSQL DSN or database client authority. Query the same
read models used by the frontend through the fixed BotMux query shim instead.
It runs against the image's preloaded Python environment, so a cold workspace
does not create a virtualenv or download packages. The API origin is fixed to
the approved host-loopback address; do not replace it with the public
Cloudflare Access URL or probe other host ports.

```bash
botmux result-query health
botmux result-query catalog-stats
botmux result-query catalog-items --type strategy --market us --status active
botmux result-query catalog-strategy <strategy-id>
botmux result-query catalog-factors
botmux result-query backtests --market us --level all
botmux result-query backtest <run-id>
botmux result-query backtest-result <backtest-id>
botmux result-query factor-pool
botmux result-query workflow-tasks --status running
botmux result-query workflow-task <task-id>
botmux result-query research-assets
botmux result-query data-marketplace-datasets
```

The CLI performs GET requests only to named allow-listed routes, bounds timeout
and response size, and prints JSON. It does not accept an arbitrary URL or any
SQL. If a route or filter is missing, report the concrete requirement instead
of using a database credential, a direct PostgreSQL connection, or an ad hoc
HTTP call to a write endpoint.

## Publish research results

Factor, strategy, and backtest outputs are not visible in the dashboard merely
because files exist in a workspace. Put one result manifest and its declared
data artifacts in a fresh session staging child, then submit through BotMux's
single-use host relay:

```bash
request_dir="$QRANT_SESSION_STAGING_ROOT/<result-request-id>"
mkdir -p "$request_dir/payload"
# Write result.toml at $request_dir/result.toml and declared files below payload/.
botmux result-publish submit \
  --manifest "$request_dir/result.toml" \
  --staging-dir "$request_dir"
```

The manifest must use `version = 1` and
`kind = "research_result_publish_request"`, identify `strategy_id`,
`strategy_name`, `campaign_id`, `run_id`, `market`, `engine`,
`data_snapshot_hash`, `code_hash`, and `stage = "experimental"`, and declare
every artifact. Read the maintained example before producing a request:

```bash
sed -n '1,220p' /workspace/analyze/apps/quant-qlib/docs/result_publish.md
```

Only non-empty Parquet, CSV, JSON, JSONL, and NDJSON artifacts are accepted.
The relay snapshots the manifest and payload, rechecks session/owner/turn and
hash bindings on the host, copies data into the trusted research artifact root,
then atomically registers the campaign, strategy, run, artifacts, and backtest
in the existing ResearchRegistry. A missing experimental campaign is created
inside that transaction. A guest cannot claim `formal`; formal promotion needs
a separate trusted host approval.

## Network and Clash diagnostics

Guest networking uses rootless `pasta`; host network mode, published ports, and
an implicit gateway are not available. The current fixed Clash route is the
Windows Mihomo dedicated listener `127.0.0.1:17890`, selected as `USA-08`.
Podman maps that loopback listener with:

```text
--map-host-loopback,169.254.1.1
```

Inside the container, the corresponding proxy URLs are:

```text
HTTP_PROXY=http://169.254.1.1:17890
HTTPS_PROXY=http://169.254.1.1:17890
ALL_PROXY=socks5h://169.254.1.1:17890
```

`NO_PROXY` is injected alongside them. Use only the injected standard proxy
variables, including their lower-case spellings when a tool requires them.
Never substitute an implicit container gateway, hardcode another Clash port,
or copy Clash/Mihomo config, controller credentials, or the node list into a
guest. A missing proxy variable means the session's proxy capability was not
injected; report it instead of inventing a gateway.

Safe diagnostics do not print credentials:

```bash
env | grep -E '^(HTTP_PROXY|HTTPS_PROXY|ALL_PROXY|NO_PROXY)=' | sed -E 's#(https?://)[^/@]+@#\1<redacted>@#'
curl --fail --silent --show-error --max-time 10 -I https://pypi.org/simple/
curl --fail --silent --show-error --max-time 10 -I https://api.github.com/
```

Do not use `--noproxy '*'` for a normal request unless comparing direct versus
proxy behavior; that test deliberately bypasses a configured Clash route. Do
not probe host loopback, Podman APIs, or private services to find a usable
gateway.

## Non-negotiable boundaries

- Canonical/raw/marts/qlib-provider data is read-only in a guest.
- PostgreSQL credentials are never available in a guest. Read dashboard state
  through `qrant-qlib result query`; publish results through the BotMux relay.
- Writes go to the current topic's staging request and then the formal publish
  outbox; there is no direct merge command inside the container.
- In Podman guest mode, never access `/home/admin/mrlonely-code/brain`,
  OpenMemory, host `.codex`, host `.claude`, another principal's credentials,
  Podman sockets, or sibling topic directories. Native owner mode follows the
  explicit owner permissions above.
- Do not install arbitrary global tools, replace the fixed harness, or create a
  parallel downloader, queue, data lake, or backtest engine.
- If a path, dataset, proxy, or publish capability is missing, report the
  concrete error and stop at the boundary instead of bypassing it.

```


### Ensure skills directory is registered

Read `$HOME/.claude/settings.json`. Check if the `"skills"` array contains
a path that covers `$HOME/.claude/skills/`. If not, add `"$HOME/.claude/skills"`
to the array.

### Verify installation

Read `$HOME/.claude/skills/sandbox-dev-environment/SKILL.md` and confirm:
- YAML frontmatter has valid `name` and `description` fields
- File content is not empty or corrupted

### Report to user

Tell the user:
"sandbox-dev-environment installed successfully!
- Location: ~/.claude/skills/sandbox-dev-environment/
- Trigger: Use the BotMux development environment correctly. Distinguishes native owner sessions from Podman guests, and covers the
- To uninstall: delete the ~/.claude/skills/sandbox-dev-environment/ directory"

## Rollback

If ANY step fails:
1. Delete the `$HOME/.claude/skills/sandbox-dev-environment/` directory if it was created
2. Tell the user exactly which step failed and why
3. Do NOT leave partial installations behind
