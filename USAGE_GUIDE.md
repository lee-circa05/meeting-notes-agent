# How to Use the Meeting-Notes-to-Actions Agent

A step-by-step guide for converting meeting notes into actionable tasks.

## Quick Start (5 minutes)

### Step 1: Prepare Your Meeting Notes

Copy your meeting notes from Teams, OneNote, Word, or Loop. The agent works best with notes that include:
- Meeting title and date
- Attendees
- Discussion topics
- Action items with owners and due dates
- Key decisions

**Example:**
```
Daily Standup - September 2, 2026

Attendees: Sarah, Mike, John, Lisa

Database Issue (P1):
- Connection pool exhaustion affecting payments
- Owner: John - due TODAY at 1 PM
- Escalate to senior DBA if not resolved

Weekly Report:
- Mike to create P1/P2 status report
- Due Friday at 5 PM
- Lisa to send to leadership by 6 PM
```

### Step 2: Run the Agent

```bash
# Using Python
python -m meeting_agent --input notes.txt --output results.json

# Or using CLI interface
python -m meeting_agent --input notes.txt --format json,csv,markdown
```

### Step 3: Review the Output

The agent generates three key outputs:

**JSON Format** (for APIs and data processing):
```json
{
  "action_items": [
    {
      "id": "AI-001",
      "title": "Diagnose database issue",
      "team": "Technical",
      "owner": "John",
      "due_date": "2026-09-02T13:00:00",
      "priority": "P1"
    }
  ],
  "decisions": [...]
}
```

**CSV Format** (for spreadsheets):
```
ID,Title,Team,Owner,Due Date,Priority
AI-001,Diagnose database issue,Technical,John,2026-09-02T13:00:00,P1
```

**Markdown Format** (for documentation):
```markdown
# Action Items

## Technical Team
- **Diagnose database issue**
  - Owner: John
  - Due: 2026-09-02T13:00:00
  - Priority: P1
```

### Step 4: Share or Track Results

- Import CSV into your project management tool (Jira, Azure DevOps, etc.)
- Email the Markdown version to teams
- Use JSON output for automated processing
- Track in Excel or Google Sheets

---

## Detailed Usage Guide

### Scenario 1: Daily Standup Processing

**Time Required:** 10 minutes total

#### Step 1: Capture Notes During Meeting

During the meeting, capture:
1. **Issue/Topic** - What was discussed?
2. **Owner** - Who is responsible?
3. **Due Date** - When must it be done?
4. **Priority** - P1 (urgent) or P2 (normal)?
5. **Dependencies** - What blocks this task?

**Example Capture:**
```
Meeting: Daily Standup - Sept 2, 9:00 AM

🚨 P1 ISSUE - Database Connection Pool
- Problem: Exhaustion affecting payment processing
- Impact: 2% of transactions failing
- Opened: Sept 2, 8:00 AM
- Troubleshoot: John, due TODAY 1:00 PM
- Check logs: Sarah, due TODAY 12:00 PM
- Customer notification: Mike, depends on diagnosis
- Priority: P1 - needs escalation to DBA if not resolved by 1 PM

📋 WEEKLY REPORT
- Create report: Mike, due Friday 5 PM (gather all P1/P2 status)
- Send to leadership: Lisa, due Friday 6 PM (depends on report)
- Priority: High
```

#### Step 2: Save Notes to File

Save as `daily_standup_sept2.txt` or copy to the agent interface.

#### Step 3: Run the Agent

```bash
python -m meeting_agent \
  --input daily_standup_sept2.txt \
  --format json,csv,markdown \
  --output-dir results/
```

#### Step 4: Check Assignment

Verify teams were assigned correctly:
- ✅ **Technical Team:** Troubleshoot, investigate, diagnose, deploy
- ✅ **Operations Team:** Report, email, notification, communication

#### Step 5: Review Action Items

Check the output:
```
Tasks Identified: 7
- Technical Team: 3 items
- Operations Team: 4 items

Priority Breakdown:
- P1 (Critical): 5 items
- P2 (Normal): 2 items
```

#### Step 6: Export and Distribute

- **To Jira:** Import CSV, create tickets
- **To Teams:** Send Markdown in channel
- **To Excel:** Open CSV file
- **To API:** Use JSON output

#### Step 7: Track Progress

Update status as tasks are completed:
```
✅ AI-001: Sarah checked logs at 11:45 AM - pool usage at 95%
✅ AI-002: John identified connection leak in payment module at 12:30 PM
🔄 AI-003: Fix deployed to staging, testing in progress
```

---

### Scenario 2: Weekly Ticket Review

**Time Required:** 20 minutes

#### Step 1: Gather Weekly Data

Collect all meeting notes and incidents from the week:
- Monday daily standup
- Wednesday incident report
- Friday ticket review
- Escalations logged
- Customer issues reported

#### Step 2: Consolidate Notes

```
WEEKLY REVIEW - Aug 28, 2026

P1 ESCALATIONS:
- #DB-11111: Opened Aug 26 - NOW 52 HOURS (past SLA)
  -> Must escalate today to senior engineering
  -> Operations needs to notify VP Engineering

- #API-22222: Opened Aug 27 - NOW 45 HOURS (approaching SLA)
  -> Fix in staging, deploy if tests pass
  -> If not fixed by tomorrow morning, escalate

P2 ITEMS:
- #UI-33333: Dashboard performance - 36 hours (within SLA)

WEEKLY REPORTS:
- Mike: Compile all P1/P2 ticket status by Friday 5 PM
- Lisa: Send report to leadership by Friday 6 PM
- Escalations summary: Include in report
```

#### Step 3: Run Agent

```bash
python -m meeting_agent \
  --input weekly_review_aug28.txt \
  --priority p1,escalation \
  --output weekly_results.json
```

#### Step 4: Review SLA Violations

Agent identifies:
```
⚠️  SLA VIOLATIONS (P1 > 48 hours):
   - #DB-11111: 52 hours - ESCALATE IMMEDIATELY
   
⚠️  APPROACHING SLA (P1 < 6 hours remaining):
   - #API-22222: 45 hours - 3 hours remaining
```

#### Step 5: Generate Reports

Agent creates ready-to-send reports:

**Management Summary:**
```
Weekly Ticket Report - Aug 28 - Sep 3

P1 Tickets: 2
- 1 Escalated (beyond 48h)
- 1 Critical (6h to SLA)

P2 Tickets: 1
- All within SLA

Actions Taken:
- Escalation notification sent to VP Engineering
- Fix deployed to staging for #API-22222
- Dashboard performance investigation started
```

#### Step 6: Send to Stakeholders

```bash
# Generate HTML email version
python -m meeting_agent \
  --input weekly_review_aug28.txt \
  --format html \
  --output weekly_report.html

# Send via email
Send weekly_report.html to: leadership@company.com
```

---

## Advanced Usage

### Configuration File

Create `.meeting-agent-config.yml`:

```yaml
# Default output formats
output_formats:
  - json
  - csv
  - markdown

# Team keywords (for auto-assignment)
technical_keywords:
  - diagnose
  - investigate
  - troubleshoot
  - deploy
  - fix
  - escalate

operations_keywords:
  - report
  - email
  - notification
  - communication
  - send

# SLA thresholds
sla:
  p1_hours: 48
  p2_days: 5

# Alert thresholds
alerts:
  p1_warning_hours: 24  # Alert when < 24 hours to SLA
  p2_warning_days: 1    # Alert when < 1 day to SLA

# Output options
output:
  include_summary: true
  include_decisions: true
  include_dependencies: true
  group_by_team: true
```

Run with config:
```bash
python -m meeting_agent \
  --config .meeting-agent-config.yml \
  --input notes.txt
```

### Batch Processing

Process multiple meetings at once:

```bash
python -m meeting_agent \
  --input-dir meeting_notes/ \
  --output-dir results/ \
  --format json,csv
```

Processes all `.txt` files in `meeting_notes/` and generates results for each.

### Integration with External Tools

**Export to Jira:**
```bash
python -m meeting_agent \
  --input notes.txt \
  --output-format jira \
  --jira-url https://jira.company.com \
  --jira-project TECH
```

**Export to Azure DevOps:**
```bash
python -m meeting_agent \
  --input notes.txt \
  --output-format azure-devops \
  --azure-org myorg \
  --azure-project MyProject
```

**Push to Google Sheets:**
```bash
python -m meeting_agent \
  --input notes.txt \
  --output-format google-sheets \
  --sheets-id <spreadsheet-id>
```

---

## Best Practices

### 1. Consistent Note Format

Use this template for best results:

```
Meeting: [Title] - [Date]
Attendees: [Names]

DECISION 1: [What was decided?]

ACTION ITEM 1:
- Title: [What needs to be done?]
- Owner: [Who?]
- Due: [When?]
- Priority: [P1/P2 or High/Normal]
- Depends on: [Blocking items]
```

### 2. Clear Ownership

Always assign owners:
- ❌ "Database needs to be fixed"
- ✅ "John will diagnose database issue by 1 PM"

### 3. Specific Due Dates

Include concrete times:
- ❌ "Fix this week"
- ✅ "Friday, Sept 6 at 5 PM"

### 4. Priority Levels

Use consistently:
- **P1** - Production critical, must resolve within 48 hours
- **P2** - Important but not blocking, resolve within 5 days
- **High** - Non-ticket items that are urgent
- **Normal** - Standard priority

### 5. Link Dependencies

Show task relationships:
- ❌ "Someone will eventually fix this and report it"
- ✅ "John fixes (AI-001) → Sarah tests (AI-002) → Mike reports (AI-003)"

### 6. Regular Reviews

Schedule reviews:
- **Daily:** Review standup tasks by end of day
- **Weekly:** Review all P1/P2 tickets and escalations
- **Monthly:** Trend analysis and process improvement

---

## Troubleshooting

### Issue: Tasks Not Assigned to Correct Team

**Solution:** Update team keywords in config file or use explicit team markers:
```
[TECHNICAL] John will troubleshoot the database issue
[OPERATIONS] Mike will send status update email
```

### Issue: Due Dates Not Captured

**Solution:** Use explicit date format:
```
Due: 2026-09-02 at 1:00 PM
Due: Today by EOD
Due: Friday, September 6 at 5 PM
```

### Issue: Dependencies Not Recognized

**Solution:** Use explicit dependency notation:
```
Depends on: AI-001, AI-002
Blocked by: Weekly report completion
Unblocks: Production deployment
```

### Issue: Missing Action Items

**Solution:** Ensure items have all required fields:
- Title: Clear description
- Owner: Specific person name
- Due Date: Specific date/time
- Priority: P1, P2, High, or Normal

---

## Examples

### Example 1: Simple Daily Standup

**Input File:** `standup_sept2.txt`
```
Daily Standup - September 2, 2026

John - P1 database issue, troubleshoot, due TODAY 1 PM
Sarah - Check connection logs, due TODAY 12 PM
Mike - Prepare customer notification if needed, depends on John
Lisa - Send weekly report, due Friday 5 PM
```

**Output CSV:**
```
ID,Title,Team,Owner,Due,Priority
1,Troubleshoot database,Technical,John,Today 1 PM,P1
2,Check connection logs,Technical,Sarah,Today 12 PM,P1
3,Prepare customer notification,Operations,Mike,Today,P1
4,Send weekly report,Operations,Lisa,Fri 5 PM,High
```

### Example 2: Complex Weekly Review

**Input File:** `weekly_review.txt` (52 lines)
**Output Files:**
- `weekly_review_output.json` (structured data)
- `weekly_review_output.csv` (for tracking)
- `weekly_review_output.md` (for email)
- `SLA_violations.txt` (escalations only)

---

## Support

For issues or questions:
1. Check TESTING.md for test scenarios
2. Review sample files in `samples/`
3. Check logs in `output/logs/`
4. Review configuration examples

