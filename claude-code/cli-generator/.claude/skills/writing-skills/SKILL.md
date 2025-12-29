---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work correctly. Provides the methodology for effective skill authoring.
---

# Writing Skills

## Core Principle

Apply TDD to skill creation: write the test scenario first, then write the skill to pass it.

## The RED-GREEN-REFACTOR Cycle for Skills

### RED: Define the Test Scenario
Before writing ANY skill content:
1. Write a specific prompt that SHOULD trigger this skill
2. Write what Claude SHOULD do when the skill activates
3. Write what Claude should NOT do

Example test scenario:
```
TRIGGER: "Help me debug why my CLI command isn't working"
EXPECTED: Claude uses systematic 4-phase debugging approach
NOT EXPECTED: Claude immediately suggests fixes without investigation
```

### GREEN: Write Minimal Skill
Write just enough in SKILL.md to pass your test scenario.
- Start with frontmatter (name, description)
- Add the core methodology
- Include explicit "do not" instructions

### REFACTOR: Improve Based on Usage
After testing with real prompts:
- Tighten descriptions if skill triggers incorrectly
- Add examples if Claude misinterprets instructions
- Remove content Claude already knows

## Skill Quality Checklist

Before considering a skill complete:
- [ ] Test scenario written BEFORE skill content
- [ ] Description includes WHAT and WHEN
- [ ] Explicit "Do NOT" section included
- [ ] Tested in fresh Claude Code session
- [ ] Asked Claude "What was unclear?" after use

## Red Flags (Restart Required)

- Writing skill content before test scenario
- Skill that triggers on first try without testing
- No "Do NOT" section
- Description uses first person ("I help...")
