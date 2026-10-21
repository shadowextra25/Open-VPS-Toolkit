#!/bin/sh
set -eu
INSTALL_DIR="${OPENVPS_INSTALL_DIR:-$HOME/.local/share/openvps-toolkit}"
BIN_DIR="${OPENVPS_BIN_DIR:-$HOME/.local/bin}"
rm -rf "$INSTALL_DIR"
rm -f "$BIN_DIR/openvps"
echo "OpenVPS Toolkit user installation removed."
