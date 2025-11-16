"""
Web Search Tool Wrapper

Type-safe wrapper for web search MCP tool
"""
from typing import Union
import asyncio

from ..models.web import PerformWebSearchInput, PerformWebSearchResponse
from ..client import call_mcp_tool


async def perform_web_search(input_data: Union[PerformWebSearchInput, dict]) -> PerformWebSearchResponse:
    """
    Performs a web search

    Args:
        input_data: Input parameters containing search query

    Returns:
        Search results
    """
    if isinstance(input_data, dict):
        input_data = PerformWebSearchInput(**input_data)

    result = await call_mcp_tool(
        'web_service__perform_web_search',
        input_data.model_dump(exclude_none=True)
    )

    return PerformWebSearchResponse(
        query=input_data.query,
        results=str(result) if not isinstance(result, dict) else result.get('results', str(result)),
        raw_data=result if isinstance(result, dict) else {"response": result}
    )


def perform_web_search_sync(input_data: Union[PerformWebSearchInput, dict]) -> PerformWebSearchResponse:
    """Synchronous version of perform_web_search"""
    return asyncio.run(perform_web_search(input_data))
