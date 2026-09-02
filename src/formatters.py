"""
Output formatter module.

Formats structured action items into various output formats.
"""

import json
import csv
from io import StringIO
from typing import Dict, List, Any


class OutputFormatter:
    """Format structured action items into various output formats."""
    
    def __init__(self, structured_data: Dict[str, Any]):
        """
        Initialize formatter with structured data.
        
        Args:
            structured_data: Dictionary with meeting data from parser
        """
        self.data = structured_data
    
    def to_json(self) -> str:
        """
        Convert to JSON format.
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.data, indent=2, default=str)
    
    def to_csv(self) -> str:
        """
        Convert action items to CSV format.
        
        Returns:
            CSV string with action items
        """
        items = self.data.get('action_items', [])
        if not items:
            return ""
        
        # Get all unique keys from action items
        fieldnames = set()
        for item in items:
            fieldnames.update(item.keys())
        fieldnames = sorted(list(fieldnames))
        
        # Create CSV output
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in items:
            # Convert lists to semicolon-separated strings
            row = {}
            for field in fieldnames:
                value = item.get(field, '')
                if isinstance(value, list):
                    row[field] = ';'.join(str(v) for v in value)
                else:
                    row[field] = value
            writer.writerow(row)
        
        return output.getvalue()
    
    def to_markdown(self) -> str:
        """
        Convert to Markdown format with tables.
        
        Returns:
            Markdown string representation
        """
        lines = []
        
        # Add meeting header
        meeting = self.data.get('meeting', {})
        lines.append(f"# Action Items - {meeting.get('title', 'Meeting')}\n")
        lines.append(f"**Date:** {meeting.get('date', 'Unknown')}\n")
        
        if meeting.get('attendees'):
            lines.append(f"**Attendees:** {', '.join(meeting['attendees'])}\n")
        
        # Add summary
        summary = self.data.get('summary', {})
        lines.append("## Summary\n")
        lines.append(f"- **Total Items:** {summary.get('total_items', 0)}\n")
        
        by_team = summary.get('by_team', {})
        if by_team:
            lines.append(f"- **Technical:** {by_team.get('Technical', 0)} items\n")
            lines.append(f"- **Operations:** {by_team.get('Operations', 0)} items\n")
        
        by_priority = summary.get('by_priority', {})
        if by_priority:
            p1_count = by_priority.get('P1', 0)
            p2_count = by_priority.get('P2', 0)
            if p1_count > 0:
                lines.append(f"- **P1 (Critical):** {p1_count} items\n")
            if p2_count > 0:
                lines.append(f"- **P2 (High):** {p2_count} items\n")
        
        lines.append("")
        
        # Group by team
        items = self.data.get('action_items', [])
        
        # Technical items
        technical_items = [i for i in items if i.get('team') == 'Technical']
        if technical_items:
            lines.append("## Technical Team\n")
            lines.append(self._create_markdown_table(technical_items))
            lines.append("")
        
        # Operations items
        operations_items = [i for i in items if i.get('team') == 'Operations']
        if operations_items:
            lines.append("## Operations Team\n")
            lines.append(self._create_markdown_table(operations_items))
            lines.append("")
        
        # Decisions
        decisions = self.data.get('decisions', [])
        if decisions:
            lines.append("## Key Decisions\n")
            for decision in decisions:
                priority = decision.get('priority', 'Normal')
                lines.append(f"- **[{priority}]** {decision.get('description', 'Unknown decision')}\n")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _create_markdown_table(self, items: List[Dict[str, Any]]) -> str:
        """
        Create markdown table for action items.
        
        Args:
            items: List of action items
            
        Returns:
            Markdown table string
        """
        if not items:
            return ""
        
        lines = []
        
        # Table header
        lines.append("| ID | Title | Owner | Due Date | Priority | Status |")
        lines.append("|--|--|--|--|--|--|")
        
        # Table rows
        for item in items:
            item_id = item.get('id', '')
            title = item.get('title', '')[:40]  # Truncate long titles
            owner = item.get('owner', 'Unassigned')
            due_date = item.get('due_date', 'No date')
            
            # Format due date
            if due_date and isinstance(due_date, str):
                if 'T' in due_date:  # ISO format
                    due_date = due_date.split('T')[0]  # Just date
            
            priority = item.get('priority', 'Normal')
            status = item.get('status', 'not_started').replace('_', ' ')
            
            lines.append(f"| {item_id} | {title} | {owner} | {due_date} | {priority} | {status} |")
        
        return '\n'.join(lines)
    
    def to_html(self) -> str:
        """
        Convert to HTML format.
        
        Returns:
            HTML string representation
        """
        meeting = self.data.get('meeting', {})
        items = self.data.get('action_items', [])
        summary = self.data.get('summary', {})
        
        html = ['<!DOCTYPE html>']
        html.append('<html><head>')
        html.append('<meta charset="utf-8">')
        html.append(f"<title>{meeting.get('title', 'Meeting Notes')}</title>")
        html.append('<style>')
        html.append('body { font-family: Arial, sans-serif; margin: 20px; }')
        html.append('h1 { color: #333; }')
        html.append('table { border-collapse: collapse; width: 100%; }')
        html.append('th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }')
        html.append('th { background-color: #4CAF50; color: white; }')
        html.append('tr:nth-child(even) { background-color: #f2f2f2; }')
        html.append('.p1 { background-color: #ffcccc; }')
        html.append('.p2 { background-color: #ffffcc; }')
        html.append('.summary { background-color: #e8f4f8; padding: 10px; border-radius: 5px; }')
        html.append('</style>')
        html.append('</head><body>')
        
        # Header
        html.append(f"<h1>{meeting.get('title', 'Meeting')}</h1>")
        html.append(f"<p><strong>Date:</strong> {meeting.get('date', 'Unknown')}</p>")
        
        if meeting.get('attendees'):
            html.append(f"<p><strong>Attendees:</strong> {', '.join(meeting['attendees'])}</p>")
        
        # Summary
        html.append('<div class="summary">')
        html.append(f"<h2>Summary</h2>")
        html.append(f"<p>Total Items: {summary.get('total_items', 0)}</p>")
        by_team = summary.get('by_team', {})
        if by_team:
            html.append(f"<p>Technical: {by_team.get('Technical', 0)}, Operations: {by_team.get('Operations', 0)}</p>")
        html.append('</div>')
        
        # Action items table
        html.append('<h2>Action Items</h2>')
        html.append('<table>')
        html.append('<tr><th>ID</th><th>Title</th><th>Team</th><th>Owner</th><th>Due</th><th>Priority</th><th>Status</th></tr>')
        
        for item in items:
            priority_class = 'p1' if item.get('priority') == 'P1' else 'p2' if item.get('priority') == 'P2' else ''
            html.append(f"<tr class='{priority_class}'>")
            html.append(f"<td>{item.get('id', '')}</td>")
            html.append(f"<td>{item.get('title', '')}</td>")
            html.append(f"<td>{item.get('team', '')}</td>")
            html.append(f"<td>{item.get('owner', '')}</td>")
            html.append(f"<td>{item.get('due_date', '')}</td>")
            html.append(f"<td>{item.get('priority', '')}</td>")
            html.append(f"<td>{item.get('status', '')}</td>")
            html.append('</tr>')
        
        html.append('</table>')
        html.append('</body></html>')
        
        return '\n'.join(html)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Return as dictionary (structured output).
        
        Returns:
            Dictionary representation of data
        """
        return self.data
