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

if ! python3 -c "import pytest" 2>/dev/null; then
    echo "Installing dependencies (including dev)..."
    pip install --quiet --upgrade pip
    pip install --quiet -e "$PROJECT_DIR[dev]"
fi

cd "$PROJECT_DIR"

PASSING="--no-header"
if [ "${1:-}" = "-v" ] || [ "${1:-}" = "--verbose" ]; then
    PASSING="-v"
fi

echo "Running tests..."
python3 -m pytest "$PROJECT_DIR/tests" $PASSING
