#!/usr/bin/env python
"""
Simple Demo Script - Works out of the box!

Run: python demo.py
"""
import sys
sys.path.insert(0, '.')

from mcp_toolkit.client import register_tool_handler, get_registry_status
from mcp_toolkit.tools import get_weather_sync, get_cryptocurrency_price_sync
from mcp_toolkit.models import GetWeatherInput, GetCryptocurrencyPriceInput

print("="*70)
print("MCP TOOLKIT - SIMPLE DEMO")
print("="*70)

# Step 1: Register mock tools
print("\n[Step 1] Registering mock tools...")

async def mock_weather(location: str):
    """Mock weather data"""
    weather_db = {
        "tokyo": {"temp": 18, "condition": "Rainy"},
        "paris": {"temp": 15, "condition": "Cloudy"},
        "london": {"temp": 12, "condition": "Foggy"},
        "new york": {"temp": 22, "condition": "Sunny"},
    }
    data = weather_db.get(location.lower(), {"temp": 20, "condition": "Clear"})
    return {"location": location, "temperature": data["temp"], "condition": data["condition"]}

async def mock_crypto(crypto: str):
    """Mock crypto prices"""
    prices = {"bitcoin": 45000, "ethereum": 3000, "cardano": 0.5}
    return {"crypto": crypto, "price": prices.get(crypto.lower(), 0), "currency": "USD"}

register_tool_handler('weather_service__get_weather', mock_weather)
register_tool_handler('crypto_service__get_cryptocurrency_price', mock_crypto)

print("[OK] Tools registered successfully")

# Step 2: Verify registration
print("\n[Step 2] Verifying registration...")
status = get_registry_status()
print(f"  Total tools: {status['total_tools']}")
print(f"  Registered: {', '.join(status['tools'])}")

# Step 3: Test weather queries
print("\n[Step 3] Testing weather queries...")
print("-"*70)

cities = ["Tokyo", "Paris", "London", "New York"]
for city in cities:
    weather = get_weather_sync(GetWeatherInput(location=city))
    print(f"  {city:12} {weather.raw_data['temperature']:>3}C  {weather.raw_data['condition']}")

# Step 4: Test crypto queries
print("\n[Step 4] Testing crypto queries...")
print("-"*70)

cryptos = ["bitcoin", "ethereum", "cardano"]
for crypto in cryptos:
    price = get_cryptocurrency_price_sync(GetCryptocurrencyPriceInput(crypto=crypto))
    print(f"  {crypto.capitalize():12} ${price.raw_data['price']:>10,.2f} USD")

# Step 5: Interactive example
print("\n[Step 5] Processing user queries...")
print("-"*70)

user_queries = [
    ("What's the weather in Tokyo?", "Tokyo"),
    ("Get Bitcoin price", "bitcoin"),
    ("Weather in Paris?", "Paris"),
]

for query, param in user_queries:
    print(f"\n  User Query: '{query}'")

    if 'weather' in query.lower():
        weather = get_weather_sync({"location": param})
        response = f"The weather in {weather.location} is {weather.raw_data['condition']} with {weather.raw_data['temperature']}C"
    elif 'bitcoin' in query.lower() or 'price' in query.lower():
        crypto = get_cryptocurrency_price_sync({"crypto": param})
        response = f"{crypto.crypto.capitalize()} is ${crypto.raw_data['price']:,.2f} USD"
    else:
        response = "Query processed"

    print(f"  Response: {response}")

# Summary
print("\n" + "="*70)
print("DEMO COMPLETE!")
print("="*70)
print("\nWhat you just saw:")
print("  1. Tool registration with mock data")
print("  2. Type-safe queries using Pydantic models")
print("  3. Multiple tool types (weather + crypto)")
print("  4. User query processing")
print("\nNext steps:")
print("  - See QUICKSTART.md for more examples")
print("  - See USAGE.md for complete documentation")
print("  - Edit examples/mcp_integration.py to connect real MCP server")
print("="*70)
