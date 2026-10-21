"""Compatibility alias for virtualization detection."""
from .system import _virtualization


def collect_virtualization():
    return {"type": _virtualization()}
