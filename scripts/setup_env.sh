#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: python3 is not installed. Install it with 'sudo apt install python3 python3-venv python3-pip'." >&2
  exit 1
fi

VENV_DIR="${PROJECT_ROOT}/.venv"

if [ ! -d "${VENV_DIR}" ]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip

if [ ! -f "${PROJECT_ROOT}/requirements.txt" ]; then
  echo "Error: requirements.txt introuvable dans ${PROJECT_ROOT}." >&2
  exit 1
fi

python -m pip install -r "${PROJECT_ROOT}/requirements.txt"

echo "\n✅ Environnement virtuel prêt. Activez-le avec : source .venv/bin/activate"
