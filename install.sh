#!/bin/sh
set -eu

REPO_URL="https://github.com/shadowextra25/Open-VPS-Toolkit.git"
INSTALL_DIR="${OPENVPS_INSTALL_DIR:-$HOME/.local/share/openvps-toolkit}"
BIN_DIR="${OPENVPS_BIN_DIR:-$HOME/.local/bin}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: Python 3 is required." >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "Error: Git is required by this installer. Install git or clone the repository manually." >&2
  exit 1
fi
if [ -e "$INSTALL_DIR" ]; then
  echo "Error: install destination already exists: $INSTALL_DIR" >&2
  echo "Move it aside or set OPENVPS_INSTALL_DIR to a new directory, then retry." >&2
  exit 1
fi

mkdir -p "$(dirname "$INSTALL_DIR")" "$BIN_DIR"
TMP_DIR="$(mktemp -d)"
cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT HUP INT TERM

git clone --depth 1 "$REPO_URL" "$TMP_DIR/repo"
mkdir -p "$INSTALL_DIR"
cp -R "$TMP_DIR/repo/src" "$INSTALL_DIR/src"

cat > "$BIN_DIR/openvps" <<EOF_LAUNCHER
#!/bin/sh
export PYTHONPATH="$INSTALL_DIR/src\${PYTHONPATH:+:\$PYTHONPATH}"
exec python3 -m openvps "\$@"
EOF_LAUNCHER
chmod 755 "$BIN_DIR/openvps"

echo "OpenVPS Toolkit installed."
echo "Run: $BIN_DIR/openvps --full"
case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) echo "Note: add $BIN_DIR to your PATH to run 'openvps' from any directory." ;;
esac
