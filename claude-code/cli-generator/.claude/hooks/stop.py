#!/usr/bin/env python3
"""
Stop Hook: Runs when Claude finishes responding.
Reminds to run tests after code generation.
"""
import json
import sys
from pathlib import Path


def main():
    try:
        input_data = json.load(sys.stdin)

        # Check if any generated Python files exist
        generated_dir = Path("generated")
        if generated_dir.exists():
            py_files = list(generated_dir.rglob("*.py"))
            if py_files:
                print("Reminder: Run tests with 'uv run pytest' or /test")

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
