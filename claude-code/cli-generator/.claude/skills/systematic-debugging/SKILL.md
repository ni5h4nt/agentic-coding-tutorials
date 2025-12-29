---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior. Provides a 4-phase methodology that must be followed BEFORE proposing any fixes.
---

# Systematic Debugging

## CRITICAL RULE

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

If you catch yourself proposing a fix before completing Phase 1, STOP and restart.

## Phase 1: Root Cause Investigation

Before ANY fix attempts:
1. Read the COMPLETE error message (not just the first line)
2. Reproduce the issue with a minimal example
3. Check what changed recently (git diff, recent edits)
4. Gather evidence: logs, stack traces, variable values

Checkpoint: Can you explain exactly WHY the error occurs?
- YES → Proceed to Phase 2
- NO → Stay in Phase 1, gather more evidence

## Phase 2: Pattern Analysis

1. Find a WORKING example of similar code
2. Compare working vs broken line-by-line
3. Identify the specific difference
4. Understand dependencies involved

Checkpoint: Can you point to the exact line causing the issue?
- YES → Proceed to Phase 3
- NO → Return to Phase 1

## Phase 3: Hypothesis Testing

1. Form ONE specific hypothesis
2. Make ONE minimal change to test it
3. Run the test
4. If it fails, revert and form new hypothesis

**NEVER stack multiple fixes.** One change at a time.

## Phase 4: Implementation

1. Write a test that reproduces the bug
2. Implement the single fix
3. Verify test passes
4. Check for regressions

## Red Flags (Process Violation)

Stop and restart if you notice:
- Proposing fix without completing Phase 1
- Making multiple changes simultaneously
- "Let me try this..." without hypothesis
- Third fix attempt failed → question architecture

## Why This Works

- Systematic: 15-30 min resolution vs 2-3 hours random attempts
- First-time fix rate: ~95% vs ~40% for guess-and-check
