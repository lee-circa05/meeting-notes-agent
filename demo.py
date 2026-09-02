"""
Quick demo of Meeting-Notes-to-Actions Agent
"""

from src.parser import MeetingNotesParser
from src.formatters import OutputFormatter


def main():
    """Run a quick demo of the agent."""
    
    # Sample meeting notes
    meeting_notes = """
    Meeting: Daily Standup - September 2, 2026
    Date: 2026-09-02
    Attendees: Sarah Chen, Mike Rodriguez, John Smith, Lisa Wang
    
    P1 ISSUE - Database Connection Pool:
    John - Diagnose database issue #DB-12345 - TODAY 1 PM - P1
    Sarah - Check connection pool logs - TODAY 12 PM - P1
    
    Mike - Prepare customer notification if needed - TODAY 2 PM - P1
    
    P2 ISSUE - Authentication Service:
    John - Investigate AUTH-6789 service latency - TOMORROW 5 PM - P2
    Lisa - Send status update email to stakeholders - TODAY 4 PM - P2
    
    WEEKLY REPORTING:
    Mike - Create weekly P1/P2 ticket status report - FRIDAY 5 PM - High
    Lisa - Send weekly report to leadership - FRIDAY 6 PM - High
    """
    
    print("=" * 60)
    print("Meeting-Notes-to-Actions Agent - Quick Demo")
    print("=" * 60)
    print()
    
    # Parse meeting notes
    print("1. Parsing meeting notes...")
    parser = MeetingNotesParser(meeting_notes)
    structured_data = parser.parse()
    
    print(f"   ✓ Extracted {len(structured_data['action_items'])} action items")
    print(f"   ✓ Extracted {len(structured_data['decisions'])} decisions")
    print()
    
    # Display summary
    summary = structured_data['summary']
    print("2. Summary Statistics:")
    print(f"   Total Items: {summary['total_items']}")
    print(f"   Technical Team: {summary['by_team']['Technical']} items")
    print(f"   Operations Team: {summary['by_team']['Operations']} items")
    print(f"   P1 (Critical): {summary['by_priority']['P1']} items")
    print(f"   P2 (High): {summary['by_priority']['P2']} items")
    print()
    
    # Show action items
    print("3. Action Items by Team:")
    print()
    
    formatter = OutputFormatter(structured_data)
    
    # Technical items
    technical_items = [i for i in structured_data['action_items'] if i['team'] == 'Technical']
    if technical_items:
        print("   Technical Team:")
        for item in technical_items:
            print(f"   - [{item['priority']}] {item['title']}")
            print(f"     Owner: {item['owner']}, Due: {item['due_date']}")
        print()
    
    # Operations items
    operations_items = [i for i in structured_data['action_items'] if i['team'] == 'Operations']
    if operations_items:
        print("   Operations Team:")
        for item in operations_items:
            print(f"   - [{item['priority']}] {item['title']}")
            print(f"     Owner: {item['owner']}, Due: {item['due_date']}")
        print()
    
    # Show formatted outputs
    print("4. Output Formats Available:")
    print()
    
    print("   Markdown Output (excerpt):")
    md_output = formatter.to_markdown()
    print("   " + "\n   ".join(md_output.split('\n')[:15]))
    print("   ...")
    print()
    
    print("   JSON Output (excerpt):")
    json_output = formatter.to_json()
    print("   " + "\n   ".join(json_output.split('\n')[:10]))
    print("   ...")
    print()
    
    print("   CSV Output (excerpt):")
    csv_output = formatter.to_csv()
    print("   " + "\n   ".join(csv_output.split('\n')[:4]))
    print("   ...")
    print()
    
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("1. Run tests: python run_tests.bat")
    print("2. Process files: python main.py --input samples/daily_standup_sept2.txt --format markdown")
    print("3. See usage guide: USAGE_GUIDE.md")
    print()


if __name__ == '__main__':
    main()
