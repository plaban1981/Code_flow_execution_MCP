"""
get_forecast - Get weather forecast for upcoming days

Server: weather-service
"""

from typing import Dict, Any, Optional, List
from ..mcp_client import call_mcp_tool


def get_forecast(city: str, days: int) -> Dict[str, Any]:
    """
    Get weather forecast for upcoming days
    
    Args:
        city (string, required): City name
        days (integer, required): Number of days (1-7)
    
    Returns:
        Dict containing the tool execution result
    """
    # Prepare parameters
    params = {
        "city": city,
        "days": days,
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Call MCP tool
    return call_mcp_tool("weather-service__get_forecast", params)