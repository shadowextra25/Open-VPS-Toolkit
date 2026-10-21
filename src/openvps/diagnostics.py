"""Conservative, explainable diagnostic rules."""


def evaluate(system, resources, network):
    findings = []
    memory = resources.get("memory") or {}
    used = memory.get("used_percent")
    if used is not None and used >= 95:
        findings.append({"severity": "high", "code": "MEMORY_CRITICAL",
                         "message": "Memory usage is at least 95%."})
    elif used is not None and used >= 85:
        findings.append({"severity": "warning", "code": "MEMORY_HIGH",
                         "message": "Memory usage is at least 85%."})

    disk = resources.get("root_filesystem") or {}
    disk_used = disk.get("used_percent")
    if disk_used is not None and disk_used >= 95:
        findings.append({"severity": "high", "code": "ROOT_DISK_CRITICAL",
                         "message": "Root filesystem usage is at least 95%."})
    elif disk_used is not None and disk_used >= 85:
        findings.append({"severity": "warning", "code": "ROOT_DISK_HIGH",
                         "message": "Root filesystem usage is at least 85%."})

    if network.get("dns") and not network["dns"].get("ok"):
        findings.append({"severity": "warning", "code": "DNS_LOOKUP_FAILED",
                         "message": "The requested DNS lookup failed."})
    if network.get("tcp") and not network["tcp"].get("ok"):
        findings.append({"severity": "warning", "code": "TCP_CHECK_FAILED",
                         "message": "The requested TCP connectivity check failed."})
    return findings
