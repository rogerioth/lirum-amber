#!/usr/bin/env python3
"""Entry point for the String Operations TUI application."""

import sys
import os


def main():
    """Launch the TUI application."""
    # Ensure the project root is on the path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        from tui.app import StringOpsApp
    except ImportError as e:
        print(f"Failed to import TUI: {e}")
        print("The TUI requires 'textual' to be installed.")
        print("Install it with: pip install textual")
        sys.exit(1)

    app = StringOpsApp()
    app.run()


if __name__ == "__main__":
    main()
