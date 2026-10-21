"""Terminal and JSON report formatting."""
import json
from datetime import datetime, timezone


def build_report(system, resources, network, findings):
    return {
        "tool": {"name": "OpenVPS Toolkit", "version": "1.0.0"},
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "system": system,
        "resources": resources,
        "network": network,
        "findings": findings,
    }


def format_bytes(value):
    if value is None:
        return "unknown"
    amount = float(value)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if amount < 1024 or unit == "TiB":
            return f"{amount:.1f} {unit}" if unit != "B" else f"{int(amount)} B"
        amount /= 1024
    return f"{amount:.1f} TiB"


def render_terminal(report):
    system = report["system"]
    resources = report["resources"]
    memory = resources.get("memory") or {}
    swap = resources.get("swap") or {}
    disk = resources.get("root_filesystem") or {}
    lines = [
        f'{report["tool"]["name"]} v{report["tool"]["version"]}',
        "=" * 34,
        "",
        "SYSTEM",
        f'  Hostname:       {system.get("hostname") or "unknown"}',
        f'  OS:             {system.get("os_name") or "unknown"}',
        f'  Kernel:         {system.get("kernel") or "unknown"}',
        f'  Architecture:   {system.get("architecture") or "unknown"}',
        f'  Virtualization: {system.get("virtualization") or "unknown"}',
        f'  CPU:            {system.get("cpu_model") or "unknown"}',
        f'  Logical CPUs:   {system.get("logical_cpu_count") or "unknown"}',
        "",
        "RESOURCES",
        f'  RAM:            {format_bytes(memory.get("used_bytes"))} used / {format_bytes(memory.get("total_bytes"))} total',
        f'  RAM usage:      {memory.get("used_percent") if memory.get("used_percent") is not None else "unknown"}%',
        f'  Swap used:      {format_bytes(swap.get("used_bytes"))} / {format_bytes(swap.get("total_bytes"))}',
        f'  Root disk:      {format_bytes(disk.get("used_bytes"))} used / {format_bytes(disk.get("total_bytes"))} total',
        f'  Root usage:     {disk.get("used_percent") if disk.get("used_percent") is not None else "unknown"}%',
        "",
        "NETWORK",
        f'  Interfaces:     {len(report["network"].get("interfaces", []))}',
    ]
    if report["network"].get("dns"):
        dns = report["network"]["dns"]
        lines.append(f'  DNS lookup:     {"OK" if dns.get("ok") else "FAILED"} ({dns.get("host")})')
    if report["network"].get("tcp"):
        tcp = report["network"]["tcp"]
        lines.append(f'  TCP check:      {"OK" if tcp.get("ok") else "FAILED"} ({tcp.get("host")}:{tcp.get("port")})')
    lines.extend(["", "DIAGNOSTICS"])
    findings = report.get("findings", [])
    if not findings:
        lines.append("  [OK] No threshold-based issues detected.")
    else:
        for item in findings:
            label = "HIGH" if item["severity"] == "high" else "WARN"
            lines.append(f'  [{label}] {item["message"]}')
    lines.extend(["", f'Generated: {report["generated_at"]}'])
    return "\n".join(lines)


def json_dumps(report):
    return json.dumps(report, indent=2, sort_keys=True)
