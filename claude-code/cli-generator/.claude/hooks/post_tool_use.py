#!/usr/bin/env python3
"""
PostToolUse Hook: Runs AFTER Claude writes files.
Validates Python syntax in generated code.

Note: PostToolUse cannot block (operation already happened).
Use stdout to provide feedback to Claude.
"""
import ast
import json
import sys
from pathlib import Path


def main():
    try:
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        if tool_name != "Write":
            sys.exit(0)

        file_path = tool_input.get("file_path", "")

        # Only validate Python files in generated/
        if not file_path.endswith(".py") or "generated/" not in file_path:
            sys.exit(0)

        # Read and validate the file
        path = Path(file_path)
        if not path.exists():
            sys.exit(0)

        code = path.read_text()

        try:
            ast.parse(code)
            # Print to stdout - shown to Claude as context
            print(f"Syntax OK: {file_path}")
        except SyntaxError as e:
            # Print warning - Claude will see this
            print(f"WARNING: Syntax error in {file_path}")
            print(f"  Line {e.lineno}: {e.msg}")
            print("Please fix the syntax error.")

        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
