import json
import unittest
from openvps.reporting import build_report, json_dumps, format_bytes
from openvps.diagnostics import evaluate


class ReportingTests(unittest.TestCase):
    def test_json_report_is_serializable(self):
        report = build_report({"hostname": "test"}, {"memory": {}}, {"interfaces": []}, [])
        decoded = json.loads(json_dumps(report))
        self.assertEqual(decoded["system"]["hostname"], "test")

    def test_bytes(self):
        self.assertEqual(format_bytes(1024), "1.0 KiB")
        self.assertEqual(format_bytes(None), "unknown")

    def test_high_memory_finding(self):
        findings = evaluate({}, {"memory": {"used_percent": 97}, "root_filesystem": {}}, {})
        self.assertEqual(findings[0]["severity"], "high")
        self.assertEqual(findings[0]["code"], "MEMORY_CRITICAL")


if __name__ == "__main__":
    unittest.main()
