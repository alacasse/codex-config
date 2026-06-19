#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python_bin="${PYTHON:-python3}"

exec "$python_bin" "$repo_root/scripts/install_codex_config.py" \
  --repo-root "$repo_root" \
  "$@"
