# Solution Architecture

## Input

Meeting notes copied from:

- Teams meeting recap
- OneNote notes
- Word meeting minutes
- Loop notes

## Processing

The agent:

1. Reads meeting notes
2. Identifies:
   - Decisions
   - Action items
   - Owners
   - Due dates
   - Dependencies
3. Converts them into structured tasks
4. Generates a task table
5. Optionally outputs JSON, CSV, Planner format, or Markdown

## Output Formats

| Format | Use Case |
|--------|----------|
| Markdown | Documentation, Git commits |
| JSON | API integration, data storage |
| CSV | Excel, spreadsheet tools |
| Planner | Microsoft Project integration |
