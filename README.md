# OpenVPS Toolkit

**Lightweight, open-source diagnostics for Linux VPS and servers.**

OpenVPS Toolkit collects useful system and network information, displays a readable terminal summary, and can export a JSON report. It is designed to help VPS owners, developers, and system administrators understand a server's basic health without changing its configuration.

> **Project status:** Version 1.0.0 is an initial release. Check the output and run the tests on your target Linux distribution before using it in production or incident response.

## Features

- Operating system, kernel, architecture, hostname, uptime, and CPU details
- Virtualization information where available
- Memory, swap, load average, and filesystem usage
- Network interface and default-route information where available
- Optional DNS lookup and TCP connectivity checks
- Human-readable terminal output
- JSON report export for later review or automation
- Python standard-library runtime; no third-party runtime packages required
- Read-only system checks by default

## Safety and privacy

- The toolkit does not intentionally modify SSH, firewall, package, or system configuration.
- It does not automatically install updates, repair services, or apply fixes.
- Network probes are opt-in and can generate outbound traffic to the host you specify.
- Reports are saved locally only; the toolkit does not upload them.
- Reports can contain hostnames, IP addresses, mount points, and other environment details. Review and redact a report before sharing it.
- Results are best-effort and may be incomplete in containers or restricted environments.

## Requirements

- Linux
- Python 3.9 or newer
- Git for the clone-based installation or one-command installer

Some checks depend on information exposed by the operating system. Missing data does not always mean that a server is unhealthy.

## Quick start: clone and run

```bash
git clone https://github.com/shadowextra25/Open-VPS-Toolkit.git
cd Open-VPS-Toolkit
python3 -m openvps
```

Run the full diagnostic collection:

```bash
python3 -m openvps --full
```

Save a JSON report:

```bash
python3 -m openvps --full --json openvps-report.json
```

Run optional DNS and TCP connectivity checks:

```bash
python3 -m openvps --dns example.com --tcp example.com:443
```

Only run network probes when you understand and authorize the traffic they generate. The exact options are also available with:

```bash
python3 -m openvps --help
```

## Install with the installer

Run the installer from the repository directory after cloning the repository:

```bash
sh install.sh
```

Alternatively, after reviewing the installer, run:

```bash
curl -fsSL https://raw.githubusercontent.com/shadowextra25/Open-VPS-Toolkit/main/install.sh | sh
```

The installer is intended to install into the current user's home directory, without `sudo`. It places the launcher in `~/.local/bin`. If that directory is not on your `PATH`, add it before running `openvps` from any directory. Review scripts before running them, especially when downloaded from the internet.

## Example JSON report

The report includes the checks and values available on the current system. Its exact contents can vary by Linux distribution, permissions, and virtualization environment.

```bash
python3 -m openvps --full --json openvps-report.json
```

## Development and tests

Clone the repository, then run:

```bash
python3 -m unittest discover -s tests -v
python3 -m openvps --help
```

The tests use mocked system inputs where possible and should not require a live VPS. Please report the operating system and Python version when filing a bug. Remove secrets and sensitive machine details from logs and reports before sharing them.

## Contributing

Issues and pull requests are welcome. For substantial changes, open an issue first to discuss the proposal. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before contributing or reporting a vulnerability.

## License

OpenVPS Toolkit is released under the [MIT License](LICENSE). You may use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software under the terms of that license.
