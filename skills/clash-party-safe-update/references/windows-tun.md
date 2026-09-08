# Windows TUN self-reentry

## Evidence and diagnosis

A September 2026 incident showed DIRECT/DNS connections attributed to the
Mihomo process returning through its own TUN. The correct physical adapter
was pinned and runtime automatic interface detection was already false.
IPv4 forwarding remained enabled on that physical adapter. Disabling only
its forwarding restored Windows and WSL traffic without restarting the core
or changing TUN configuration. This establishes a trigger on that machine;
it does not establish which Windows component originally enabled forwarding.

The upstream issue contains an independent controlled A/B/A reproduction:
[Mihomo issue 3186](https://github.com/MetaCubeX/mihomo/issues/3186).
The interaction can occur despite explicit physical-interface binding. Do not
reproduce it by re-enabling forwarding on the user's working full-route TUN.

Read-only Windows inspection:

```powershell
Get-NetIPInterface -AddressFamily IPv4 |
  Select-Object InterfaceAlias,InterfaceIndex,Forwarding,WeakHostSend,WeakHostReceive
Get-NetAdapter | Select-Object Name,ifIndex,Status,HardwareInterface,InterfaceGuid
```

Determine the selected physical adapter from the live core configuration and
the actual default route. Names and indices can change after reconnects or
Wi-Fi/Ethernet switches. Identify the adapter by its current GUID and verify
name/index immediately before any change.

## Narrow recovery transaction

Only after the user's repair request covers the operation:

1. Save the physical adapter identity, active and persistent forwarding
   settings, core PID/start time, TUN state, and connectivity baseline in a
   private local directory. Some `PersistentStore` CIM queries return an
   object with no `Forwarding` property: null is unknown, not Disabled. Use
   `netsh interface ipv4 show interface interface="ADAPTER NAME" store=persistent`
   to inspect it when necessary. Do not invent a previous persistent value
   from the active value; record inheritance/absence explicitly.
2. Assess legitimate forwarding users. SharedAccess running alone does not
   prove it enabled forwarding or can be disabled safely. Preserve virtual
   adapters, WSL, container networking, firewall policy, and VPN routes.
3. Prepare and syntax-check a Windows-local transaction and a separate
   rollback process. The rollback must work without WSL, DNS, or the agent.
   It must target the saved adapter identity, have a deadline, log errors,
   acknowledge readiness, and restore only the modified setting if no commit
   arrives. Keep the original snapshot immutable and refuse accidental reuse.
4. Test readiness before changing anything. A failed watchdog startup must
   prevent mutation. Snapshot/read failures must leave networking unchanged.
5. Change only the selected physical adapter in ActiveStore:

   ```powershell
   Set-NetIPInterface -InterfaceIndex $verifiedPhysicalIndex -AddressFamily IPv4 `
     -Forwarding Disabled -PolicyStore ActiveStore
   ```

6. Test Windows TUN and explicit proxy, WSL TUN and explicit proxy, domestic
   and foreign destinations, and the agent-control API. Preserve an existing
   control connection where possible; capture before/after PID and start time.
   Inspect *new* core self-connections and CPU growth. A timeout/error in a
   probe must be handled as a failed probe, not lost as a PowerShell native
   stderr exception. Do not use a network-dependent commit timer.
7. Persist to `PersistentStore` only after all required probes pass. Read
   back active and persistent state before writing the verified commit marker.
   If persistence fails, keep rollback armed. Verify watchdog/controller exit.
8. Keep the rollback script and evidence. Restoring forwarding can restore
   the original failure, so it is a deliberate recovery option, not an
   unattended periodic action.

The operator must complete any required Windows elevation prompt. Never
automate security prompts or repurpose unrelated privileged scheduled tasks.

## Configuration precedence and reload hazard

In the installed Clash Party build reviewed in this incident, generation was:

`subscription -> ordinary overrides -> rule overrides -> smart override -> GUI-controlled configuration -> work/config.yaml`

Thus a TUN setting in an ordinary YAML override was overwritten by the
GUI-controlled value. Do not try to make `work/config.yaml` the source of truth
or repeatedly edit it to fight the generator. GUI changes also interact with
in-memory caches; editing a control file on disk does not prove the application
has adopted it.

[Mihomo v1.19.24 listener implementation](https://github.com/MetaCubeX/mihomo/blob/v1.19.24/listener/listener.go)
returns without recreating TUN only when effective TUN configurations compare
equal. Changed settings lead to closing the existing listener before creating
the next one. An HTTP 204 from a whole-profile reload does not prove sockets
or the virtual adapter were preserved. Check the installed version rather
than assuming every newer version behaves identically.

## Authoritative references

- [Windows forwarding/TUN reproduction](https://github.com/MetaCubeX/mihomo/issues/3186)
- [Microsoft Set-NetIPInterface: forwarding and policy stores](https://learn.microsoft.com/en-us/powershell/module/nettcpip/set-netipinterface)
- [Mihomo TUN configuration](https://wiki.metacubex.one/en/config/inbound/tun/)
- [Mihomo listener lifecycle](https://github.com/MetaCubeX/mihomo/blob/v1.19.24/listener/listener.go)
