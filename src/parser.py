"""
Meeting notes parser module.

Parses meeting notes and extracts structured data.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class MeetingNotesParser:
    """Parse meeting notes and extract structured action items and decisions."""
    
    def __init__(self, notes_text: str):
        """
        Initialize parser with meeting notes.
        
        Args:
            notes_text: Raw meeting notes text
        """
        self.notes_text = notes_text
        self.action_items: List[Dict[str, Any]] = []
        self.decisions: List[Dict[str, Any]] = []
        self.meeting_metadata: Dict[str, Any] = {}
    
    def parse(self) -> Dict[str, Any]:
        """
        Parse meeting notes and extract structured data.
        
        Returns:
            Dictionary with parsed meeting data
        """
        self.extract_meeting_metadata()
        self.extract_decisions()
        self.extract_action_items()
        self.assign_teams()
        self.validate_action_items()
        
        return self.get_structured_output()
    
    def extract_meeting_metadata(self) -> None:
        """Extract meeting title, date, attendees from notes."""
        # Extract meeting title
        title_match = re.search(r'(?:Meeting|Meeting Title)[:\s]+([^\n]+)', self.notes_text, re.IGNORECASE)
        self.meeting_metadata['title'] = title_match.group(1).strip() if title_match else 'Unknown Meeting'
        
        # Extract date
        date_match = re.search(r'(?:Date|Date:)[:\s]+([^\n]+)', self.notes_text, re.IGNORECASE)
        if date_match:
            self.meeting_metadata['date'] = self._parse_date(date_match.group(1).strip())
        else:
            self.meeting_metadata['date'] = datetime.now().isoformat()
        
        # Extract attendees
        attendees_match = re.search(r'(?:Attendees?|Participants?)[:\s]+([^\n]+(?:\n[^\n]*)*)', self.notes_text, re.IGNORECASE)
        if attendees_match:
            attendees_str = attendees_match.group(1)
            self.meeting_metadata['attendees'] = [a.strip() for a in re.split(r'[,;]|\band\b', attendees_str) if a.strip()]
        else:
            self.meeting_metadata['attendees'] = []
    
    def extract_decisions(self) -> None:
        """Extract key decisions from meeting notes."""
        # Look for decision patterns
        decision_patterns = [
            r'(?:Decision|Decided?)[:\s]+([^\n]+)',
            r'✅\s+([^\n]+)',
            r'DECISION:\s+([^\n]+)'
        ]
        
        decision_id = 1
        for pattern in decision_patterns:
            matches = re.finditer(pattern, self.notes_text, re.IGNORECASE)
            for match in matches:
                decision_text = match.group(1).strip()
                if decision_text and len(decision_text) > 10:  # Filter out noise
                    # Extract priority from decision
                    priority = self._extract_priority(decision_text)
                    
                    decision = {
                        'id': f'DEC-{decision_id:03d}',
                        'description': decision_text,
                        'priority': priority
                    }
                    self.decisions.append(decision)
                    decision_id += 1
    
    def extract_action_items(self) -> None:
        """Extract action items from meeting notes."""
        # Split by common action item delimiters
        item_patterns = [
            r'(?:Action Item|AI|Task|TODO)[:\s]*\n?([^\n]+)',
            r'\|\s*([A-Za-z\s]+?)\s*\|\s*([A-Za-z0-9\s]+?)\s*\|\s*([^\|]+?)\s*\|',  # Table format
            r'^[-•*]\s+(?:\[.\])?\s*([^\n]+)$',  # Bullet points
        ]
        
        action_item_id = 1
        seen_items = set()
        
        # Find all potential action items
        lines = self.notes_text.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines and headers
            if not line or line.startswith('#') or line.startswith('|'):
                continue
            
            # Look for owner patterns (e.g., "John - Task description")
            owner_pattern = r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:-|:)\s+(.+?)(?:\s*(?:by|due|@|until|before))?\s*(?:by|due|@|until|before)?\s*(.*)$'
            match = re.match(owner_pattern, line)
            
            if match:
                owner = match.group(1).strip()
                description = match.group(2).strip()
                due_info = match.group(3).strip() if match.group(3) else ''
                
                # Skip if we've seen this exact item
                item_key = f"{owner}:{description}"
                if item_key in seen_items:
                    continue
                seen_items.add(item_key)
                
                # Extract due date and priority
                due_date = self._parse_due_date(due_info)
                priority = self._extract_priority(f"{description} {due_info}")
                
                # Extract ticket number if present
                ticket_match = re.search(r'#([A-Z]+-\d+)', description)
                ticket = ticket_match.group(1) if ticket_match else None
                
                # Create action item
                action_item = {
                    'id': f'AI-{action_item_id:03d}',
                    'title': self._create_title(description),
                    'description': description,
                    'owner': owner,
                    'due_date': due_date,
                    'priority': priority,
                    'ticket': ticket,
                    'team': None,  # Will be assigned later
                    'dependencies': [],
                    'status': 'not_started'
                }
                self.action_items.append(action_item)
                action_item_id += 1
    
    def assign_teams(self) -> None:
        """Assign action items to Technical or Operations team."""
        for item in self.action_items:
            if self._is_operations_task(item):
                item['team'] = 'Operations'
            elif self._is_technical_task(item):
                item['team'] = 'Technical'
            else:
                # Default to Technical if unclear
                item['team'] = 'Technical'
    
    def validate_action_items(self) -> None:
        """Validate action items have required fields."""
        for item in self.action_items:
            # Flag missing owners
            if not item.get('owner'):
                item['owner'] = 'Unassigned'
            
            # Flag missing due dates (but don't fail)
            if not item.get('due_date'):
                item['due_date'] = None
            
            # Validate team assignment
            if item['team'] not in ['Technical', 'Operations']:
                item['team'] = 'Technical'  # Default
    
    def extract_dependencies(self) -> None:
        """Extract dependencies between action items."""
        dependency_patterns = [
            r'(?:Depends on|depends on|requires|blocked by):\s*(.+?)(?:\n|$)',
            r'(?:Blocks|blocks|unblocks)\s*:\s*(.+?)(?:\n|$)',
        ]
        
        for pattern in dependency_patterns:
            matches = re.finditer(pattern, self.notes_text)
            for match in matches:
                dep_text = match.group(1).strip()
                # This would need to be matched against actual action items
                # For now, we'll keep it simple
    
    def _parse_date(self, date_str: str) -> str:
        """
        Parse date string to ISO format.
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            ISO 8601 formatted date string
        """
        try:
            # Try common date formats
            formats = [
                '%Y-%m-%d',
                '%B %d, %Y',
                '%b %d, %Y',
                '%m/%d/%Y',
            ]
            
            for fmt in formats:
                try:
                    parsed = datetime.strptime(date_str, fmt)
                    return parsed.isoformat()
                except ValueError:
                    continue
            
            # If no format matches, return as-is
            return date_str
        except Exception:
            return date_str
    
    def _parse_due_date(self, due_str: str) -> Optional[str]:
        """
        Parse due date from string.
        
        Args:
            due_str: Due date string (e.g., "TODAY", "TOMORROW", "Friday 5 PM")
            
        Returns:
            ISO 8601 formatted datetime or None
        """
        if not due_str:
            return None
        
        due_str = due_str.upper().strip()
        
        # Relative dates
        if due_str == 'TODAY':
            return datetime.now().replace(hour=17, minute=0).isoformat()
        elif due_str == 'TOMORROW':
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.replace(hour=17, minute=0).isoformat()
        elif due_str == 'ASAP':
            return datetime.now().replace(hour=12, minute=0).isoformat()
        
        # Day of week patterns
        day_pattern = r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)'
        time_pattern = r'(\d{1,2}):?(\d{0,2})\s*(AM|PM|A\.M\.|P\.M\.)?'
        
        day_match = re.search(day_pattern, due_str)
        time_match = re.search(time_pattern, due_str)
        
        if day_match or time_match:
            # Parse to best of ability
            try:
                # This is simplified - a real implementation would be more robust
                parsed = datetime.strptime(due_str.split()[0], '%Y-%m-%d')
                return parsed.isoformat()
            except ValueError:
                pass
        
        # Try to parse as datetime
        try:
            parsed = datetime.fromisoformat(due_str)
            return parsed.isoformat()
        except ValueError:
            pass
        
        return due_str if due_str else None
    
    def _extract_priority(self, text: str) -> str:
        """
        Extract priority from text.
        
        Args:
            text: Text to search for priority indicators
            
        Returns:
            Priority level (P1, P2, High, Normal, Low)
        """
        text_upper = text.upper()
        
        if 'P1' in text_upper or 'CRITICAL' in text_upper or 'URGENT' in text_upper:
            return 'P1'
        elif 'P2' in text_upper or 'ESCALATE' in text_upper:
            return 'P2'
        elif 'HIGH' in text_upper or 'IMPORTANT' in text_upper:
            return 'High'
        elif 'LOW' in text_upper:
            return 'Low'
        else:
            return 'Normal'
    
    def _create_title(self, description: str) -> str:
        """
        Create concise title from description.
        
        Args:
            description: Full description text
            
        Returns:
            Concise title (max 10 words)
        """
        # Take first sentence or first 10 words
        words = description.split()[:10]
        title = ' '.join(words)
        
        # Remove trailing punctuation if it's incomplete
        if title.endswith(','):
            title = title[:-1]
        
        return title
    
    def _is_operations_task(self, item: Dict[str, Any]) -> bool:
        """
        Determine if task belongs to Operations team.
        
        Args:
            item: Action item dictionary
            
        Returns:
            True if Operations task, False otherwise
        """
        keywords = [
            'report', 'create report', 'generate report', 'weekly report', 'daily report',
            'email', 'send email', 'notification', 'notify',
            'communication', 'inform', 'update', 'send',
            'escalation notification', 'escalate notification'
        ]
        
        text_lower = f"{item.get('title', '')} {item.get('description', '')}".lower()
        return any(kw in text_lower for kw in keywords)
    
    def _is_technical_task(self, item: Dict[str, Any]) -> bool:
        """
        Determine if task belongs to Technical team.
        
        Args:
            item: Action item dictionary
            
        Returns:
            True if Technical task, False otherwise
        """
        keywords = [
            'diagnose', 'investigate', 'troubleshoot', 'debug',
            'fix', 'repair', 'resolve', 'patch', 'deploy',
            'escalate', 'check', 'analyze', 'review',
            'test', 'build', 'develop', 'implement'
        ]
        
        text_lower = f"{item.get('title', '')} {item.get('description', '')}".lower()
        return any(kw in text_lower for kw in keywords)
    
    def get_structured_output(self) -> Dict[str, Any]:
        """
        Get structured output of parsed meeting.
        
        Returns:
            Dictionary with all meeting data
        """
        return {
            'meeting': self.meeting_metadata,
            'decisions': self.decisions,
            'action_items': self.action_items,
            'summary': {
                'total_items': len(self.action_items),
                'by_team': {
                    'Technical': len([i for i in self.action_items if i.get('team') == 'Technical']),
                    'Operations': len([i for i in self.action_items if i.get('team') == 'Operations'])
                },
                'by_priority': {
                    'P1': len([i for i in self.action_items if i.get('priority') == 'P1']),
                    'P2': len([i for i in self.action_items if i.get('priority') == 'P2']),
                    'High': len([i for i in self.action_items if i.get('priority') == 'High']),
                    'Normal': len([i for i in self.action_items if i.get('priority') == 'Normal']),
                    'Low': len([i for i in self.action_items if i.get('priority') == 'Low'])
                }
            }
        }
