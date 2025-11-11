#!/usr/bin/env bash
set -euo pipefail

# Determine project root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "$PROJECT_ROOT"

removed_any=false

if [ -d ".venv" ]; then
  rm -rf .venv
  echo "✅ Removed virtual environment at .venv"
  removed_any=true
else
  echo "ℹ️ No .venv directory found"
fi

# Remove Python cache directories
CACHE_DIRS=$(find . -type d -name '__pycache__')
if [ -n "$CACHE_DIRS" ]; then
  find . -type d -name '__pycache__' -prune -exec rm -rf {} +
  echo "✅ Cleared Python __pycache__ folders"
  removed_any=true
else
  echo "ℹ️ No __pycache__ folders found"
fi

# Optionally purge generated media
if [ -d "media" ]; then
  if [ "${1:-}" = "--purge-media" ]; then
    rm -rf media/* media/.gitignore 2>/dev/null || true
    mkdir -p media
    echo "✅ Removed generated files from media/"
    removed_any=true
  else
    echo "ℹ️ media/ kept (pass --purge-media to remove its contents)"
  fi
fi

if [ "$removed_any" = false ]; then
  echo "Nothing to clean."
fi
