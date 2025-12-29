---
name: enforcing-code-style
description: Enforces Python and Click code style conventions when generating or reviewing CLI code. Use when writing Python code, generating CLI commands, or reviewing code quality.
allowed-tools: Read, Grep, Glob
---

# Code Style Enforcer

## Python Conventions

When generating or reviewing Python code, ensure:

### Imports Order
1. Standard library imports
2. Third-party imports (click, rich, etc.)
3. Local imports

### Type Hints
- All function signatures must have type hints
- Use `|` for unions (Python 3.11+): `str | None`
- Use `list[str]` not `List[str]`

### Click-Specific
- Decorators order: `@cli.command()` then `@click.option()` then `@click.argument()`
- Options before arguments in decorator stack
- Always include `help=` parameter

## Option Naming

### Standard Short Options
| Short | Meaning | Never use for |
|-------|---------|---------------|
| -v | verbose | version |
| -q | quiet | - |
| -o | output | - |
| -f | force | - |
| -n | dry-run | - |
| -r | recursive | - |

### Long Option Format
- Use kebab-case: `--output-file` not `--outputFile`
- Use full words: `--config` not `--cfg`

## When to Flag Issues

If you see code that violates these conventions:
1. Point out the specific violation
2. Show the corrected version
3. Explain why the convention matters
