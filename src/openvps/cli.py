"""Command-line interface."""
import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .diagnostics import evaluate
from .network import collect_interfaces, dns_lookup, tcp_check
from .reporting import build_report, json_dumps, render_terminal
from .resources import collect_resources
from .system import collect_system


def _tcp_argument(value):
    if value.startswith("["):
        end = value.find("]")
        if end < 0 or len(value) <= end + 2 or value[end + 1] != ":":
            raise argparse.ArgumentTypeError("Use HOST:PORT or [IPv6]:PORT")
        host, raw_port = value[1:end], value[end + 2:]
    else:
        if ":" not in value:
            raise argparse.ArgumentTypeError("Use HOST:PORT or [IPv6]:PORT")
        host, raw_port = value.rsplit(":", 1)
    try:
        port = int(raw_port)
    except ValueError:
        raise argparse.ArgumentTypeError("Port must be an integer")
    if not host or not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("Host is required and port must be 1-65535")
    return host, port


def make_parser():
    parser = argparse.ArgumentParser(
        prog="openvps",
        description="Read-only Linux VPS diagnostics. Network probes run only when requested.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--full", action="store_true", help="Collect all local diagnostic modules (default behavior)")
    parser.add_argument("--json", metavar="FILE", help="Write JSON report to FILE, or '-' for stdout")
    parser.add_argument("--dns", metavar="HOST", help="Explicitly perform a DNS lookup for HOST")
    parser.add_argument("--tcp", metavar="HOST:PORT", type=_tcp_argument,
                        help="Explicitly test TCP connectivity (e.g. example.com:443 or [::1]:443)")
    return parser


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)
    try:
        system = collect_system()
        resources = collect_resources()
        network = {"interfaces": collect_interfaces()}
        if args.dns:
            network["dns"] = dns_lookup(args.dns)
        if args.tcp:
            host, port = args.tcp
            network["tcp"] = tcp_check(host, port)
        findings = evaluate(system, resources, network)
        report = build_report(system, resources, network, findings)
        if args.json == "-":
            print(json_dumps(report))
        else:
            print(render_terminal(report))
            if args.json:
                target = Path(args.json).expanduser()
                target.write_text(json_dumps(report) + "\n", encoding="utf-8")
                print(f"\nJSON report written to: {target}")
        return 1 if any(item["severity"] == "high" for item in findings) else 0
    except (OSError, ValueError) as exc:
        print(f"openvps: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
