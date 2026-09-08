#!/usr/bin/env python3
"""Summarize a bounded local daemon log tail without emitting task content."""
import argparse
import collections
import datetime as dt
import json
from pathlib import Path
import re
import sys


RECORD = re.compile(r"^(\d{2}:\d{2}:\d{2}\.\d+) (?:DBG|INF|WRN|ERR) (.*?) component=daemon(?: |$)")
FAILURES = {
    "failed to report task messages": "messageReport",
    "report task usage failed": "usageReport",
    "complete task failed after retries; leaving task in running rather than falling back to fail": "completionReport",
    "heartbeat failed": "httpHeartbeat",
}


def summarize(lines, now, window_seconds=300):
    cutoff = now - dt.timedelta(seconds=window_seconds)
    counts = collections.Counter()
    last_event = None
    last_message_success = None
    terminal_failures = 0
    day = now.date()
    previous = now
    future = False
    # The daemon's text format omits dates. Infer midnight crossings backwards
    # within the bounded tail, anchored to the file's last-write date by caller.
    for line in reversed(lines):
        match = RECORD.match(line)
        if not match:
            continue
        try:
            clock = dt.time.fromisoformat(match[1])
        except ValueError:
            continue
        event = dt.datetime.combine(day, clock, tzinfo=now.tzinfo)
        if event - previous > dt.timedelta(hours=12):
            day -= dt.timedelta(days=1)
            event -= dt.timedelta(days=1)
        previous = event
        if event > now + dt.timedelta(seconds=5):
            future = True
            continue
        last_event = max(last_event, event) if last_event else event
        message = match[2]
        if message == "reported task messages":
            last_message_success = max(last_message_success, event) if last_message_success else event
        if FAILURES.get(message) == "completionReport":
            terminal_failures += 1
        if cutoff <= event <= now and message in FAILURES:
            counts[FAILURES[message]] += 1
    return {
        "lastRecordAt": last_event.isoformat() if last_event else None,
        "recordStreamFresh": bool(last_event and 0 <= (now - last_event).total_seconds() <= 120 and not future),
        "recentFailures": dict(counts),
        "lastMessageReportSuccessAt": last_message_success.isoformat() if last_message_success else None,
        "recentMessageReportSuccess": bool(last_message_success and cutoff <= last_message_success <= now),
        "terminalRetryFailuresInTail": terminal_failures,
        "terminalRecovery": "requires-server-state-verification" if terminal_failures else "not-established-by-this-log",
        "dateInference": "time-only-records; verify rotation and local timezone",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--window-seconds", type=int, default=300)
    args = parser.parse_args()
    if not 60 <= args.window_seconds <= 3600:
        parser.error("window must be between 60 and 3600 seconds")
    now = dt.datetime.now().astimezone()
    try:
        with args.log.open("rb") as source:
            stat = source.seek(0, 2)
            start = max(0, stat - 4 * 1024 * 1024)
            source.seek(start)
            if start:
                source.readline()
            data = source.read(4 * 1024 * 1024)
        mtime = dt.datetime.fromtimestamp(args.log.stat().st_mtime, now.tzinfo)
        if mtime.date() != now.date():
            print(json.dumps({"status": "unknown", "reason": "log-not-written-today"}))
            return 2
        result = summarize(data.decode("utf-8", errors="replace").splitlines(), now, args.window_seconds)
    except OSError:
        print(json.dumps({"status": "unknown", "reason": "log-unavailable"}))
        return 2
    result.update({"observedAt": now.isoformat(), "windowSeconds": args.window_seconds, "tailTruncated": bool(start)})
    result["status"] = "alert" if result["recentFailures"] else ("observed" if result["recordStreamFresh"] else "unknown")
    # An observed stream is deliberately not called healthy: no task activity
    # and an old exhausted completion both need separate treatment.
    print(json.dumps(result, indent=2))
    return {"alert": 1, "unknown": 2, "observed": 0}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())
