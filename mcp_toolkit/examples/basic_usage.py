#!/usr/bin/env python
"""
Basic Usage Example

Shows how to use the MCP toolkit with user queries
"""
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_toolkit.models import GetWeatherInput, GetCryptocurrencyPriceInput
from mcp_toolkit.tools import get_weather_sync, get_cryptocurrency_price_sync
from mcp_toolkit.client import get_registry_status


def example_without_mcp_server():
    """
    Example showing what happens without MCP server connected
    This will show error messages guiding you to register tools
    """
    print("="*70)
    print("EXAMPLE 1: Attempting to use tools without registration")
    print("="*70)

    # Check registry status
    status = get_registry_status()
    print(f"\nRegistry Status:")
    print(f"  Tools registered: {status['total_tools']}")
    print(f"  Available tools: {status['tools']}")

    if status['total_tools'] == 0:
        print("\n[!] No tools registered!")
        print("[i] You need to:")
        print("   1. Set up your MCP server")
        print("   2. Get tools from the server")
        print("   3. Register them using register_langchain_tools_sync()")
        print("\nSee example_with_mock_registration() for simulation")

    try:
        # This will fail with helpful error message
        weather = get_weather_sync({"location": "Tokyo"})
        print(f"\nWeather: {weather}")
    except ValueError as e:
        print(f"\n[!] Expected error: {e}")


def example_with_mock_registration():
    """
    Example showing how to register mock tools for testing
    """
    print("\n\n" + "="*70)
    print("EXAMPLE 2: Registering mock tools for testing")
    print("="*70)

    from mcp_toolkit.client import register_tool_handler

    # Register a mock weather tool
    async def mock_weather_tool(location: str):
        """Mock weather tool that returns fake data"""
        return {
            "location": location,
            "temperature": 22.5,
            "condition": "Sunny",
            "humidity": 65,
            "wind_speed": "10 km/h"
        }

    # Register the mock tool
    register_tool_handler('weather_service__get_weather', mock_weather_tool)
    print("[OK] Mock weather tool registered")

    # Now we can use it
    weather_input = GetWeatherInput(location="Tokyo")
    weather = get_weather_sync(weather_input)

    print(f"\n📊 Weather Results:")
    print(f"   Location: {weather.location}")
    print(f"   Temperature: {weather.temperature}°C")
    print(f"   Condition: {weather.condition}")
    print(f"   Raw data: {weather.raw_data}")


def example_user_query_processing():
    """
    Example showing how to process user queries
    """
    print("\n\n" + "="*70)
    print("EXAMPLE 3: Processing user queries")
    print("="*70)

    from mcp_toolkit.client import register_tool_handler, list_available_tools

    # Register mock tools
    async def mock_weather(location: str):
        return {"temperature": 25, "condition": "Cloudy", "location": location}

    async def mock_crypto(crypto: str):
        prices = {"bitcoin": 45000, "ethereum": 3000, "cardano": 0.5}
        return {"price": prices.get(crypto.lower(), 0), "currency": "USD"}

    register_tool_handler('weather_service__get_weather', mock_weather)
    register_tool_handler('crypto_service__get_cryptocurrency_price', mock_crypto)

    print(f"[OK] Registered tools: {list(list_available_tools().keys())}")

    # Process different user queries
    user_queries = [
        ("weather", "What's the weather in Paris?", "Paris"),
        ("crypto", "Get Bitcoin price", "bitcoin"),
        ("crypto", "How much is Ethereum?", "ethereum")
    ]

    print("\n📝 Processing user queries:")

    for query_type, user_input, param in user_queries:
        print(f"\n  User: '{user_input}'")

        if query_type == "weather":
            result = get_weather_sync({"location": param})
            print(f"  Bot: The weather in {result.location} is {result.raw_data.get('condition')} "
                  f"with a temperature of {result.raw_data.get('temperature')}°C")

        elif query_type == "crypto":
            result = get_cryptocurrency_price_sync({"crypto": param})
            print(f"  Bot: {param.capitalize()} is currently ${result.raw_data.get('price'):,.2f} USD")


def main():
    """Run all examples"""
    print("MCP TOOLKIT - BASIC USAGE EXAMPLES")
    print("="*70)

    # Example 1: Without registration
    example_without_mcp_server()

    # Example 2: With mock registration
    example_with_mock_registration()

    # Example 3: User query processing
    example_user_query_processing()

    print("\n\n" + "="*70)
    print("[OK] Examples completed!")
    print("="*70)
    print("\n💡 Next steps:")
    print("   1. Connect to your MCP server")
    print("   2. Register actual tools")
    print("   3. Process real user queries")
    print("\nSee examples/mcp_integration.py for MCP server integration")


if __name__ == '__main__':
    main()
