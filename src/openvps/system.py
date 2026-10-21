"""Best-effort read-only system information collectors."""
import os
import platform
import socket
from pathlib import Path


def _read_text(path, default=None):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace").strip()
    except (OSError, ValueError):
        return default


def _parse_os_release():
    raw = _read_text("/etc/os-release", "") or ""
    result = {}
    for line in raw.splitlines():
        if "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        result[key] = value.strip().strip('"').strip("'")
    return result


def _uptime_seconds():
    raw = _read_text("/proc/uptime")
    if not raw:
        return None
    try:
        return int(float(raw.split()[0]))
    except (ValueError, IndexError):
        return None

def _cpu_model():
    raw = _read_text("/proc/cpuinfo", "") or ""
    preferred_keys = ("model name", "hardware", "processor")

    entries = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if value:
            entries.setdefault(key, []).append(value)

    for key in preferred_keys:
        for value in entries.get(key, []):
            if key == "processor" and value.isdigit():
                continue
            if value:
                return value

    return platform.processor() or None

def _virtualization():
    # Detect WSL before checking generic container or VM indicators.
    kernel = (platform.release() or "").lower()
    version = (_read_text("/proc/version", "") or "").lower()

    if "microsoft" in kernel or "microsoft" in version:
        return "wsl"

    if Path("/.dockerenv").exists():
        return "docker"

    cgroup = (_read_text("/proc/1/cgroup", "") or "").lower()
    if "kubepods" in cgroup:
        return "kubernetes/container"
    if "lxc" in cgroup:
        return "lxc"

    dmi = (_read_text("/sys/class/dmi/id/product_name", "") or "").lower()
    for needle, label in (
        ("kvm", "kvm"),
        ("vmware", "vmware"),
        ("virtualbox", "virtualbox"),
        ("hyper-v", "hyper-v"),
        ("xen", "xen"),
        ("qemu", "qemu"),
        ("openvz", "openvz"),
    ):
        if needle in dmi:
            return label

    return "unknown"

def collect_system():
    os_release = _parse_os_release()
    try:
        hostname = socket.gethostname()
    except OSError:
        hostname = None
    return {
        "hostname": hostname,
        "os_name": os_release.get("PRETTY_NAME") or platform.system(),
        "os_id": os_release.get("ID"),
        "os_version": os_release.get("VERSION_ID"),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "uptime_seconds": _uptime_seconds(),
        "cpu_model": _cpu_model(),
        "logical_cpu_count": os.cpu_count(),
        "virtualization": _virtualization(),
    }
