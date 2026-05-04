#!/usr/bin/env python3
"""Lirum Amber — a TUI and CLI for 200+ string operations, by Lirum Labs."""

import sys
import os


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    if len(sys.argv) > 1:
        from cli import run_cli
        run_cli()
    else:
        try:
            from tui.app import StringOpsApp
        except ImportError as e:
            print(f"Failed to import TUI: {e}")
            print("The TUI requires 'textual' to be installed.")
            print("Install it with: pip install textual")
            sys.exit(1)
        StringOpsApp().run()


if __name__ == "__main__":
    main()
