"""
LangChain Bridge

Integration layer between LangChain StructuredTools and MCP client
"""
from typing import List, Dict, Any, Callable
import logging
import asyncio

from ..client import register_tool_handler, list_available_tools, is_tool_registered

logger = logging.getLogger(__name__)


def register_langchain_tools_sync(tools: List) -> None:
    """
    Register LangChain StructuredTools with our MCP client (synchronous version)

    Args:
        tools: List of LangChain StructuredTool objects
    """
    tool_mapping = {
        'get_weather': 'weather_service__get_weather',
        'perform_web_search': 'web_service__perform_web_search',
        'add_note_to_file': 'notes_service__add_note_to_file',
        'read_notes': 'notes_service__read_notes',
        'get_cryptocurrency_price': 'crypto_service__get_cryptocurrency_price'
    }

    for tool in tools:
        if tool.name in tool_mapping:
            mcp_tool_id = tool_mapping[tool.name]

            # Create wrapper function for the LangChain tool
            def create_tool_wrapper(langchain_tool) -> Callable:
                """Create a wrapper function for the LangChain tool"""

                async def async_wrapper(**kwargs) -> Any:
                    """Async wrapper for the tool"""
                    try:
                        logger.debug(f"Calling {langchain_tool.name} with args: {kwargs}")

                        # Call the LangChain tool - use ainvoke if available, otherwise invoke
                        if hasattr(langchain_tool, 'ainvoke'):
                            result = await langchain_tool.ainvoke(kwargs)
                        elif hasattr(langchain_tool, 'arun'):
                            result = await langchain_tool.arun(**kwargs)
                        else:
                            # Fallback to sync invoke
                            result = langchain_tool.invoke(kwargs)

                        logger.debug(f"Tool {langchain_tool.name} returned: {result}")

                        # Ensure we return a dict for consistency
                        if isinstance(result, dict):
                            return result
                        else:
                            return {"result": result, "raw_response": str(result)}

                    except Exception as e:
                        logger.error(f"Tool {langchain_tool.name} failed: {e}")
                        raise

                return async_wrapper

            # Create and register the wrapper
            wrapper = create_tool_wrapper(tool)
            register_tool_handler(mcp_tool_id, wrapper)
            logger.info(f"Registered tool: {tool.name} -> {mcp_tool_id}")

        else:
            logger.warning(f"Unknown tool: {tool.name} (not in mapping)")

    # Log summary
    registered_tools = list_available_tools()
    logger.info(f"Total registered tools: {len(registered_tools)}")
    for tool_id in registered_tools:
        logger.info(f"  ✓ {tool_id}")


async def register_langchain_tools_async(tools: List) -> None:
    """
    Async version of tool registration (if needed)

    Args:
        tools: List of LangChain StructuredTool objects
    """
    register_langchain_tools_sync(tools)  # The sync version works fine for registration


def quick_test_registration(tools: List) -> Dict[str, bool]:
    """
    Quick test to verify tool registration worked

    Args:
        tools: List of LangChain StructuredTool objects

    Returns:
        Dict mapping tool names to registration status
    """
    register_langchain_tools_sync(tools)

    tool_mapping = {
        'get_weather': 'weather_service__get_weather',
        'perform_web_search': 'web_service__perform_web_search',
        'add_note_to_file': 'notes_service__add_note_to_file',
        'read_notes': 'notes_service__read_notes',
        'get_cryptocurrency_price': 'crypto_service__get_cryptocurrency_price'
    }

    results = {}
    for tool in tools:
        if tool.name in tool_mapping:
            mcp_tool_id = tool_mapping[tool.name]
            results[tool.name] = is_tool_registered(mcp_tool_id)
        else:
            results[tool.name] = False

    return results
