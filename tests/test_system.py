import unittest
from unittest.mock import patch
from openvps.system import _uptime_seconds, _parse_os_release


class SystemTests(unittest.TestCase):
    @patch("openvps.system._read_text", return_value="12345.9 999.0")
    def test_uptime_seconds(self, _):
        self.assertEqual(_uptime_seconds(), 12345)

    @patch("openvps.system._read_text", return_value='NAME="Example Linux"\nID=example\nVERSION_ID="1.2"')
    def test_parse_os_release(self, _):
        result = _parse_os_release()
        self.assertEqual(result["NAME"], "Example Linux")
        self.assertEqual(result["ID"], "example")
        self.assertEqual(result["VERSION_ID"], "1.2")


if __name__ == "__main__":
    unittest.main()
