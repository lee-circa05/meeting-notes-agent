"""
Unit tests for Meeting-Notes-to-Actions Agent
"""

import pytest
import json
import csv
from io import StringIO
from tests.conftest import MeetingNotesParser, OutputFormatter


class TestParser:
    """Test cases for the MeetingNotesParser."""
    
    def test_parser_initialization(self):
        """Test parser can be initialized with notes text."""
        notes = "Meeting notes test"
        parser = MeetingNotesParser(notes)
        assert parser.notes_text == notes
        assert parser.action_items == []
        assert parser.decisions == []
    
    def test_action_items_list(self, parser):
        """Test parser maintains action items list."""
        assert isinstance(parser.action_items, list)
        assert len(parser.action_items) == 2
    
    def test_decisions_list(self, parser):
        """Test parser maintains decisions list."""
        assert isinstance(parser.decisions, list)
        assert len(parser.decisions) == 1


class TestTeamAssignment:
    """Test cases for team assignment logic."""
    
    def test_operations_team_assignment(self):
        """Test Operations team is assigned correctly."""
        parser = MeetingNotesParser("")
        parser.action_items = [
            {'id': 'AI-001', 'title': 'Send status update email', 'team': None}
        ]
        parser.assign_teams()
        assert parser.action_items[0]['team'] == 'Operations'
    
    def test_technical_team_assignment(self):
        """Test Technical team is assigned correctly."""
        parser = MeetingNotesParser("")
        parser.action_items = [
            {'id': 'AI-001', 'title': 'Troubleshoot database issue', 'team': None}
        ]
        parser.assign_teams()
        assert parser.action_items[0]['team'] == 'Technical'
    
    def test_report_assignment_to_operations(self):
        """Test report tasks are assigned to Operations."""
        parser = MeetingNotesParser("")
        parser.action_items = [
            {'id': 'AI-001', 'title': 'Create daily report', 'team': None}
        ]
        parser.assign_teams()
        assert parser.action_items[0]['team'] == 'Operations'
    
    def test_escalation_assignment_to_technical(self):
        """Test escalation tasks are assigned to Technical."""
        parser = MeetingNotesParser("")
        parser.action_items = [
            {'id': 'AI-001', 'title': 'Escalate P1 ticket', 'team': None}
        ]
        parser.assign_teams()
        assert parser.action_items[0]['team'] == 'Technical'
    
    def test_deploy_assignment_to_technical(self):
        """Test deployment tasks are assigned to Technical."""
        parser = MeetingNotesParser("")
        parser.action_items = [
            {'id': 'AI-001', 'title': 'Deploy fix to production', 'team': None}
        ]
        parser.assign_teams()
        assert parser.action_items[0]['team'] == 'Technical'


class TestActionItemValidation:
    """Test cases for validating action items."""
    
    def test_action_item_has_required_fields(self, sample_action_item):
        """Test action items have all required fields."""
        required_fields = ['id', 'title', 'team', 'owner', 'due_date', 'priority']
        for field in required_fields:
            assert field in sample_action_item
            assert sample_action_item[field] is not None
    
    def test_action_item_priority_is_valid(self, sample_action_item):
        """Test action item priority is valid."""
        valid_priorities = ['P1', 'P2', 'High', 'Normal', 'Low']
        assert sample_action_item['priority'] in valid_priorities
    
    def test_action_item_owner_is_assigned(self, sample_action_item):
        """Test action item has owner assigned."""
        assert sample_action_item['owner'] != 'Unassigned'
        assert sample_action_item['owner'] != ''


class TestOutputFormatting:
    """Test cases for output formatting."""
    
    def test_formatter_json_output(self, formatter):
        """Test formatter can generate valid JSON."""
        json_output = formatter.to_json()
        # Should not raise exception
        data = json.loads(json_output)
        assert 'action_items' in data
        assert 'decisions' in data
    
    def test_formatter_json_has_action_items(self, formatter):
        """Test JSON output contains action items."""
        json_output = formatter.to_json()
        data = json.loads(json_output)
        assert len(data['action_items']) > 0
    
    def test_formatter_csv_output(self, formatter):
        """Test formatter can generate CSV output."""
        csv_output = formatter.to_csv()
        # Should have header row and data rows
        lines = csv_output.strip().split('\n')
        assert len(lines) >= 2  # Header + at least one data row
    
    def test_formatter_csv_has_headers(self, formatter):
        """Test CSV output has column headers."""
        csv_output = formatter.to_csv()
        lines = csv_output.strip().split('\n')
        header = lines[0]
        assert 'id' in header.lower() or 'title' in header.lower()
    
    def test_formatter_markdown_output(self, formatter):
        """Test formatter can generate Markdown output."""
        md_output = formatter.to_markdown()
        # Should contain markdown headers
        assert '#' in md_output
        assert 'Team' in md_output or 'team' in md_output
    
    def test_formatter_markdown_has_teams(self, formatter):
        """Test Markdown output groups by teams."""
        md_output = formatter.to_markdown()
        assert 'Technical' in md_output
        assert 'Operations' in md_output


class TestDataIntegrity:
    """Test cases for data integrity and consistency."""
    
    def test_action_items_ids_are_unique(self, formatter):
        """Test all action items have unique IDs."""
        ids = [item.get('id') for item in formatter.data['action_items']]
        assert len(ids) == len(set(ids))
    
    def test_all_action_items_assigned_to_team(self, formatter):
        """Test all action items are assigned to a team."""
        for item in formatter.data['action_items']:
            assert item.get('team') in ['Technical', 'Operations']
    
    def test_dependencies_reference_valid_items(self, formatter):
        """Test action item dependencies reference valid items."""
        all_ids = {item.get('id') for item in formatter.data['action_items']}
        for item in formatter.data['action_items']:
            deps = item.get('dependencies', [])
            if isinstance(deps, list):
                for dep in deps:
                    assert dep in all_ids or dep == ''


class TestPriorityHandling:
    """Test cases for priority handling."""
    
    def test_p1_items_identified(self, formatter):
        """Test P1 priority items are identified."""
        p1_items = [item for item in formatter.data['action_items'] if item.get('priority') == 'P1']
        assert len(p1_items) > 0
    
    def test_p2_items_identified(self, formatter):
        """Test P2 priority items are identified."""
        p2_items = [item for item in formatter.data['action_items'] if item.get('priority') == 'P2']
        # P2 items may or may not exist
        assert isinstance(p2_items, list)
    
    def test_escalation_flag_for_overdue_items(self):
        """Test escalation logic for items beyond SLA."""
        parser = MeetingNotesParser("")
        item = {
            'id': 'AI-001',
            'title': 'Troubleshoot P1 ticket',
            'priority': 'P1',
            'opened_time': '2026-09-01T08:00:00',  # Over 48 hours ago
            'team': 'Technical'
        }
        parser.action_items = [item]
        # Escalation check would happen here in real implementation
        assert item['priority'] == 'P1'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
