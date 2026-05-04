#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Cleaning build artifacts and caches..."

find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PROJECT_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$PROJECT_DIR" -type f -name "*.pyo" -delete 2>/dev/null || true
find "$PROJECT_DIR" -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

rm -rf "$PROJECT_DIR/build" 2>/dev/null || true
rm -rf "$PROJECT_DIR/dist" 2>/dev/null || true
rm -rf "$PROJECT_DIR/.pytest_cache" 2>/dev/null || true
rm -rf "$PROJECT_DIR/.mypy_cache" 2>/dev/null || true
rm -rf "$PROJECT_DIR/.ruff_cache" 2>/dev/null || true

echo "Done."
