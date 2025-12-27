# /design - Design a New CLI

## Purpose
Generate and preview a CLI specification from a natural language
description, without generating code yet.

## Usage
```
/design <description>
/design "A tool that encrypts files with AES"
/design --detailed "Complex multi-command CLI for database migrations"
```

## Process

### 1. Understand the Request
Parse the description to identify:
- Primary purpose
- Likely commands needed
- Input/output types
- Common options for this type of tool

### 2. Generate Specification
Use SpecGenerator to create CLISpec with:
- Appropriate name (derived from description)
- Clear, concise description
- Well-designed commands with arguments and options
- Helpful examples for each command
- Sensible defaults

### 3. Present for Review
```
CLI Design: <name>
================

Description: <description>

Commands:
---------
<command_name>
  <description>
  Arguments: <args>
  Options: <options>
  Example: <example>

[Repeat for each command]

Next steps:
  /refine <feedback>     - Modify the design
  /generate              - Generate code from this spec
  /save-spec <filename>  - Save spec to file
```

## Output
- Display formatted CLI design
- Do NOT generate code
- Do NOT save files
- Wait for user to approve or refine
