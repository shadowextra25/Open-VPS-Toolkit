"""Read-only CPU, memory, and filesystem resource checks."""
import os
import shutil
from pathlib import Path


def _meminfo():
    data = {}
    try:
        lines = Path("/proc/meminfo").read_text(encoding="utf-8").splitlines()
    except OSError:
        return data
    for line in lines:
        if ":" not in line:
            continue
        key, rest = line.split(":", 1)
        parts = rest.strip().split()
        if parts:
            try:
                # Linux meminfo values are normally kB.
                data[key] = int(parts[0]) * 1024
            except ValueError:
                pass
    return data


def _load_average():
    try:
        one, five, fifteen = os.getloadavg()
        return {"1m": one, "5m": five, "15m": fifteen}
    except (AttributeError, OSError):
        return None


def collect_resources():
    mem = _meminfo()
    total = mem.get("MemTotal")
    available = mem.get("MemAvailable")
    if available is None and total is not None:
        available = mem.get("MemFree", 0) + mem.get("Buffers", 0) + mem.get("Cached", 0)
    swap_total = mem.get("SwapTotal")
    swap_free = mem.get("SwapFree")
    try:
        disk = shutil.disk_usage("/")
        disk_info = {
            "path": "/",
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
            "used_percent": round((disk.used / disk.total) * 100, 2) if disk.total else None,
        }
    except OSError:
        disk_info = None

    return {
        "memory": {
            "total_bytes": total,
            "available_bytes": available,
            "used_bytes": max(0, total - available) if total is not None and available is not None else None,
            "used_percent": round((total - available) / total * 100, 2)
                if total and available is not None else None,
        },
        "swap": {
            "total_bytes": swap_total,
            "free_bytes": swap_free,
            "used_bytes": max(0, swap_total - swap_free)
                if swap_total is not None and swap_free is not None else None,
        },
        "load_average": _load_average(),
        "root_filesystem": disk_info,
    }
