"""Network inventory and explicitly requested, bounded connectivity probes."""
import socket
from pathlib import Path


def collect_interfaces():
    """Return interface names and best-effort IPv4/IPv6 addresses from procfs."""
    interfaces = {}
    for proc_path, family in (
        ("/proc/net/fib_trie", "ipv4"),
        ("/proc/net/if_inet6", "ipv6"),
    ):
        try:
            raw = Path(proc_path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if family == "ipv6":
            for line in raw.splitlines():
                parts = line.split()
                if len(parts) >= 6:
                    address, _idx, _prefix, _scope, _flags, name = parts[:6]
                    try:
                        ip = socket.inet_ntop(socket.AF_INET6, bytes.fromhex(address))
                    except (ValueError, OSError):
                        continue
                    interfaces.setdefault(name, {"ipv4": [], "ipv6": []})["ipv6"].append(ip)
        # fib_trie does not reliably associate addresses with interfaces on all kernels.
        # IPv4 collection is therefore intentionally left best-effort/empty rather than guessed.
    try:
        names = [name for _, name in socket.if_nameindex()]
        for name in names:
            interfaces.setdefault(name, {"ipv4": [], "ipv6": []})
    except OSError:
        pass
    return [{"name": name, **addresses} for name, addresses in sorted(interfaces.items())]


def dns_lookup(host, timeout=3.0):
    """Resolve a host name; getaddrinfo has no portable per-call timeout."""
    if not host or len(host) > 253 or any(c.isspace() for c in host):
        return {"host": host, "ok": False, "addresses": [], "error": "Invalid hostname"}
    try:
        answers = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        addresses = sorted({item[4][0] for item in answers})
        return {"host": host, "ok": bool(addresses), "addresses": addresses, "error": None}
    except (socket.gaierror, OSError) as exc:
        return {"host": host, "ok": False, "addresses": [], "error": str(exc)}


def tcp_check(host, port, timeout=2.0):
    if not host or len(host) > 253 or any(c.isspace() for c in host):
        return {"host": host, "port": port, "ok": False, "error": "Invalid hostname"}
    if not isinstance(port, int) or not 1 <= port <= 65535:
        return {"host": host, "port": port, "ok": False, "error": "Port must be between 1 and 65535"}
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"host": host, "port": port, "ok": True, "error": None}
    except (OSError, socket.timeout) as exc:
        return {"host": host, "port": port, "ok": False, "error": str(exc)}
