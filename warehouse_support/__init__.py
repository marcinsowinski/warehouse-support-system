"""
Warehouse Management System Support package.
"""

# This makes the directory a Python package
from .settings import settings
from .jira_client import JiraClient
from .ai_assistant import AIAssistant

__version__ = '1.0.0'
__all__ = ['settings', 'JiraClient', 'AIAssistant'] 