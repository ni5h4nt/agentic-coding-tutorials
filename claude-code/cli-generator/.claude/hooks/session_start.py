#!/usr/bin/env python3
"""
SessionStart Hook: Runs once when session begins.
Use for dynamic checks that CLAUDE.md can't do.
"""
import json
import subprocess
import sys

def main():
    try:
        input_data = json.load(sys.stdin)

        # Show current git branch
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True
        )
        if branch.stdout.strip():
            print(f"Branch: {branch.stdout.strip()}")

        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
