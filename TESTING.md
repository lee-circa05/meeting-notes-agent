# Testing Strategy - Meeting-Notes-to-Actions Agent

## Test Objectives

1. Validate that meeting notes are correctly parsed
2. Verify action items are assigned to correct teams (Operations/Technical)
3. Ensure all fields (decisions, owners, due dates, dependencies) are extracted
4. Check output formats are valid (JSON, CSV, Markdown)
5. Validate priority (P1/P2) categorization

## Test Categories

### 1. Unit Tests
- **Parser Tests**: Validate individual note parsing
- **Extraction Tests**: Verify identification of decisions, action items, owners, dates
- **Team Assignment Tests**: Ensure correct team routing (Operations vs Technical)
- **Format Tests**: Validate JSON, CSV, Markdown output generation

### 2. Integration Tests
- **End-to-End Flow**: Notes → Parsed → Assigned → Formatted Output
- **Multi-Format Output**: Same input produces valid output in all formats
- **Dependencies Resolution**: Verify linked action items are connected

### 3. Manual Test Cases
- Simple meetings (2-3 action items)
- Complex meetings (multiple teams, dependencies)
- Edge cases (missing dates, unclear owners, malformed notes)

## Test Data

### Sample Scenarios

#### Scenario 1: P1 Ticket Escalation
```
Meeting: Daily Standup - Sept 2, 2026
Attendees: Technical Team, Operations

Note: Database connection issue affecting production
- P1 ticket #12345 opened at 8 AM
- Technical team investigating
- Issue persists > 48 hours
```

**Expected Output:**
- Technical: Troubleshoot #12345 (Due: Today, Priority: P1)
- Technical: Escalate #12345 to Operations (Due: 48h from creation)
- Operations: Send email update on #12345 escalation

#### Scenario 2: Weekly Report Generation
```
Meeting: Weekly Review - Sept 2, 2026
Attendees: Operations, Technical

Topics: P1/P2 ticket status, escalations
```

**Expected Output:**
- Operations: Create weekly report on P1/P2 status (Due: EOW Friday)
- Operations: Send email to stakeholders (Due: EOW Friday)

## Running Tests

### Python Setup
```bash
pip install pytest pytest-cov
pytest tests/ -v
```

### Test Coverage
Aim for:
- Unit tests: 80%+ coverage
- Integration tests: Key workflows covered
- Manual test cases: All major scenarios

## Test Execution Plan

1. **Phase 1**: Set up test framework (Week 1)
2. **Phase 2**: Unit tests for parsing & extraction (Week 1)
3. **Phase 3**: Integration tests for team assignment (Week 2)
4. **Phase 4**: Output format validation (Week 2)
5. **Phase 5**: Manual testing & edge cases (Week 2)

## Success Criteria

✅ All unit tests pass with 80%+ coverage  
✅ Integration tests cover all team workflows  
✅ Manual test cases complete without errors  
✅ Output formats are valid and complete  
✅ Action items correctly routed to Operations/Technical teams  
