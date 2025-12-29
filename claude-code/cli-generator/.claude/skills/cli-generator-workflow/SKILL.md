---
name: cli-generator-workflow
description: Use when working on CLI Generator project tasks including designing CLIs, generating code, or running the /design, /generate, or /implement commands. Ensures consistent workflow across the project.
---

# CLI Generator Workflow

## Project Context

This skill applies to the CLI Generator project specifically.
For general CLI development, see other skills.

## The Standard Workflow

### 1. Design Phase (/design)
**Input:** Natural language description
**Output:** CLISpec (validated specification)

Checklist:
- [ ] All commands have descriptions
- [ ] Options follow naming conventions (-v=verbose, -o=output)
- [ ] Required arguments identified
- [ ] Examples provided for each command

### 2. Generate Phase (/generate)
**Input:** CLISpec
**Output:** Python code + tests

Checklist:
- [ ] Code passes syntax validation
- [ ] Type hints on all functions
- [ ] Click decorators in correct order
- [ ] Tests generated for each command

### 3. Implement Phase (/implement)
**Input:** Generated code with TODO stubs
**Output:** Working implementation

Checklist:
- [ ] All TODOs replaced with real code
- [ ] Error handling added
- [ ] Tests pass

## Project-Specific Rules

### File Locations
- Generated CLIs: `generated/{cli-name}/`
- Specs: `generated/{cli-name}/spec.json`
- Tests: `generated/{cli-name}/tests/`

### Required Dependencies
Always include in generated CLIs:
- click (CLI framework)
- rich (optional, for pretty output)

### Forbidden Patterns
Never generate:
- eval() or exec()
- Hardcoded credentials
- Commands that delete without --force confirmation

## When NOT to Use This Skill

- Working on cli-generator's own code (not generated CLIs)
- General Python development unrelated to CLI generation
- Debugging cli-generator internals
