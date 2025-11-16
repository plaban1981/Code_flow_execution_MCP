"""
get_weather - Get current weather for a city

Server: weather-service
"""

from typing import Dict, Any, Optional, List
from ..mcp_client import call_mcp_tool


def get_weather(city: str, units: Optional[str] = None) -> Dict[str, Any]:
    """
    Get current weather for a city
    
    Args:
        city (string, required): City name (e.g., 'New York')
        units (string, optional): Temperature units: 'celsius' or 'fahrenheit'
    
    Returns:
        Dict containing the tool execution result
    """
    # Prepare parameters
    params = {
        "city": city,
        "units": units,
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Call MCP tool
    return call_mcp_tool("weather-service__get_weather", params)