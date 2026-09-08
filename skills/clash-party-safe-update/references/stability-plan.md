# Stability plan and incident lessons

## Keep the verified invariant

For the affected Windows client, keep IPv4 forwarding disabled on the physical
interface used by Mihomo, in both ActiveStore and PersistentStore. This is not
a blanket policy for routers: if the user needs hotspot/gateway/subnet routing,
design a separate network path and maintenance test rather than silently
re-enabling forwarding under the same full-route TUN.

Recheck after adapter changes, Windows updates, hotspot/Internet Connection
Sharing changes, VPN/subnet routing changes, and client configuration changes.
The original actor enabling forwarding was not identified from the available
logs. A service being present/running is not attribution. Do not disable
SharedAccess or change global routing/firewall settings based on that alone.

## One configuration owner

- GUI-controlled TUN/DNS fields belong to the client settings; custom domain
  rules belong to named persistent overrides. Generated work profiles are
  output. Maintain the intended effective values, not duplicate competing
  fragments. Never silently fix a harmless drift by applying a TUN change to
  an otherwise working network.
- Keep a verified baseline recording client/core version, adapter identity,
  protected effective settings, reload preferences, and last successful
  Windows/WSL checks. Baseline files stay local and exclude credentials.
- Gate routing changes with a fresh snapshot, candidate validation, protected
  configuration comparison, and reversible scope. Block overlapping writers
  when PID/config timestamps unexpectedly change; identify the actor before
  proceeding. Do not blame a user or another agent without evidence.
- Do not automatically upgrade, switch cores, or reset Windows/WSL networking
  to address a connection error. Such changes need a separate authorized task.
- Inspect subscription `autoUpdate` flags before blaming unattended refresh.
  They were disabled on the reviewed machine. An enabled application update
  check is not proof of installation or restart. Also inspect
  `autoCloseConnection`: node/mode changes can close connections even when
  the separate hot-reload auto-close preference is false. Do not change the
  node or mode to test reachability on the active control channel.

## Detection without restart loops

The included inspector is read-only. If the user separately requests continuous
monitoring, agree on schedule and notification destination before installing it.
Use bounded probes, non-overlapping runs, finite log retention, and deduplicated
notifications only on meaningful changes. Healthy/unchanged checks stay quiet.
Monitor physical forwarding drift, expected TUN state, new core self-reentry,
agent-control API reachability, and repeated WebSocket errors.

Do not implement a watchdog that repeatedly restarts Clash, toggles TUN, changes
nodes, flushes routes, or force-closes sockets on every timeout. A monitor
detects/alerts; an explicitly authorized local recovery transaction makes one
scoped change with independent rollback. A foreign site's HTTP 403 or API 401
is not automatically a network failure; use an endpoint-specific expectation.

If unattended recovery is later requested, scope it to the known adapter and
the proven forwarding drift, verify legitimate routing requirements, serialize
operations, rate-limit attempts, and stop after one failed recovery with a
local record requiring review. Do not turn temporary loss of Internet access
into repeated configuration mutations.

## Agent continuity and honest observation

Agent services should retain their existing bounded reconnect behavior.
When a connection created during the outage times out after repair, verify
the replacement connection and observe subsequent traffic. API success alone
does not establish that the task-wakeup WebSocket recovered. Do not restart
a running daemon merely to clear old errors from its log.

Track task-message, usage, and completion reporting separately from WebSocket
heartbeats. In this incident, heartbeats resumed but a task still logged
message/reporting timeouts and later exhausted completion retries. A healthy
heartbeat or `/health` endpoint must not hide that failure. Do not assume a
post-repair timeout is an old socket unless request timing proves it.

The reviewed daemon build skips HTTP heartbeat when WebSocket acknowledgments
are recent. Its idle HTTP connection cleanup is triggered by consecutive HTTP
heartbeat failures, so a healthy WebSocket alone cannot exercise that recovery
path. This is a recovery-coverage gap, not proof that stale sockets caused every
observed timeout. Completion retries are bounded; after exhaustion the reviewed
build leaves the task pending instead of retaining a durable retry queue.
The informational `task completed` log precedes the server callback.

The included `check-agent-log.py` checks message-report errors at DEBUG level,
keeps old terminal retry failures visible, and never calls a heartbeat-only
stream "healthy". Its four-MiB tail and inferred dates have explicit coverage
limits. Verify a pending task against server state; never fabricate or replay
its result merely to make a status indicator green. Any daemon transport or
durable-reporting implementation belongs in a separately scoped, tested
maintenance change, not an unannounced binary replacement during TUN repair.

If explicit local proxy checks succeed while default/TUN checks fail, record
DNS results and compare bounded IPv4/IPv6 and Windows/WSL probes. That narrows
the affected path; it does not prove a DNS or IPv6 root cause. Consider an
explicit existing proxy for the agent's supported transport configuration in
a separately authorized continuity change, with rollback and verification of
actual task reporting. Do not add another proxy or restart the daemon now.

Observe for several minutes after the last reconnect, with repeated low-cost
probes and stable process identities. Then validate across natural later events
(sleep/wake, Wi-Fi reconnect, network switch) when the user permits or those
events occur. Never induce those events on the only active control channel
just to increase test coverage. A short observation is not a lifetime guarantee.

## Separate resource exhaustion from networking

A distinct earlier incident involved concurrent Python/Qlib backtests exhausting
WSL RAM and swap, followed by kernel OOM kills affecting the agent backend and
system services. A routing repair does not protect against that failure.

For an authorized workload-hardening task, use measured concurrency limits,
bounded worker lifetimes, and cgroup/systemd memory limits on the research
workload. Reserve memory for WSL and control services. Derive limits from
current measurements and test them in an isolated workload; do not prescribe
universal RAM values or change WSL allocation/restart WSL during a network
repair. Confirm an OOM from kernel/service evidence before classifying a new
disconnection as memory pressure.

## Sanitized incident timeline: 2026-09-08 (UTC+08:00)

| Time | Evidence | What it establishes |
| --- | --- | --- |
| Before recovery | DIRECT and DNS connections attributed to the core re-entered TUN | Actual self-reentry, not merely a failed remote API |
| 20:50 | Client log recorded a non-admin startup, TUN auto-disable, and elevation restart | A restart happened; the initiating actor was not established |
| 20:54 | An agent performed whole-profile PUT and got 204 | The action was not proof of continuity; live/disk TUN settings differed during the investigation |
| 21:05-21:11 | Repeated agent network warnings and WebSocket failures | The network had not been repaired by the reload |
| 21:11:38 | Only physical-interface IPv4 forwarding was disabled | Windows/WSL connectivity immediately recovered; core PID stayed unchanged |
| 21:12:09 | Windows and WSL probes passed, then the setting was persisted | The narrow repair passed both platform checks |
| 21:13:22 | Agent task-wakeup WebSocket reconnected after an old connection timeout | Recovery of the control connection, with a finite reconnect interruption |
| 21:18 and 21:24 | One task's usage and completion reporting timed out despite ongoing heartbeats | Agent end-to-end reporting was not fully recovered; do not report complete stability |
| Later read-only checks | Default WSL health probe timed out once; explicit proxy and subsequent Windows/WSL IPv4 probes succeeded; no core self-connections in snapshot | A residual intermittent/path-specific issue remains unclassified, separate from the eliminated observed self-reentry |
| 21:32-21:34 | Fifteen consecutive health probes passed across Windows TUN, WSL TUN, and explicit proxy; new task messages were acknowledged | Current connectivity and new message reporting recovered without another restart; an earlier exhausted completion still needs server-state verification |
| Follow-up status read | The earlier task's authenticated status endpoint returned `cancelled` | Its pending completion must not be replayed; this is not proof that its original completion reached the server |

Important limits: the record supports the forwarding trigger and its successful
correction, not an exact attribution of every earlier dropout. Capped core logs
sometimes contained old record timestamps despite a recent modification time;
use fresh controller observations instead of treating an empty post-repair
log search as a clean bill of health.
