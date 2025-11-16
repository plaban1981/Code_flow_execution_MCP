"""
MCP Client Core Functionality

Core functions for calling MCP tools and managing tool handlers
"""
from typing import Dict, Any, Callable
import asyncio
import logging

logger = logging.getLogger(__name__)

# Global tool registry
_tool_registry: Dict[str, Callable] = {}


def register_tool_handler(tool_id: str, handler: Callable):
    """
    Register a handler for a tool

    Args:
        tool_id: Unique identifier for the tool
        handler: Async or sync callable that implements the tool
    """
    _tool_registry[tool_id] = handler
    logger.debug(f"Registered tool handler: {tool_id}")


async def call_mcp_tool(tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call an MCP tool by its ID (async version)

    Args:
        tool_id: The tool identifier
        params: Parameters to pass to the tool

    Returns:
        Tool result as a dictionary

    Raises:
        ValueError: If tool not found in registry
    """
    if tool_id not in _tool_registry:
        available = list(_tool_registry.keys())
        error_msg = f"Tool not found: {tool_id}."

        if not available:
            error_msg += "\n❌ No tools registered! Use register_langchain_tools_sync() first."
        else:
            error_msg += f"\n📋 Available tools: {available}"

        logger.error(error_msg)
        raise ValueError(error_msg)

    handler = _tool_registry[tool_id]

    try:
        logger.debug(f"🔧 Calling tool {tool_id} with params: {params}")

        if asyncio.iscoroutinefunction(handler):
            result = await handler(**params)
        else:
            result = handler(**params)

        logger.debug(f"✅ Tool {tool_id} returned: {type(result)} - {result}")

        # Ensure consistent return format
        if not isinstance(result, dict):
            result = {"data": result, "raw": str(result)}

        return result

    except Exception as e:
        logger.error(f"❌ Tool execution failed for {tool_id}: {e}")
        raise


def call_mcp_tool_sync(tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call an MCP tool by its ID (synchronous version)

    Args:
        tool_id: The tool identifier
        params: Parameters to pass to the tool

    Returns:
        Tool result as a dictionary

    Raises:
        ValueError: If tool not found in registry
        RuntimeError: If event loop issues occur
    """
    try:
        # Try using existing event loop if available
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're in an environment with a running loop (like Jupyter)
                try:
                    import nest_asyncio
                    nest_asyncio.apply()
                except ImportError:
                    pass
        except:
            pass

        return asyncio.run(call_mcp_tool(tool_id, params))
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            logger.error("❌ Event loop issue - make sure nest_asyncio is installed and applied")
        raise
