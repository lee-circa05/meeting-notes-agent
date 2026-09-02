"""
Meeting-Notes-to-Actions Agent

Main entry point for the agent.
"""

from .parser import MeetingNotesParser
from .formatters import OutputFormatter

__version__ = '1.0.0'
__author__ = 'Meeting Actions Team'

__all__ = ['MeetingNotesParser', 'OutputFormatter']
