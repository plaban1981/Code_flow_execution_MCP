"""
salesforce - MCP Server Tools

Available tools: 2
"""

from .update_record import update_record
from .create_lead import create_lead

__all__ = [
    "update_record",
    "create_lead",
]