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

echo "Checking/installing ruff..."
pip install --quiet --upgrade pip 2>/dev/null || true
pip install --quiet ruff 2>/dev/null || true
{ python3 -c "import ruff" 2>/dev/null; } || {
    echo "ERROR: Failed to install ruff. Try: pip install ruff"
    exit 1
}

echo "Formatting code..."
cd "$PROJECT_DIR"
python3 -m ruff format string_ops/ tui/ tests/ main.py operations_mapping.py

echo "Running ruff --fix..."
python3 -m ruff check --fix string_ops/ tui/ tests/ main.py operations_mapping.py

echo ""
echo "Formatting complete."
