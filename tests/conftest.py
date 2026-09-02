"""
Test framework for Meeting-Notes-to-Actions Agent
"""

import pytest
import json
import csv
from pathlib import Path
from datetime import datetime, timedelta

# Import actual implementations
from src.parser import MeetingNotesParser
from src.formatters import OutputFormatter


# Test Fixtures

@pytest.fixture
def sample_action_item():
    """Sample action item for testing."""
    return {
        'id': 'AI-001',
        'title': 'Diagnose database issue #DB-12345',
        'team': 'Technical',
        'owner': 'John',
        'due_date': '2026-09-02T13:00:00',
        'priority': 'P1',
        'ticket': 'DB-12345',
        'description': 'Investigate database connection pool exhaustion',
        'dependencies': [],
        'status': 'not_started'
    }


@pytest.fixture
def sample_structured_data():
    """Sample structured data from parser."""
    return {
        'action_items': [
            {
                'id': 'AI-001',
                'title': 'Diagnose database issue',
                'team': 'Technical',
                'owner': 'John',
                'due_date': '2026-09-02T13:00:00',
                'priority': 'P1'
            },
            {
                'id': 'AI-002',
                'title': 'Send status update email',
                'team': 'Operations',
                'owner': 'Lisa',
                'due_date': '2026-09-02T16:00:00',
                'priority': 'P1'
            }
        ],
        'decisions': [
            {
                'id': 'DEC-001',
                'description': 'Prioritize database issue',
                'priority': 'P1'
            }
        ]
    }


@pytest.fixture
def parser():
    """Initialize parser with sample data."""
    sample_notes = """
    Meeting: Daily Standup - September 2, 2026
    Date: 2026-09-02
    Attendees: John Smith, Sarah Chen, Lisa Wang
    
    John - Diagnose database issue #DB-12345 - TODAY 1 PM - P1
    Sarah - Check connection pool logs - TODAY 12 PM - P1
    Lisa - Send status update email - TODAY 4 PM - P2
    Mike - Create weekly P1/P2 report - Friday 5 PM - High
    """
    return MeetingNotesParser(sample_notes)


@pytest.fixture
def formatter(sample_structured_data):
    """Initialize formatter with sample data."""
    return OutputFormatter(sample_structured_data)


if __name__ == '__main__':
    print("Test framework loaded. Run with: pytest tests/test_agent.py -v")
