import unittest
from unittest.mock import patch
from openvps.network import tcp_check
from openvps.cli import _tcp_argument


class NetworkTests(unittest.TestCase):
    def test_tcp_argument(self):
        self.assertEqual(_tcp_argument("example.com:443"), ("example.com", 443))
        self.assertEqual(_tcp_argument("[::1]:443"), ("::1", 443))

    def test_tcp_invalid_port(self):
        with self.assertRaises(Exception):
            _tcp_argument("example.com:99999")

    @patch("openvps.network.socket.create_connection")
    def test_tcp_check_success(self, connect):
        self.assertTrue(tcp_check("example.com", 443)["ok"])
        connect.assert_called_once()


if __name__ == "__main__":
    unittest.main()
