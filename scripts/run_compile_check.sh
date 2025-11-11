#!/usr/bin/env bash
set -euo pipefail

# Determine project root (directory containing this script's parent)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -d ".venv" ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

python3 -m compileall app
