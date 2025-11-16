#!/usr/bin/env python
"""
Interactive Demo

Shows how to create an interactive CLI that processes user queries
"""
import sys
from pathlib import Path
import os

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_toolkit.client import register_tool_handler, list_available_tools
from mcp_toolkit.tools import get_weather_sync, get_cryptocurrency_price_sync, perform_web_search_sync
from mcp_toolkit.models import GetWeatherInput, GetCryptocurrencyPriceInput


def setup_mock_tools():
    """Register mock tools for demonstration"""

    async def mock_weather(location: str):
        """Real weather tool using wttr.in API"""
        try:
            import requests
            import json

            # Use wttr.in API for real weather data (free, no API key needed)
            url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract weather information
            current = data.get('current_condition', [{}])[0]
            temp_c = current.get('temp_C', 'N/A')
            condition = current.get('weatherDesc', [{}])[0].get('value', 'Unknown')
            humidity = current.get('humidity', 'N/A')

            return {
                "location": location,
                "temperature": int(temp_c) if temp_c != 'N/A' else 0,
                "condition": condition,
                "humidity": int(humidity) if humidity != 'N/A' else 0
            }
        except Exception as e:
            # Fallback to mock data if API fails
            print(f"Warning: Could not fetch real weather for {location}, using mock data. Error: {e}")
            weather_data = {
                "tokyo": {"temp": 18, "condition": "Rainy", "humidity": 80},
                "paris": {"temp": 15, "condition": "Cloudy", "humidity": 70},
                "new york": {"temp": 22, "condition": "Sunny", "humidity": 60},
                "london": {"temp": 12, "condition": "Foggy", "humidity": 85},
            }
            data = weather_data.get(location.lower(), {"temp": 20, "condition": "Clear", "humidity": 65})
            return {
                "location": location,
                "temperature": data["temp"],
                "condition": data["condition"],
                "humidity": data["humidity"]
            }

    async def mock_crypto(crypto: str):
        """Real crypto price tool using CoinGecko API"""
        try:
            import requests

            # Use CoinGecko API to fetch current price in USD
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {"ids": crypto.lower(), "vs_currencies": "usd"}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            price = data.get(crypto.lower(), {}).get("usd")

            if price is not None:
                return {"crypto": crypto, "price": float(price), "currency": "USD"}
            else:
                # Fallback to mock data if crypto not found
                prices = {
                    "bitcoin": 45000.00,
                    "ethereum": 3000.00,
                    "cardano": 0.50,
                    "solana": 100.00,
                    "dogecoin": 0.08,
                    "litecoin": 85.50
                }
                price = prices.get(crypto.lower(), 0)
                return {"crypto": crypto, "price": price, "currency": "USD"}

        except Exception as e:
            # Fallback to mock data if API fails
            print(f"Warning: Could not fetch real price for {crypto}, using mock data. Error: {e}")
            prices = {
                "bitcoin": 45000.00,
                "ethereum": 3000.00,
                "cardano": 0.50,
                "solana": 100.00,
                "dogecoin": 0.08,
                "litecoin": 85.50
            }
            price = prices.get(crypto.lower(), 0)
            return {"crypto": crypto, "price": price, "currency": "USD"}

    async def mock_web_search(query: str):
        """Real web search using Groq API"""
        try:
            from groq import Groq

            # Use Groq API key from environment or hardcoded
            GROQ_API_KEY = "Your API Key"

            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant that searches the web and responds to questions"
                },
                {
                    "role": "user",
                    "content": query
                },
            ]

            client = Groq(api_key=GROQ_API_KEY)

            # Chat completion without streaming
            response = client.chat.completions.create(
                model="groq/compound-mini",
                messages=messages
            )

            return {
                "query": query,
                "results": response.choices[0].message.content
            }
        except Exception as e:
            # Fallback to mock data if API fails
            print(f"Warning: Could not perform real web search, using mock data. Error: {e}")
            return {
                "query": query,
                "results": f"Mock search results for: {query}\n1. Result one\n2. Result two"
            }

    # Register tools
    register_tool_handler('weather_service__get_weather', mock_weather)
    register_tool_handler('crypto_service__get_cryptocurrency_price', mock_crypto)
    register_tool_handler('web_service__perform_web_search', mock_web_search)

    print("[OK] Mock tools registered")
    print(f"📋 Available tools: {list(list_available_tools().keys())}")


def extract_cryptocurrency(query: str) -> str:
    """
    Extract cryptocurrency name from query

    Args:
        query: User query string

    Returns:
        Extracted cryptocurrency name or None
    """
    import re

    # Common patterns for crypto queries
    patterns = [
        r'(?:price|cost|value) (?:of|for) ([a-zA-Z]+)',
        r'([a-zA-Z]+) (?:price|cost|value)',
        r'how much is ([a-zA-Z]+)',
        r'what(?:\'s| is) (?:the )?([a-zA-Z]+) (?:price|worth)',
    ]

    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            crypto_name = match.group(1).lower()
            # Filter out common words that aren't cryptocurrencies
            if crypto_name not in ['the', 'a', 'an', 'is', 'price', 'crypto', 'cryptocurrency']:
                return crypto_name

    # Fallback: look for known crypto keywords
    known_cryptos = ['bitcoin', 'ethereum', 'cardano', 'solana', 'dogecoin', 'litecoin',
                     'ripple', 'xrp', 'polkadot', 'chainlink', 'stellar', 'monero',
                     'tether', 'usdc', 'bnb', 'binance']
    query_lower = query.lower()
    for crypto in known_cryptos:
        if crypto in query_lower:
            return crypto

    return None


def extract_location(query: str) -> str:
    """
    Extract location from query using simple pattern matching

    Args:
        query: User query string

    Returns:
        Extracted location or None
    """
    import re

    # Common patterns for location queries
    patterns = [
        r'weather (?:in|at|for) ([A-Z][a-zA-Z\s]+?)(?:\?|$|,)',
        r'climate (?:in|at|of) ([A-Z][a-zA-Z\s]+?)(?:\?|$|,)',
        r'temperature (?:in|at|of) ([A-Z][a-zA-Z\s]+?)(?:\?|$|,)',
        r'forecast (?:for|in|at) ([A-Z][a-zA-Z\s]+?)(?:\?|$|,)',
    ]

    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # Fallback: look for capitalized words after weather-related keywords
    words = query.split()
    for i, word in enumerate(words):
        if word.lower() in ['weather', 'climate', 'temperature', 'forecast']:
            # Get next few capitalized words
            location_parts = []
            for j in range(i+1, min(i+4, len(words))):
                if words[j][0].isupper() or words[j].lower() in ['in', 'at', 'of', 'for']:
                    if words[j].lower() not in ['in', 'at', 'of', 'for']:
                        location_parts.append(words[j])
                else:
                    break
            if location_parts:
                return ' '.join(location_parts).rstrip('?,!')

    return None


def process_query(query: str, verbose: bool = False):
    """
    Process a user query and return response

    Args:
        query: User input query
        verbose: If True, return detailed metadata

    Returns:
        Response string or dict with metadata
    """
    import time
    start_time = time.time()

    query_lower = query.lower()
    metadata = {
        "query": query,
        "steps": [],
        "api_calls": [],
        "llm_calls": 0,
        "token_usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        },
        "cost": 0.0,
        "latency_ms": 0
    }

    try:
        # Weather queries
        if any(word in query_lower for word in ['weather', 'temperature', 'forecast', 'climate']):
            # Extract location from query
            location = extract_location(query)

            if not location:
                return "Please specify a location. For example: 'What's the weather in Tokyo?'"

            # Check if location is in mock data
            known_cities = ['tokyo', 'paris', 'new york', 'london']
            location_lower = location.lower()

            # If not in known cities, use web search
            if location_lower not in known_cities:
                search_query = f"current weather in {location}"
                search_result = perform_web_search_sync({"query": search_query})
                return (f"🔍 Searched for weather in {location}:\n"
                       f"{search_result.raw_data.get('results', 'No results found')}")

            # Use weather tool for known cities
            weather = get_weather_sync({"location": location})
            return (f"The weather in {weather.location} is {weather.raw_data.get('condition', 'Unknown')} "
                   f"with a temperature of {weather.raw_data.get('temperature', 'N/A')}°C "
                   f"and {weather.raw_data.get('humidity', 'N/A')}% humidity.")

        # Crypto queries
        elif any(word in query_lower for word in ['bitcoin', 'ethereum', 'crypto', 'price', 'litecoin', 'cryptocurrency']):
            metadata["steps"].append("Detected cryptocurrency query")

            # Extract cryptocurrency name from query
            crypto = extract_cryptocurrency(query)
            metadata["steps"].append(f"Extracted cryptocurrency: {crypto}")

            if not crypto:
                response = "Please specify a cryptocurrency. For example: 'What's the Bitcoin price?'"
                metadata["latency_ms"] = (time.time() - start_time) * 1000
                return {"response": response, "metadata": metadata} if verbose else response

            # All cryptocurrencies now use CoinGecko API
            metadata["steps"].append(f"Calling CoinGecko API for {crypto}")
            api_start = time.time()

            price_data = get_cryptocurrency_price_sync({"crypto": crypto})
            price = price_data.raw_data.get('price', 0)

            api_latency = (time.time() - api_start) * 1000
            metadata["api_calls"].append({
                "service": "CoinGecko",
                "endpoint": f"GET /api/v3/simple/price?ids={crypto}&vs_currencies=usd",
                "latency_ms": api_latency,
                "response": {"price": price, "currency": "USD"}
            })
            metadata["steps"].append(f"Received price: ${price}")

            if price > 0:
                response = f"{crypto.capitalize()} is currently priced at ${price:,.2f} USD"
            else:
                response = f"Could not find price information for {crypto}. Please check the cryptocurrency name."

            metadata["latency_ms"] = (time.time() - start_time) * 1000
            metadata["steps"].append("Formatted response")

            return {"response": response, "metadata": metadata} if verbose else response

        # Default response
        else:
            response = f"I understand you asked: '{query}'\nI can help with weather and cryptocurrency queries!"
            metadata["latency_ms"] = (time.time() - start_time) * 1000
            return {"response": response, "metadata": metadata} if verbose else response

    except Exception as e:
        response = f"Error processing query: {e}"
        metadata["latency_ms"] = (time.time() - start_time) * 1000
        metadata["error"] = str(e)
        return {"response": response, "metadata": metadata} if verbose else response


def interactive_mode():
    """Run interactive CLI"""
    print("\n" + "="*70)
    print("INTERACTIVE MCP TOOLKIT DEMO")
    print("="*70)
    print("\nCommands:")
    print("  - Ask about weather: 'What's the weather in Tokyo?'")
    print("  - Ask about crypto: 'What's the Bitcoin price?'")
    print("  - Type 'help' for examples")
    print("  - Type 'quit' or 'exit' to quit")
    print("="*70)

    setup_mock_tools()

    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            # Check for exit
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break

            # Check for help
            if user_input.lower() == 'help':
                print("\n📚 Example queries:")
                print("  • What's the weather in Paris?")
                print("  • Get weather for London")
                print("  • What's the Bitcoin price?")
                print("  • How much is Ethereum?")
                print("  • Get Cardano price")
                continue

            # Process query
            response = process_query(user_input)
            print(f"🤖 Bot: {response}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"[X] Error: {e}")


def batch_mode(queries: list, verbose: bool = False):
    """
    Process multiple queries in batch

    Args:
        queries: List of query strings
        verbose: If True, show detailed metadata
    """
    print("\n" + "="*70)
    print("BATCH QUERY PROCESSING" + (" (VERBOSE MODE)" if verbose else ""))
    print("="*70)

    setup_mock_tools()

    for i, query in enumerate(queries, 1):
        print(f"\n[Query {i}] {query}")
        result = process_query(query, verbose=verbose)

        if verbose and isinstance(result, dict):
            import json
            print(f"[Response] {result['response']}")
            print(f"\n[Detailed Metadata]")
            print(json.dumps(result['metadata'], indent=2))
        else:
            print(f"[Response] {result}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Interactive MCP Toolkit Demo")
    parser.add_argument(
        '--mode',
        choices=['interactive', 'batch'],
        default='interactive',
        help='Run mode (default: interactive)'
    )
    parser.add_argument(
        '--queries',
        nargs='+',
        help='Queries for batch mode'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed metadata (batch mode only)'
    )

    args = parser.parse_args()

    if args.mode == 'interactive':
        interactive_mode()
    elif args.mode == 'batch':
        if args.queries:
            batch_mode(args.queries, verbose=args.verbose)
        else:
            # Default batch queries
            default_queries = [
                "What's the weather in Tokyo?",
                "Get Bitcoin price",
                "What's the weather in Paris?",
                "How much is Ethereum?"
            ]
            batch_mode(default_queries, verbose=args.verbose)


if __name__ == '__main__':
    main()
