# /create-cli - Create CLI Using Specialized Agents

Create a complete CLI application by delegating to specialized agents.

## Usage
/create-cli $ARGUMENTS

## Workflow

You have access to these specialized agents in `.claude/agents/`:
- **spec-designer**: Designs CLI structure from natural language
- **code-generator**: Generates Python/Click code from specs
- **test-writer**: Creates comprehensive pytest test suites
- **code-reviewer**: Reviews code quality and suggests improvements

## Process

### Phase 1: Design
Delegate to spec-designer agent:
"Use the spec-designer agent to design a CLI for: $ARGUMENTS"

Wait for the specification and present it to the user for approval.

### Phase 2: Implementation
After spec approval, delegate to code-generator:
"Use code-generator to implement this CLI spec: [spec from phase 1]"

### Phase 3: Testing
Delegate to test-writer:
"Use test-writer to create tests for the generated CLI"

### Phase 4: Review
Finally, delegate to code-reviewer:
"Use code-reviewer to review the generated code and tests"

## Output
Present the final summary:
- Files created
- Test results
- Review findings
- Next steps for the user
