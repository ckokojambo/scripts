#!/usr/bin/env bash
set -euo pipefail

USER="blackbox_exporter"
GROUP="blackbox_exporter"
BIN_SRC="${1:-./blackbox_exporter}"
BIN_DST="/usr/local/bin/blackbox_exporter"
ETC_DIR="/etc/blackbox_exporter"
DATA_DIR="/var/lib/blackbox_exporter"

require_root() {
  if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
    echo "Error: must be run as root. Try: sudo $0 [path-to-blackbox_exporter]" >&2
    exit 1
  fi
}

main() {
  require_root

  # Create system user (idempotent)
  if ! id -u "$USER" >/dev/null 2>&1; then
    useradd --system --no-create-home --shell /usr/sbin/nologin "$USER"
  fi

  # Ensure directories exist
  install -d -m 0755 "$ETC_DIR"
  install -d -m 0755 "$DATA_DIR"

  # Ensure ownership for data dir
  chown -R "$USER:$GROUP" "$DATA_DIR"

  # Install the binary
  if [[ ! -f "$BIN_SRC" ]]; then
    echo "Error: binary not found at: $BIN_SRC" >&2
    echo "Usage: sudo $0 /path/to/blackbox_exporter" >&2
    exit 1
  fi
  install -m 0755 "$BIN_SRC" "$BIN_DST"

  # Reload and enable service
  systemctl daemon-reload
  systemctl enable --now blackbox_exporter
}

main "$@"
