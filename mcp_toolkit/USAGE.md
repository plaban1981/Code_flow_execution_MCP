# MCP Toolkit - Usage Guide

Complete guide for invoking and using the MCP Toolkit modular structure.

## Table of Contents

1. [Quick Start](#quick-start)
2. [CLI Commands](#cli-commands)
3. [Python Script Usage](#python-script-usage)
4. [Processing User Queries](#processing-user-queries)
5. [Interactive Mode](#interactive-mode)
6. [MCP Server Integration](#mcp-server-integration)
7. [Examples](#examples)

---

## Quick Start

### Installation

```bash
cd mcp_toolkit
pip install -r requirements.txt
```

### Verify Installation

```bash
python main.py verify
```

**Expected Output:**
```
Verification Status
============================================================
Tools registered: 0
Jupyter mode: False
nest_asyncio available: True

No tools registered yet.
Use register_langchain_tools_sync() to register tools.
```

---

## CLI Commands

### 1. Verify Installation

```bash
python main.py verify
```

Shows registry status and confirms the toolkit is working.

### 2. Debug Information

```bash
python main.py debug
```

Displays detailed debug information about registered tools and system state.

### 3. Run Demo

```bash
python main.py demo
```

Runs the token efficiency demonstration (requires tracking module).

---

## Python Script Usage

### Basic Import and Usage

```python
# Navigate to the toolkit directory
cd mcp_toolkit

# Run Python
python
```

```python
# Import components
from mcp_toolkit.models import GetWeatherInput
from mcp_toolkit.tools import get_weather_sync
from mcp_toolkit.client import register_tool_handler

# Register a mock tool for testing
async def mock_weather(location: str):
    return {
        "location": location,
        "temperature": 22.5,
        "condition": "Sunny"
    }

register_tool_handler('weather_service__get_weather', mock_weather)

# Use the tool
weather = get_weather_sync({"location": "Tokyo"})
print(weather.raw_data)
```

---

## Processing User Queries

### Method 1: Direct Script Execution

Create a file `my_queries.py`:

```python
from mcp_toolkit.client import register_tool_handler
from mcp_toolkit.tools import get_weather_sync

# Setup mock tool
async def mock_weather(location: str):
    return {"temperature": 22, "condition": "Sunny", "location": location}

register_tool_handler('weather_service__get_weather', mock_weather)

# Process user query
user_query = "What's the weather in Paris?"
# Extract location (simplified)
location = "Paris"

weather = get_weather_sync({"location": location})
print(f"Weather in {weather.location}: {weather.raw_data}")
```

**Run it:**
```bash
python my_queries.py
```

### Method 2: Using the Examples

```bash
# Run basic usage examples
python examples/basic_usage.py
```

**Output:**
```
EXAMPLE 1: Attempting to use tools without registration
...
EXAMPLE 2: Registering mock tools for testing
...
EXAMPLE 3: Processing user queries
  User: 'What's the weather in Paris?'
  Bot: The weather in Paris is Cloudy with a temperature of 25°C
```

---

## Interactive Mode

### Run Interactive Demo

```bash
python examples/interactive_demo.py
```

**Interactive Session:**
```
INTERACTIVE MCP TOOLKIT DEMO
======================================================================

Commands:
  - Ask about weather: 'What's the weather in Tokyo?'
  - Ask about crypto: 'What's the Bitcoin price?'
  - Type 'help' for examples
  - Type 'quit' or 'exit' to quit
======================================================================

👤 You: What's the weather in Tokyo?
🤖 Bot: The weather in Tokyo is Rainy with a temperature of 18°C and 80% humidity.

👤 You: What's the Bitcoin price?
🤖 Bot: Bitcoin is currently priced at $45,000.00 USD

👤 You: quit
👋 Goodbye!
```

### Batch Mode

Process multiple queries at once:

```bash
python examples/interactive_demo.py --mode batch --queries \
  "What's the weather in Paris?" \
  "Get Bitcoin price" \
  "How much is Ethereum?"
```

**Output:**
```
[Query 1] What's the weather in Paris?
[Response] The weather in Paris is Cloudy with a temperature of 15°C...

[Query 2] Get Bitcoin price
[Response] Bitcoin is currently priced at $45,000.00 USD

[Query 3] How much is Ethereum?
[Response] Ethereum is currently priced at $3,000.00 USD
```

---

## MCP Server Integration

### Step 1: Configure Your MCP Server

Edit `examples/mcp_integration.py` and uncomment your server configuration:

```python
# For LangChain MCP Adapter
from langchain_mcp_adapters.client import MultiServerMCPClient

server_params = {
    "weather": {
        "command": "uv",
        "args": ["--directory", "/path/to/server", "run", "server.py"],
        "transport": "stdio"
    }
}

client = MultiServerMCPClient(server_params)
tools = await client.get_tools()
```

### Step 2: Run Integration

```bash
python examples/mcp_integration.py
```

### Step 3: Use in Your Code

```python
from mcp_toolkit.bridge import register_langchain_tools_sync
from mcp_toolkit.tools import get_weather_sync

# After getting tools from MCP server
register_langchain_tools_sync(tools)

# Now use the tools
weather = get_weather_sync({"location": "New York"})
print(weather.raw_data)
```

---

## Examples

### Example 1: Simple Query Script

**File: `simple_query.py`**
```python
import sys
sys.path.insert(0, '.')

from mcp_toolkit.client import register_tool_handler
from mcp_toolkit.tools import get_weather_sync

# Mock tool
async def weather(location: str):
    return {"temp": 25, "condition": "Clear"}

register_tool_handler('weather_service__get_weather', weather)

# Query
result = get_weather_sync({"location": "London"})
print(f"Temperature: {result.raw_data['temp']}°C")
```

**Run:**
```bash
python simple_query.py
```

### Example 2: Multiple Tool Types

**File: `multi_tool.py`**
```python
from mcp_toolkit.client import register_tool_handler
from mcp_toolkit.tools import (
    get_weather_sync,
    get_cryptocurrency_price_sync
)

# Register mocks
async def weather(location: str):
    return {"temp": 22, "condition": "Sunny"}

async def crypto(crypto: str):
    return {"price": 45000, "currency": "USD"}

register_tool_handler('weather_service__get_weather', weather)
register_tool_handler('crypto_service__get_cryptocurrency_price', crypto)

# Use both
weather = get_weather_sync({"location": "Tokyo"})
bitcoin = get_cryptocurrency_price_sync({"crypto": "bitcoin"})

print(f"Weather: {weather.raw_data}")
print(f"Bitcoin: ${bitcoin.raw_data['price']:,.2f}")
```

**Run:**
```bash
python multi_tool.py
```

### Example 3: Command-Line Arguments

**File: `cli_query.py`**
```python
import sys
import argparse
sys.path.insert(0, '.')

from mcp_toolkit.client import register_tool_handler
from mcp_toolkit.tools import get_weather_sync

# Setup
async def weather(location: str):
    return {"temp": 20, "condition": "Cloudy"}

register_tool_handler('weather_service__get_weather', weather)

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('location', help='Location for weather')
args = parser.parse_args()

# Query
weather = get_weather_sync({"location": args.location})
print(f"Weather in {args.location}: {weather.raw_data}")
```

**Run:**
```bash
python cli_query.py Tokyo
python cli_query.py "New York"
python cli_query.py Paris
```

---

## Common Patterns

### Pattern 1: Query Router

```python
def route_query(user_input: str):
    """Route user query to appropriate tool"""
    if 'weather' in user_input.lower():
        # Extract location and call weather tool
        return get_weather_sync(...)
    elif 'price' in user_input.lower():
        # Extract crypto and call price tool
        return get_cryptocurrency_price_sync(...)
    else:
        return "Unknown query type"
```

### Pattern 2: Async Batch Processing

```python
import asyncio
from mcp_toolkit.tools import get_weather

async def process_batch(locations):
    """Process multiple queries concurrently"""
    tasks = [get_weather({"location": loc}) for loc in locations]
    results = await asyncio.gather(*tasks)
    return results

# Use it
locations = ["Tokyo", "Paris", "London"]
results = asyncio.run(process_batch(locations))
```

### Pattern 3: Error Handling

```python
from mcp_toolkit.tools import get_weather_sync

try:
    weather = get_weather_sync({"location": "Tokyo"})
    print(weather.raw_data)
except ValueError as e:
    if "Tool not found" in str(e):
        print("Tools not registered. Run setup first.")
    else:
        raise
```

---

## Troubleshooting

### Issue: "Tool not found" Error

**Solution:**
```python
# Check registry status
from mcp_toolkit.client import get_registry_status
status = get_registry_status()
print(status)  # Check if tools are registered

# If no tools, register them
from mcp_toolkit.client import register_tool_handler
# ... register your tools
```

### Issue: Import Errors

**Solution:**
```bash
# Make sure you're in the right directory
cd mcp_toolkit

# Or add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/mcp_toolkit"
```

### Issue: Async Errors in Jupyter

**Solution:**
```python
import nest_asyncio
nest_asyncio.apply()
```

---

## Next Steps

1. **Test with mock tools:** Run `python examples/basic_usage.py`
2. **Try interactive mode:** Run `python examples/interactive_demo.py`
3. **Connect MCP server:** Edit and run `examples/mcp_integration.py`
4. **Build your app:** Use the patterns above to create your application

---

## Reference

- **Main CLI:** `python main.py [command]`
- **Examples:** `python examples/[script].py`
- **Import:** `from mcp_toolkit.[module] import ...`
- **Registry:** `get_registry_status()`, `list_available_tools()`

**Happy coding!** 🚀
