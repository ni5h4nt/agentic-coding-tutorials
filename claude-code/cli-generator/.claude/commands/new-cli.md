# /new-cli - Complete CLI Creation Workflow

## Purpose
Create a complete CLI from description through working code in one
guided workflow.

## Usage
```
/new-cli <description>
/new-cli "A tool to manage dotfiles across machines"
```

## Process

This command orchestrates the full workflow:

### Step 1: Design (/design)
```
Creating new CLI...

Step 1/5: Design
```
Run /design with the description.
Show the design for approval.

```
Design complete. Approve? [y/refine/cancel]
```

If "refine": Loop back with /refine until approved.
If "cancel": Stop workflow.

### Step 2: Generate (/generate)
```
Step 2/5: Generate
```
Run /generate --with-tests.
Show generated files.

### Step 3: Implement (/implement)
```
Step 3/5: Implement
```
For each command, offer to implement:
```
Implement 'sync' command? [y/skip/all]
```

### Step 4: Test (/test)
```
Step 4/5: Test
```
Run /test with coverage.
If failures: Offer to fix or continue.

### Step 5: Summary
```
Step 5/5: Complete!

CLI: <name>
Location: ./generated/<name>
Commands: <count> implemented, <count> TODO
Tests: <pass>/<total> passing
Coverage: <percent>%

Quick start:
  cd ./generated/<name>
  uv pip install -e .
  <name> --help
```

## Checkpoints
User can exit at any step. Progress is not lost:
- Spec saved to ./specs/<name>.json
- Generated code in ./generated/<name>
- Can resume with individual commands
