#!/usr/bin/env python3
"""Verify that all generated Python files are syntactically valid."""

import ast
import sys
from pathlib import Path


def verify_file(filepath: Path) -> tuple[bool, str]:
    """Verify a Python file is syntactically valid.

    Args:
        filepath: Path to Python file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {e}"


def main() -> int:
    """Main verification function."""
    base_dir = Path(__file__).parent
    python_files = list(base_dir.glob('**/*.py'))

    print(f"Verifying {len(python_files)} Python files...\n")

    all_valid = True
    for filepath in sorted(python_files):
        relative_path = filepath.relative_to(base_dir)
        is_valid, error_msg = verify_file(filepath)

        if is_valid:
            print(f"✓ {relative_path}")
        else:
            print(f"✗ {relative_path}")
            print(f"  {error_msg}")
            all_valid = False

    print()
    if all_valid:
        print(f"✓ All {len(python_files)} files are syntactically valid!")
        return 0
    else:
        print("✗ Some files have syntax errors")
        return 1


if __name__ == '__main__':
    sys.exit(main())
