"""
MCP Tool Registry Management

Functions for managing and querying the tool registry
"""
from typing import Dict, Any
import logging
import sys

from .core import _tool_registry

logger = logging.getLogger(__name__)


def list_available_tools() -> Dict[str, str]:
    """
    List all registered tools with their IDs

    Returns:
        Dictionary mapping tool IDs to handler descriptions
    """
    return {
        tool_id: f"<function {handler.__name__}>"
        for tool_id, handler in _tool_registry.items()
    }


def is_tool_registered(tool_id: str) -> bool:
    """
    Check if a tool is registered

    Args:
        tool_id: The tool identifier to check

    Returns:
        True if tool is registered, False otherwise
    """
    return tool_id in _tool_registry


def clear_tool_registry():
    """
    Clear all registered tools (useful for testing)
    """
    _tool_registry.clear()
    logger.info("🧹 Cleared tool registry")


def get_registry_status() -> Dict[str, Any]:
    """
    Get detailed registry status

    Returns:
        Dictionary with registry statistics and environment info
    """
    return {
        "total_tools": len(_tool_registry),
        "tools": list(_tool_registry.keys()),
        "jupyter_mode": 'ipykernel' in sys.modules,
        "nest_asyncio_available": 'nest_asyncio' in sys.modules
    }
