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

echo "Installing core dependencies..."
pip install --quiet -e "$PROJECT_DIR"

echo "Installing dev dependencies..."
pip install --quiet -e "$PROJECT_DIR[dev]"

echo "Installing optional dependencies (crypto, hash extensions)..."
pip install --quiet pycryptodome blake3 xxhash bcrypt    || true
pip install --quiet mmh3                                   || true

echo ""
echo "Installation complete."
echo "Run './scripts/run_tui.sh' to launch the TUI."
echo "Run './scripts/run_tests.sh' to run the test suite."
