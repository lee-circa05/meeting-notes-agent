# Meeting-Actions Agent Definition

**Agent ID:** `meeting-actions`  
**Purpose:** Extract and assign action items from meeting notes  
**Version:** 1.0  
**Status:** Active

---

## Agent Overview

The Meeting-Actions Agent processes meeting notes and converts them into structured, assigned action items for Operations and Technical teams. It handles P1/P2 ticket management, SLA tracking, and dependency resolution.

## Core Capabilities

### 1. Meeting Notes Parsing
- **Input Formats:** Plain text, email, Teams chat, OneNote, Word documents
- **Extract:** Meeting metadata, attendees, topics, decisions, action items
- **Validate:** Completeness and consistency of extracted data

### 2. Action Item Extraction
- Identify action items from narrative meeting notes
- Extract: Title, owner, due date, priority, dependencies
- Normalize: Descriptions to clear, actionable language
- Validate: All required fields present

### 3. Team Assignment
- Route tasks to **Operations** or **Technical** teams
- Keyword matching: "report/email/send" → Operations
- Keyword matching: "diagnose/fix/deploy/troubleshoot" → Technical
- Flag ambiguous assignments for manual review

### 4. Priority & SLA Management
- Categorize: P1 (critical), P2 (high), Normal, Low
- Track: SLA compliance for P1 (48h) and P2 (5d)
- Alert: When approaching or exceeding SLA
- Escalate: Automatic escalation procedures

### 5. Dependency Resolution
- Identify task dependencies and blocking relationships
- Detect: Circular dependencies (flag as error)
- Show: Dependency chains and critical path
- Validate: All referenced tasks exist

### 6. Output Formatting
- Generate: JSON, CSV, Markdown, HTML outputs
- Format: Markdown tables for summaries
- Export: Integration formats (Jira, Azure DevOps, Google Sheets)
- Validate: Output format correctness

---

## Input Specification

### Required Input
```yaml
meeting_notes: |
  Plain text or structured meeting notes
  Must include:
  - Meeting title and date
  - Discussion topics or decisions
  - Action items (at least one)
```

### Optional Input
```yaml
format: json              # Output format (default: markdown)
config_file: .config.yml  # Custom configuration
team_override: null       # Manual team assignment
priority_override: null   # Manual priority assignment
```

### Input Validation
- ✓ Meeting notes not empty
- ✓ At least one action item identified
- ✓ Date format valid (ISO 8601 or natural language)
- ✓ Priority values valid (P1, P2, High, Normal, Low)
- ⚠ Flag: Missing owners or due dates
- ⚠ Flag: Ambiguous team assignments
- ✗ Reject: Invalid priority levels
- ✗ Reject: Circular dependencies

---

## Output Specification

### Standard Output (JSON)
```json
{
  "meeting": {
    "title": "string",
    "date": "ISO-8601",
    "attendees": ["string"]
  },
  "decisions": [
    {
      "id": "string",
      "description": "string",
      "priority": "P1|P2|High|Normal"
    }
  ],
  "action_items": [
    {
      "id": "string",
      "title": "string (max 10 words)",
      "team": "Technical|Operations",
      "owner": "string (person name)",
      "due_date": "ISO-8601",
      "priority": "P1|P2|High|Normal",
      "ticket": "string (optional)",
      "description": "string",
      "dependencies": ["string (IDs)"],
      "status": "not_started|in_progress|completed|blocked"
    }
  ],
  "summary": {
    "total_items": number,
    "by_team": { "Technical": number, "Operations": number },
    "by_priority": { "P1": number, "P2": number, "High": number },
    "sla_violations": number,
    "unassigned_items": number
  }
}
```

### CSV Output
```
ID,Title,Team,Owner,Due Date,Priority,Ticket,Description,Dependencies,Status
```

### Markdown Output
```markdown
# Action Items - [Meeting Title]

## Technical Team
- **Item Title** (ID)
  - Owner: [Name]
  - Due: [Date]
  - Priority: [Level]

## Operations Team
...

## Summary
- Total: X items
- Critical (P1): Y items
```

### Output Validation
- ✓ All action items have unique IDs
- ✓ All teams are valid (Technical or Operations)
- ✓ All dates are ISO 8601 format
- ✓ All priorities are valid values
- ✓ All dependencies reference existing items
- ✓ No circular dependencies exist
- ✓ Summary statistics match actual counts

---

## Team Assignment Logic

### Operations Team (Decision Tree)

```
Is the task about:
  ├─ Creating a report (daily/weekly/monthly)? → YES
  ├─ Sending an email/notification? → YES
  ├─ Customer communication? → YES
  ├─ Escalation notification? → YES
  ├─ Status update? → YES
  └─ Otherwise → Check Technical Team
```

**Operations Keywords:**
- report, create report, generate report
- email, send email, notification
- communication, inform, update, notify
- escalation (notification only)
- weekly, daily, monthly (in context of reporting)

### Technical Team (Decision Tree)

```
Is the task about:
  ├─ Troubleshooting/diagnosing an issue? → YES
  ├─ Investigating root cause? → YES
  ├─ Fixing a bug or deploying a fix? → YES
  ├─ Escalating to senior engineering? → YES
  ├─ Performance analysis? → YES
  └─ Otherwise → Flag as ambiguous
```

**Technical Keywords:**
- diagnose, troubleshoot, investigate, diagnose
- fix, repair, resolve, patch, deploy
- escalate (to engineering)
- check, analyze, review (in technical context)

### Ambiguity Resolution

If team assignment is unclear:
1. Ask for clarification (if interactive)
2. Use secondary keywords to refine
3. Default to Technical if involving ticket resolution
4. Flag for manual review
5. Suggest both teams if truly ambiguous

---

## Priority Categorization

### P1 - Critical/Urgent
**Criteria:**
- Production system down or degraded
- Security vulnerability
- SLA violation
- Customer-impacting issue
- Payment/revenue affecting
- Data loss risk

**SLA:** 48 hours to resolve  
**Escalation:** After 48 hours → Escalate to VP Engineering  
**Notification:** Operations sends email on escalation

### P2 - High Priority
**Criteria:**
- Important business impact
- Non-blocking issue
- Moderate customer impact
- Performance degradation
- Workaround available

**SLA:** 5 business days to resolve  
**Escalation:** After 4 days → Escalate to team lead  
**Notification:** Weekly status update required

### High / Normal - Standard Priority
**Criteria:**
- Routine tasks
- Feature requests
- Process improvements
- Non-urgent enhancements

**SLA:** None (team discretion)  
**Notification:** As scheduled

### Automatic Priority Detection
```
IF ticket_id contains "P1" → P1
ELSE IF mentioned "production down" → P1
ELSE IF mentioned "SLA violation" → P1
ELSE IF ticket_id contains "P2" → P2
ELSE IF mentioned "important but" → P2
ELSE IF mentioned "urgent" → High
ELSE → Normal (default)
```

---

## SLA & Escalation Rules

### P1 Ticket Timeline

```
T+0h:   Ticket opened
        → Technical team notified
        → Action item created (Priority: P1)

T+24h:  P1 still open
        → Team lead notified
        → Flag: "Approaching SLA (24h remaining)"

T+42h:  P1 still open (< 6h to SLA)
        → VP Engineering notified
        → Flag: "Critical - Approaching SLA"

T+48h:  P1 unresolved (SLA violated)
        → Escalation triggered
        → Operations sends escalation email
        → Action item: "Escalate #TICKET to senior engineering"
        → Technical: Create urgent escalation task

T+48h+: P1 in escalation status
        → Daily updates required
        → CEO/Executive notification if critical
```

### P2 Ticket Timeline

```
T+0d:   Ticket opened
        → Action item created (Priority: P2)

T+3d:   P2 still open (1 day to SLA)
        → Team lead notified
        → Flag: "Approaching SLA"

T+5d:   P2 unresolved (SLA violated)
        → Flag: "SLA Violated"
        → Operations: Weekly report includes missed SLA
        → No automatic escalation for P2

T+5d+:  P2 in violation
        → Weekly reports track status
```

### Escalation Actions

**When escalating P1:**
1. Create escalation task: "Escalate [TICKET] to senior engineering"
2. Assign to: VP Engineering or Team Lead
3. Priority: P1
4. Due: Immediate (EOD same day)
5. Operations: Create task "Send escalation email to stakeholders"

**When approaching SLA:**
1. Flag in output with warning emoji (⚠️)
2. Include in summary section
3. Create reminder task for team lead
4. Send automated reminder email

---

## Dependency Management

### Dependency Types

```
blocks_by: Task A blocks Task B (B cannot start until A is done)
depends_on: Task B depends on Task A (same as above, reversed)
related_to: Tasks are related but not blocking
triggers: Task A triggers Task B (automatically)
```

### Dependency Resolution

**Valid Dependency:**
- All referenced task IDs exist
- No circular dependencies (A→B→C→A)
- Clear causality relationship

**Invalid Dependency:**
- Reference to non-existent task → Error
- Circular dependency detected → Error
- Unclear relationship → Warning

**Circular Dependency Detection:**
```python
def has_circular_dependency(task_id, dependencies, visited=None):
    if visited is None:
        visited = set()
    
    if task_id in visited:
        return True  # Circular found
    
    visited.add(task_id)
    
    for dep_id in dependencies[task_id]:
        if has_circular_dependency(dep_id, dependencies, visited.copy()):
            return True
    
    return False
```

### Critical Path Calculation

Show dependencies that form critical path:
```
AI-001 → AI-002 → AI-003 → AI-004
(4 items in critical path)
```

---

## Error Handling

### Recoverable Errors (Warnings)

| Error | Handling | Output |
|-------|----------|--------|
| Missing owner | Flag as "Unassigned" | ⚠️ Mark in output |
| Missing due date | Flag as "No due date" | ⚠️ Mark in output |
| Ambiguous team | Default to best guess | ⚠️ Flag for review |
| Unclear date | Request clarification | ⚠️ Prompt user |
| No priority | Default to "Normal" | ⚠️ Mark in output |

### Fatal Errors (Failures)

| Error | Action |
|-------|--------|
| No action items found | Reject input, prompt user |
| Invalid date format | Reject and request clarification |
| Invalid priority value | Reject and show valid options |
| Circular dependencies | Reject and highlight circular chain |
| Empty input | Reject with error message |

### Error Messages

```
ERROR: No action items found in meeting notes.
Please ensure notes include:
- Specific tasks with owners
- Due dates or timeframes
- Clear descriptions

Example:
  John - Investigate database issue - due TODAY at 1 PM
```

---

## Configuration

### Default Configuration

```yaml
# output settings
default_output_format: markdown
include_summary: true
include_decisions: true
include_dependencies: true
group_by_team: true

# team assignment
team_keywords:
  technical:
    - diagnose
    - investigate
    - troubleshoot
    - fix
    - deploy
    - escalate
    - check
    - resolve
  operations:
    - report
    - create report
    - email
    - send
    - notification
    - communication
    - update
    - notify

# sla settings
sla:
  p1_hours: 48
  p2_days: 5

# alert thresholds
alert_thresholds:
  p1_warning_hours: 6    # Alert when < 6 hours to SLA
  p2_warning_days: 1     # Alert when < 1 day to SLA
```

### Custom Configuration File

Users can create `.meeting-agent-config.yml` to override defaults.

---

## Agent Behavior Standards

### Do's ✅

- ✅ Extract all action items from notes
- ✅ Assign owners and due dates
- ✅ Use consistent formatting (ISO 8601 dates)
- ✅ Create clear, actionable task titles
- ✅ Identify dependencies and blocking items
- ✅ Flag SLA violations and escalations
- ✅ Use markdown tables for summaries
- ✅ Provide business language for stakeholders
- ✅ Validate all output before returning
- ✅ Ask for clarification on ambiguous items

### Don'ts ❌

- ❌ Leave action items unassigned
- ❌ Use vague task descriptions
- ❌ Assume priorities without clear indicators
- ❌ Create circular dependencies
- ❌ Ignore SLA violations
- ❌ Mix business and technical jargon
- ❌ Output invalid formats (malformed JSON, etc.)
- ❌ Assume team assignments without validation
- ❌ Skip dependency analysis
- ❌ Ignore error conditions

---

## Quality Assurance

### Pre-Output Validation

```python
def validate_output(action_items, decisions):
    checks = {
        "unique_ids": len(ids) == len(set(ids)),
        "all_have_owners": all(item.owner for item in action_items),
        "all_have_dates": all(item.due_date for item in action_items),
        "valid_teams": all(item.team in ['Technical', 'Operations'] for item in action_items),
        "valid_priorities": all(item.priority in ['P1', 'P2', 'High', 'Normal', 'Low'] for item in action_items),
        "no_circular_deps": not has_circular_dependencies(action_items),
        "valid_format": validate_json_format(output)
    }
    return all(checks.values()), checks
```

### Success Criteria

Agent output is successful when:
- ✅ All action items identified and extracted
- ✅ Owners assigned (or flagged if missing)
- ✅ Due dates specified and formatted correctly
- ✅ Priorities categorized appropriately
- ✅ Teams assigned with high confidence
- ✅ Dependencies clearly marked
- ✅ No circular dependencies
- ✅ Output formats are valid and complete
- ✅ SLA violations highlighted
- ✅ Summary statistics accurate

---

## Integration Points

### External Integrations

- **Jira**: Export as issues via JSON
- **Azure DevOps**: Export as work items
- **Microsoft Project**: Export Planner tasks
- **Google Sheets**: Export to shared spreadsheet
- **Slack**: Send summaries to channels
- **Email**: Send Markdown reports

### API Endpoints (Planned)

```
POST /api/v1/parse
  Input: Meeting notes
  Output: Structured action items

POST /api/v1/assign
  Input: Action items
  Output: Team assignments

GET /api/v1/sla-status
  Output: All SLA violations and escalations

POST /api/v1/export
  Input: Format (json, csv, markdown)
  Output: Formatted data
```

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Parse time | < 2 seconds |
| Average accuracy | > 95% |
| Team assignment accuracy | > 90% |
| SLA detection | 100% |
| Dependency detection | 100% |
| False positives | < 5% |

---

## Change Log

### Version 1.0 (2026-09-02)
- Initial agent definition
- Core parsing and extraction
- Team assignment logic
- SLA/priority handling
- Output formatting
- Error handling

