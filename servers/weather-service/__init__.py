"""
weather-service - MCP Server Tools

Available tools: 2
"""

from .get_weather import get_weather
from .get_forecast import get_forecast

__all__ = [
    "get_weather",
    "get_forecast",
]