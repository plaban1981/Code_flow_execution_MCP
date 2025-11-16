"""
Weather Tool Wrapper

Type-safe wrapper for weather MCP tool
"""
from typing import Union
import asyncio

from ..models.weather import GetWeatherInput, GetWeatherResponse
from ..client import call_mcp_tool, call_mcp_tool_sync as client_sync_call


async def get_weather(input_data: Union[GetWeatherInput, dict]) -> GetWeatherResponse:
    """
    Gets the weather given a location

    Args:
        input_data: Input parameters containing location

    Returns:
        Weather information for the specified location
    """
    if isinstance(input_data, dict):
        input_data = GetWeatherInput(**input_data)

    result = await call_mcp_tool(
        'weather_service__get_weather',
        input_data.model_dump(exclude_none=True)
    )

    # Parse the response intelligently
    if isinstance(result, dict):
        # Extract fields that match the response model (excluding location which we set explicitly)
        response_fields = {k: v for k, v in result.items() if k in GetWeatherResponse.model_fields and k != 'location' and k != 'raw_data'}
        return GetWeatherResponse(
            location=input_data.location,
            raw_data=result,
            **response_fields
        )
    else:
        return GetWeatherResponse(
            location=input_data.location,
            raw_data={"response": result}
        )


def get_weather_sync(input_data: Union[GetWeatherInput, dict]) -> GetWeatherResponse:
    """Synchronous version of get_weather"""
    return asyncio.run(get_weather(input_data))
