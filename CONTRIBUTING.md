# Contributing

Thanks for helping improve OpenVPS Toolkit.

1. Open an issue for significant features or behavior changes.
2. Keep collection read-only by default.
3. Do not add shell execution or automatic remediation without prior discussion.
4. Keep network probes opt-in, bounded by timeouts, and clearly documented.
5. Add tests for parsers, edge cases, and unavailable system files.
6. Run `python3 -m unittest discover -s tests -v`.
7. Never commit real server reports, IPs, hostnames, credentials, tokens, or other sensitive data.

Use standard-library functionality where practical to keep installation simple.
