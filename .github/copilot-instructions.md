# Repository Instructions for GitHub Copilot

These instructions guide GitHub Copilot's behavior when working on the Meeting-Notes-to-Actions Agent repository.

## Core Behaviors

Always:

1. **Extract action items** from meeting discussions
   - Identify all tasks, deliverables, and action points
   - Look for implicit actions (e.g., "we need to fix this" → action item)

2. **Identify owners** whenever possible
   - Assign specific people to each action item
   - Flag when owner is unclear or missing
   - Suggest owner if context implies responsibility

3. **Normalize task descriptions**
   - Convert vague descriptions to clear, actionable tasks
   - Use consistent terminology
   - Ensure descriptions are specific and measurable

4. **Create concise task titles**
   - Keep titles under 10 words
   - Use action verbs (Investigate, Deploy, Create, etc.)
   - Make titles self-explanatory

5. **Detect due dates**
   - Extract explicit dates (e.g., "Friday at 5 PM")
   - Infer implied deadlines (e.g., "ASAP" → Today)
   - Normalize to ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
   - Flag ambiguous dates (e.g., "next week" → ask for clarification)

6. **Categorize priority levels**
   - **P1 / Critical**: Production issues, SLA violations, security
   - **P2 / High**: Important but non-blocking
   - **Normal**: Standard priority items
   - Consider ticket number (P1, P2) when provided

7. **Highlight blockers and dependencies**
   - Identify tasks that block other tasks
   - List prerequisites before starting a task
   - Warn if circular dependencies exist
   - Show dependency chains when relevant

## Language & Style

- Use **business language**, not technical jargon when documenting for non-technical stakeholders
- Use **technical precision** when writing code or for technical teams
- Be **direct and concise** in all communications
- **Avoid ambiguity** - ask for clarification if needed

## Output Format

**Output tables whenever possible** for:
- Action item summaries
- Team assignments
- Priority breakdowns
- SLA tracking
- Dependency relationships

Use markdown tables:
```markdown
| Item | Owner | Due Date | Priority | Status |
|------|-------|----------|----------|--------|
| ... | ... | ... | ... | ... |
```

## Code Generation Guidelines

When generating code for this repository:

1. **Follow existing patterns** in `tests/conftest.py` and `tests/test_agent.py`
2. **Write tests first** - TDD approach
3. **Maintain 80%+ coverage** target
4. **Document with docstrings** using Google-style format
5. **Use type hints** for function parameters and return values
6. **Handle edge cases** - None values, empty strings, malformed input

### Example Code Structure

```python
"""Module docstring explaining purpose."""

def function_name(param1: str, param2: int = None) -> dict:
    """
    Function docstring with description.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: None)
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When input is invalid
    """
    # Implementation
    pass
```

## Testing Guidelines

- Create test fixtures in `tests/conftest.py`
- Group related tests in test classes
- Use descriptive test names: `test_<action>_<condition>_<expected_result>`
- Test both happy path and edge cases
- Mock external dependencies

## Documentation Guidelines

- Keep READMEs focused and beginner-friendly
- Use USAGE_GUIDE.md for step-by-step instructions
- Add examples with real meeting note samples
- Include troubleshooting sections
- Link between related documentation files

## Team Assignment Rules

When assigning action items to teams:

### Operations Team
- Creating reports (daily, weekly, monthly)
- Sending emails and notifications
- Customer communications
- Escalation notifications
- Status updates to stakeholders

### Technical Team
- Troubleshooting and diagnostics
- Investigation of issues
- Fixing bugs and deploying fixes
- Resolving tickets
- SLA escalations (after 48 hours for P1)

**Default Rule**: If task contains keywords like "report", "email", "send", "notify" → Operations. If contains "diagnose", "investigate", "fix", "deploy", "troubleshoot" → Technical.

## SLA Handling

P1 Ticket Rules:
- Must be resolved within 48 hours
- If approaching 48h (< 6 hours remaining) → flag as "Critical - Approaching SLA"
- If past 48h → flag as "Escalated - SLA Violated"
- Operations must send notification when escalated
- Technical must escalate to senior engineering

P2 Ticket Rules:
- Must be resolved within 5 business days
- Monitor status weekly
- Escalate if approaching deadline

## Quality Checks

Before suggesting completion, verify:
- [ ] All action items have owners
- [ ] All action items have due dates
- [ ] Priority levels are consistent
- [ ] Dependencies are clearly marked
- [ ] Team assignments are correct
- [ ] Output formats are valid (JSON, CSV, Markdown)
- [ ] No critical information is missing

## File Organization

Maintain this structure:
```
meeting-notes-agent/
├── README.md
├── ARCHITECTURE.md
├── TESTING.md
├── USAGE_GUIDE.md
├── requirements-test.txt
├── .github/
│   └── copilot-instructions.md (this file)
├── samples/
│   ├── daily_standup_sept2.txt
│   ├── weekly_review_aug28.txt
│   └── expected_output_*.{json,csv}
├── tests/
│   ├── conftest.py
│   └── test_agent.py
└── src/ (to be created)
    ├── parser.py
    ├── extractor.py
    ├── team_router.py
    └── formatters.py
```

## Helpful Shortcuts

When working in this repo:
- Type `@meeting-notes-agent` to reference the project
- Reference sample files: `samples/daily_standup_sept2.txt`
- Run tests: `pytest tests/ -v`
- Check coverage: `pytest tests/ -v --cov=src`

## Common Patterns

### Pattern: Parsing Meeting Notes
1. Extract meeting metadata (title, date, attendees)
2. Identify sections (topics, decisions, action items)
3. For each action item: extract title, owner, due date, priority
4. Identify dependencies between items
5. Assign to team based on keywords

### Pattern: Creating Output
1. Collect structured action items
2. Format based on requested output type (JSON, CSV, Markdown)
3. Add metadata (meeting info, summary statistics)
4. Validate output format is correct
5. Return or export to file

### Pattern: Team Assignment
1. Scan task title and description for keywords
2. Match against Operations keywords vs Technical keywords
3. Default to most likely team
4. Flag if ambiguous
5. Check for special cases (escalations → Technical, reports → Operations)

## Escalation Path

If you need clarification:
1. Ask specific questions (don't assume)
2. Provide options: "Should this be P1 or P2?"
3. Reference existing examples: "Like in samples/daily_standup_sept2.txt"
4. Suggest default behavior if unclear

## Success Criteria

Copilot has done well when:
- ✅ All action items are clearly identified
- ✅ Owners are assigned and appropriate
- ✅ Due dates are specific and formatted consistently
- ✅ Priorities match SLA requirements
- ✅ Teams are assigned correctly
- ✅ Dependencies are highlighted
- ✅ Output is in requested format (JSON, CSV, Markdown)
- ✅ Tables are used for summaries
- ✅ Documentation is clear and actionable
- ✅ Code follows project patterns and includes tests
