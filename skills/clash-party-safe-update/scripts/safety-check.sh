#!/usr/bin/env bash
set -u

phase="${1:-check}"
multica_profile="${MULTICA_PROFILE:-desktop-api.multica.ai}"
multica_bin="${MULTICA_BIN:-${HOME}/.local/bin/multica-native-context}"
service_name="${MULTICA_SERVICE:-multica-desktop-api.service}"
failed=0

if [[ -z "${CLASH_PARTY_ROOT:-}" ]]; then
  printf 'FAIL set CLASH_PARTY_ROOT to the local mihomo-party data directory\n' >&2
  exit 1
fi
printf 'Clash/Multica read-only precheck: %s\n' "$phase"
if ! python3 - "${CLASH_PARTY_ROOT}/config.yaml" <<'PY'
import sys
try:
    import yaml
    with open(sys.argv[1], encoding="utf-8-sig") as source:
        config = yaml.safe_load(source)
    valid = (isinstance(config, dict)
             and config.get("useHotReloadProfile") is True
             and config.get("hotReloadProfileAutoCloseConnection") is False)
except Exception:
    valid = False
print("ok  reload preferences" if valid else "FAIL reload preferences unavailable or unsafe")
sys.exit(0 if valid else 1)
PY
then
  failed=1
fi
runtime_dir="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
if [[ -z "${DBUS_SESSION_BUS_ADDRESS:-}" && -O "$runtime_dir" && -S "$runtime_dir/bus" ]]; then
  export XDG_RUNTIME_DIR="$runtime_dir"
  export DBUS_SESSION_BUS_ADDRESS="unix:path=$runtime_dir/bus"
fi
if timeout 10 systemctl --user is-active --quiet "$service_name" 2>/dev/null; then
  printf 'ok  agent service active\n'
else
  printf 'FAIL agent service unavailable or inactive\n' >&2
  failed=1
fi
if timeout 10 "$multica_bin" daemon status --profile "$multica_profile" >/dev/null 2>&1; then
  printf 'ok  daemon status command succeeded (confirm connected state in fresh logs)\n'
else
  printf 'FAIL daemon status command failed; raw output withheld\n' >&2
  failed=1
fi
if curl --noproxy '*' -fsS --connect-timeout 5 --max-time 10 https://api.multica.ai/health >/dev/null 2>&1; then
  printf 'ok  agent API reachable over default/TUN path\n'
else
  printf 'FAIL agent API unreachable over default/TUN path\n' >&2
  failed=1
fi
printf 'This check does not authorize a reload or prove TUN continuity.\n'
exit "$failed"
