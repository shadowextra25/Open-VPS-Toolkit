import unittest
from unittest.mock import patch, mock_open
from openvps.resources import _meminfo


class ResourceTests(unittest.TestCase):
    @patch("openvps.resources.Path.read_text", return_value="MemTotal: 100 kB\nMemAvailable: 25 kB\nSwapTotal: 0 kB\n")
    def test_meminfo_converts_kib_to_bytes(self, _mock_read):
        data = _meminfo()
        self.assertEqual(data["MemTotal"], 102400)
        self.assertEqual(data["MemAvailable"], 25600)
        self.assertEqual(data["SwapTotal"], 0)


if __name__ == "__main__":
    unittest.main()
