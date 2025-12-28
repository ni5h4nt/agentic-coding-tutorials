#!/usr/bin/env python3
"""
PreToolUse Hook: Runs BEFORE Claude writes/edits files.
Blocks dangerous patterns in generated code.

Exit codes:
  0 = Allow the operation
  2 = BLOCK the operation (stderr sent to Claude)
"""
import json
import re
import sys

# Patterns that should NEVER appear in generated CLIs
DANGEROUS_PATTERNS = [
    (r"\beval\s*\(", "eval() is forbidden"),
    (r"\bexec\s*\(", "exec() is forbidden"),
    (r"shell\s*=\s*True", "shell=True is forbidden"),
    (r"\bos\.system\s*\(", "os.system() is forbidden"),
]

FORBIDDEN_PATHS = [".env", "credentials", "secrets", "/etc/", "/usr/"]


def main():
    try:
        # Hooks receive JSON input via stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Only check Write and Edit operations
        if tool_name not in ["Write", "Edit"]:
            sys.exit(0)  # Allow other tools

        file_path = tool_input.get("file_path", "")

        # Check forbidden paths
        for forbidden in FORBIDDEN_PATHS:
            if forbidden in file_path.lower():
                print(f"BLOCKED: Cannot write to '{file_path}'", file=sys.stderr)
                sys.exit(2)  # Exit 2 = BLOCK

        # Check content for dangerous patterns (Write tool)
        if tool_name == "Write":
            content = tool_input.get("content", "")

            # Only check Python files in generated/
            if file_path.endswith(".py") and "generated/" in file_path:
                for pattern, message in DANGEROUS_PATTERNS:
                    if re.search(pattern, content, re.IGNORECASE):
                        print(f"BLOCKED: {message}", file=sys.stderr)
                        print(f"Found in: {file_path}", file=sys.stderr)
                        sys.exit(2)  # BLOCK

        # Check new content for dangerous patterns (Edit tool)
        if tool_name == "Edit":
            new_content = tool_input.get("new_string", "")
            if file_path.endswith(".py") and "generated/" in file_path:
                for pattern, message in DANGEROUS_PATTERNS:
                    if re.search(pattern, new_content, re.IGNORECASE):
                        print(f"BLOCKED: {message}", file=sys.stderr)
                        sys.exit(2)

        # All checks passed
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)  # Don't block on JSON errors
    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Fail open


if __name__ == "__main__":
    main()
