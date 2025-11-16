"""
MCP Client - Handles actual tool execution

This module provides the call_mcp_tool function that all generated
tool files import and use to make actual MCP server calls.
"""

from typing import Dict, Any
import asyncio

# In-memory registry of MCP tool handlers
_tool_registry: Dict[str, Any] = {}


def register_tool_handler(tool_id: str, handler):
    """Register a handler for a tool."""
    _tool_registry[tool_id] = handler


def call_mcp_tool(tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call an MCP tool by its ID (sync wrapper for async handler).
    
    Args:
        tool_id: Tool identifier (e.g., "server__tool_name")
        params: Tool parameters
        
    Returns:
        Tool execution result
    """
    if tool_id not in _tool_registry:
        raise ValueError(f"Tool not found: {tool_id}. Available tools: {list(_tool_registry.keys())}")
    
    handler = _tool_registry[tool_id]
    
    # Handler might be sync or async
    if asyncio.iscoroutinefunction(handler):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                try:
                    import nest_asyncio
                    nest_asyncio.apply()
                    return loop.run_until_complete(handler(**params))
                except ImportError:
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, handler(**params))
                        return future.result()
            else:
                return loop.run_until_complete(handler(**params))
        except RuntimeError:
            return asyncio.run(handler(**params))
    else:
        return handler(**params)


def list_available_servers() -> list:
    """List all available MCP servers by exploring the filesystem."""
    import os
    servers_dir = os.path.join(os.path.dirname(__file__))
    
    if not os.path.exists(servers_dir):
        return []
    
    servers = []
    for item in os.listdir(servers_dir):
        item_path = os.path.join(servers_dir, item)
        if os.path.isdir(item_path) and not item.startswith('_') and item != '__pycache__':
            servers.append(item)
    
    return servers


def list_server_tools(server_name: str) -> list:
    """List all tools for a specific server."""
    import os
    server_dir = os.path.join(os.path.dirname(__file__), server_name)
    
    if not os.path.exists(server_dir):
        return []
    
    tools = []
    for item in os.listdir(server_dir):
        if item.endswith('.py') and not item.startswith('_'):
            tool_name = item[:-3]
            tools.append(tool_name)
    
    return tools
