import copy
import datetime as dt
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("guard", Path(__file__).parents[1] / "scripts/check-reload.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class ReloadTests(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime.now(dt.timezone.utc)
        self.config = {"tun": {"enable": True, "auto-detect-interface": False},
                       "interface-name": "Test Wi-Fi", "mixed-port": 7890}
        self.snapshot = {"schemaVersion": 1, "observedAt": self.now.isoformat(),
                         "config": copy.deepcopy(self.config), "warnings": [],
                         "physicalInterface": {"name": "Test Wi-Fi", "status": "Up", "forwarding": "Disabled"}}

    def test_equal(self):
        self.assertEqual(guard.check(self.snapshot, self.config, self.now), [])

    def test_tun_change(self):
        self.config["tun"]["auto-detect-interface"] = True
        self.assertIn("tun:changed", guard.check(self.snapshot, self.config, self.now))

    def test_missing_default(self):
        del self.config["mixed-port"]
        self.assertIn("mixed-port:unproven-default", guard.check(self.snapshot, self.config, self.now))

    def test_forwarding_enabled_or_unknown(self):
        for value in ("Enabled", None, ""):
            self.snapshot["physicalInterface"]["forwarding"] = value
            self.assertTrue(guard.check(self.snapshot, self.config, self.now))

    def test_stale_future_and_naive(self):
        for value in (self.now - dt.timedelta(minutes=3), self.now + dt.timedelta(seconds=1), self.now.replace(tzinfo=None)):
            self.snapshot["observedAt"] = value.isoformat()
            self.assertIn("stale-or-invalid-snapshot", guard.check(self.snapshot, self.config, self.now))

    def test_wrong_interface(self):
        self.snapshot["physicalInterface"]["name"] = "Other"
        self.assertIn("physical-interface:unverified", guard.check(self.snapshot, self.config, self.now))

    def test_type_change(self):
        self.config["tun"]["enable"] = 1
        self.assertIn("tun:changed", guard.check(self.snapshot, self.config, self.now))

    def test_unknown_fields_and_missing_tun(self):
        self.config["tun"]["new-option"] = True
        self.assertIn("tun:changed", guard.check(self.snapshot, self.config, self.now))
        del self.config["tun"]
        self.assertIn("tun:missing-or-invalid", guard.check(self.snapshot, self.config, self.now))

    def test_duplicate_yaml_rejected(self):
        with self.assertRaises(ValueError):
            guard.yaml.load("tun: {}\ntun: {}\n", Loader=guard.UniqueLoader)

    def test_empty_tun_is_not_proof(self):
        self.config["tun"] = {}
        self.snapshot["config"]["tun"] = {}
        self.assertIn("tun.enable:missing-or-invalid", guard.check(self.snapshot, self.config, self.now))

    def test_malformed_snapshot(self):
        self.assertTrue(guard.check([], self.config, self.now))
        self.assertTrue(guard.check({}, self.config, self.now))


if __name__ == "__main__":
    unittest.main()
