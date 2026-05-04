#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"

python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" || {
    echo "ERROR: Python 3.10+ is required."
    exit 1
}

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."
pip install --quiet --upgrade pip

echo "Installing project in editable mode with all deps..."
pip install --quiet -e "$PROJECT_DIR[dev]"
pip install --quiet pycryptodome blake3 xxhash bcrypt mmh3 2>/dev/null || true
pip install --quiet ruff mypy 2>/dev/null || true

echo ""
echo "Dev environment ready."
echo "Source the venv:  source .venv/bin/activate"
