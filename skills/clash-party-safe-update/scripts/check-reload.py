#!/usr/bin/env python3
"""Read-only, fail-closed screen. A pass is not authorization to reload."""
import argparse
import datetime as dt
import json
import sys

import yaml


PROTECTED = (
    "tun", "interface-name", "port", "socks-port", "mixed-port", "redir-port",
    "tproxy-port", "ipv6", "bind-address", "allow-lan", "mode",
)


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError("Duplicate YAML key")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def check(snapshot, candidate, now=None):
    if not isinstance(snapshot, dict) or not isinstance(candidate, dict):
        return ["invalid-document"]
    blocked = []
    now = now or dt.datetime.now(dt.timezone.utc)
    try:
        observed = dt.datetime.fromisoformat(snapshot["observedAt"].replace("Z", "+00:00"))
        if observed.tzinfo is None or not 0 <= (now - observed).total_seconds() <= 120:
            blocked.append("stale-or-invalid-snapshot")
    except (KeyError, TypeError, ValueError, AttributeError):
        blocked.append("stale-or-invalid-snapshot")
    if snapshot.get("schemaVersion") != 1:
        blocked.append("snapshot-schema")
    runtime = snapshot.get("config")
    if not isinstance(runtime, dict):
        return blocked + ["runtime-config"]
    if not isinstance(runtime.get("tun"), dict) or not isinstance(candidate.get("tun"), dict):
        blocked.append("tun:missing-or-invalid")
    elif type(runtime["tun"].get("enable")) is not bool or type(candidate["tun"].get("enable")) is not bool:
        blocked.append("tun.enable:missing-or-invalid")
    for key in PROTECTED:
        if key not in runtime and key not in candidate:
            continue
        if key not in runtime or key not in candidate:
            blocked.append(key + ":unproven-default")
        elif json.dumps(runtime[key], sort_keys=True) != json.dumps(candidate[key], sort_keys=True):
            blocked.append(key + ":changed")
    if isinstance(runtime.get("tun"), dict) and runtime["tun"].get("enable"):
        interface = snapshot.get("physicalInterface")
        if not isinstance(interface, dict) or interface.get("forwarding") != "Disabled":
            blocked.append("physical-ipv4-forwarding:unknown-or-enabled")
        elif interface.get("status") != "Up" or interface.get("name") != runtime.get("interface-name"):
            blocked.append("physical-interface:unverified")
    if snapshot.get("warnings"):
        blocked.append("snapshot-warnings")
    return blocked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args()
    try:
        with open(args.runtime, encoding="utf-8-sig") as source:
            snapshot = json.load(source)
        with open(args.candidate, encoding="utf-8-sig") as source:
            candidate = yaml.load(source, Loader=UniqueLoader)
        blocked = check(snapshot, candidate)
    except (OSError, ValueError, TypeError, yaml.YAMLError, RecursionError):
        print("BLOCK: input unavailable or invalid; raw content withheld", file=sys.stderr)
        return 2
    if blocked:
        print("BLOCK: " + ", ".join(blocked), file=sys.stderr)
        return 1
    print("PASS: compared fields only. Separately verify DNS, listeners, credentials, profile caches, and authorization. No reload performed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
