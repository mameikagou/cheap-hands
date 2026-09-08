---
name: clash-party-safe-update
description: Diagnose and repair Clash Party/Mihomo TUN failures or safely update routing on Windows/WSL while preserving active agent connections. Covers physical-interface forwarding, configuration precedence, guarded profile reloads, and local rollback. Not an application or core upgrade workflow.
---

# Clash Party Safe Update

Keep the user's working network and agent connection alive. A successful API
response or one reachable URL is not proof of a stable TUN.

## Boundaries

- Do not restart or kill Clash Party, Mihomo, TUN, WSL, or the Windows network
  stack; toggle TUN/system proxy; close all connections; switch cores; or
  change the existing proxy ports as a routine repair. Respect an explicit
  user prohibition across subsequent turns. General approval to fix the
  network does not override that prohibition.
- **Hot reload can disconnect the user.** Mihomo recreates TUN when effective
  TUN parameters differ. Never promise continuity from `useHotReloadProfile`
  alone. Compare live state, GUI-controlled configuration, and the proposed
  generated profile before any whole-profile PUT.
- Preserve subscriptions, credentials, controller secrets, and unrelated
  rules. Parse configuration structurally and print only selected fields.
  Do not print full profiles, full controller responses, or raw connection
  metadata. Keep machine snapshots and logs outside public repositories.
- Prefer a single justified correction. Do not accumulate hosts entries,
  fixed CDN IP routes, DNS providers, proxy processes, or restart watchdogs.
- A skill update does not authorize changes to the running network. Diagnosis
  helpers in this skill are read-only and never apply or schedule repairs.

## Diagnose First

1. Record wall time, core PID/start time, live TUN settings, selected physical
   adapter, forwarding state, current connectivity, and recent agent logs.
   On Windows, run `scripts/inspect-network.ps1`. From WSL, invoke it with
   Windows PowerShell and a Windows-accessible script path. Multiple controller
   pipes require explicit selection; do not choose the first one silently.
2. Check IPv4 `Forwarding` on the **actual bound physical interface** before
   blaming DNS or automatic interface detection. Correct `interface-name`
   plus `auto-detect-interface: false` does not prevent the demonstrated
   Windows forwarding/TUN interaction. Read
   [references/windows-tun.md](references/windows-tun.md) for this symptom.
3. Read only the active profile's identity and override list. In the reviewed
   Clash Party build, ordinary overrides are applied before GUI-controlled
   `mihomo.yaml`; therefore the GUI's TUN/DNS values can overwrite an override.
   Confirm precedence against the installed client when its version changes.
   `work/config.yaml` is generated output, not a durable source of truth.
4. Separate paths: Windows TUN, WSL TUN, explicit local proxy, physical egress,
   and DNS. Explicit proxy tests must clear `NO_PROXY` (`--noproxy ''`); a
   direct/TUN probe must ignore proxy environment variables (`--noproxy '*'`).
   An existing hosts/IP bypass does not test whether Clash DIRECT works.
5. A failed precheck blocks unrelated rule updates. For an already broken
   network, continue read-only diagnosis and prepare the authorized narrow
   recovery; do not require the broken health check to pass before repairing
   its verified cause.

Set `CLASH_PARTY_ROOT` to the local client data directory, then use
`bash scripts/safety-check.sh pre` for the local Multica checks. This
checks service/API health and reload preferences only; it does **not** prove
that a configuration reload is safe. Configure its paths through environment
variables. The shell checks require Python 3 with PyYAML, curl, timeout, and
systemctl; the inspector requires Windows PowerShell with NetTCPIP/NetAdapter.
Diagnose missing dependencies rather than declaring success.

## Apply Within the Authorized Scope

### Windows forwarding failure

When physical-interface IPv4 forwarding is enabled and core self-reentry is
observed, use the procedure in [references/windows-tun.md](references/windows-tun.md).
Record whether that adapter must route other devices, run a hotspot, or
provide VPN/subnet routing. Do not disable forwarding globally or alter
unrelated adapters, firewalls, WSL networking mode, or global registry keys.

The demonstrated repair changes only the selected adapter's IPv4 forwarding
in `ActiveStore`, without profile reload or process restart. A separately
running Windows-local rollback must be ready **before** the change. Persist
the tested value only after Windows and WSL checks pass. Recheck the adapter
identity instead of hardcoding an old interface index.

### Rule or subscription update

1. Require `useHotReloadProfile: true` and
   `hotReloadProfileAutoCloseConnection: false`. Do not change proxy selection
   or mode merely to test a rule; other auto-close preferences may apply.
2. Back up the named override being changed under the client's `backups/`
   directory. Keep persistent custom rules in `override/` and preserve
   first-match order (`+rules:` for prepending). Modify with `apply_patch`.
3. Generate and validate the candidate through the client's profile validation
   path; the reviewed build uses `mihomo -t -f candidate -d test-directory`.
   Validation checks syntax, not connectivity or TUN continuity.
4. Save a fresh read-only runtime snapshot locally. Run
   `python3 scripts/check-reload.py --runtime snapshot.json --candidate candidate.yaml`.
   It conservatively blocks protected-field changes and unproven defaults;
   it never applies the candidate. An unknown is not a pass. Do not rewrite
   the candidate merely to silence the guard.
   This is a necessary screen, not a complete proof: DNS (including fake-IP
   range), listeners, authentication, and controller settings are not exposed
   by this snapshot and must be checked separately against the actual running
   generation. Omitted versus explicit defaults conservatively block.
5. Whole-profile reload is allowed only after protected-state equivalence
   is established and existing user authorization permits it. GUI/profile
   caches must be accounted for. If TUN reconstruction is needed, prepare
   a concrete local recovery and maintenance action for user approval; do
   not silently perform it under the name of hot reload.
6. Revert only this operation's edits on failure. A rollback reload needs the
   same protected-state check; blindly reloading an old profile can also
   reconstruct TUN. For an unchanged-profile diagnostic reload there is no
   file edit to roll back: do not reload it repeatedly.

## Verify and Report

- Test both Windows and WSL: a domestic DIRECT destination, a foreign proxied
  destination, the affected API, and agent-control health. Check expected
  HTTP status and TLS success. An unauthenticated API 401 may prove reachability,
  but does not prove a model call succeeded.
- Compare core PID/start time, TUN/interface state, new core self-connections,
  and CPU growth. Do not close old sockets simply to make the counters clean.
- Read recent Multica daemon logs and verify task-wakeup WebSocket recovery.
  An old failed connection can time out after the repair: identify it,
  observe a successful new connection, and start the observation window from
  that recovery. Repeated new errors mean the repair is not stable.
- Check timestamps **inside** log records, not just file modification time.
  Capped/rewritten logs observed during this incident retained stale records.
  Zero matching new errors in stale logs is not evidence of health; use fresh
  controller snapshots and live probes and report missing log coverage.
- Record exact changes, persistence, baseline/rollback location, test results,
  any reconnect, and observation duration. Distinguish short-term recovery
  from long-term reliability. Never claim zero-disconnection guarantees.

For prevention, configuration ownership, optional monitoring, and separate
WSL resource failures, read
[references/stability-plan.md](references/stability-plan.md). Do not install
a scheduler or an automatic repair loop merely because this skill is loaded.
