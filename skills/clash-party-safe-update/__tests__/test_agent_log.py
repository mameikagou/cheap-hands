import datetime as dt
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("agent_log", Path(__file__).parents[1] / "scripts/check-agent-log.py")
log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log)


class LogTests(unittest.TestCase):
    now = dt.datetime(2026, 9, 8, 21, 35, tzinfo=dt.timezone(dt.timedelta(hours=8)))

    def test_debug_failure_not_hidden_by_heartbeat(self):
        result = log.summarize([
            "21:34:01.100 DBG failed to report task messages component=daemon task=private error=private",
            "21:34:59.000 DBG heartbeat: skipping HTTP tick, WS recently acked component=daemon",
        ], self.now)
        self.assertEqual(result["recentFailures"], {"messageReport": 1})
        self.assertTrue(result["recordStreamFresh"])

    def test_complete_log_is_not_server_ack(self):
        result = log.summarize(["21:34:01.100 INF task completed component=daemon"], self.now)
        self.assertFalse(result["recentMessageReportSuccess"])
        self.assertEqual(result["terminalRecovery"], "not-established-by-this-log")

    def test_old_completion_failure_remains_unverified(self):
        result = log.summarize([
            "21:24:38.000 ERR complete task failed after retries; leaving task in running rather than falling back to fail component=daemon",
            "21:34:59.000 DBG reported task messages component=daemon",
        ], self.now)
        self.assertEqual(result["recentFailures"], {})
        self.assertTrue(result["recentMessageReportSuccess"])
        self.assertEqual(result["terminalRetryFailuresInTail"], 1)
        self.assertEqual(result["terminalRecovery"], "requires-server-state-verification")

    def test_stale_records_not_fresh(self):
        result = log.summarize(["20:34:59.000 DBG reported task messages component=daemon"], self.now)
        self.assertFalse(result["recordStreamFresh"])

    def test_midnight(self):
        now = self.now.replace(hour=0, minute=1)
        result = log.summarize([
            "23:59:59.000 WRN report task usage failed component=daemon",
            "00:00:59.000 DBG reported task messages component=daemon",
        ], now)
        self.assertEqual(result["recentFailures"], {"usageReport": 1})
        self.assertTrue(result["recordStreamFresh"])

    def test_quoted_error_is_not_failure(self):
        result = log.summarize([
            '21:34:59.000 DBG agent component=daemon text="failed to report task messages"'
        ], self.now)
        self.assertEqual(result["recentFailures"], {})

    def test_future_timestamp_is_unknown(self):
        result = log.summarize(["21:40:59.000 DBG reported task messages component=daemon"], self.now)
        self.assertFalse(result["recordStreamFresh"])


if __name__ == "__main__":
    unittest.main()
