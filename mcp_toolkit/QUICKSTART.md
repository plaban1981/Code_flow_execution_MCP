# Quick Start Guide

## Running the MCP Toolkit - 5 Minute Guide

### 1. Verify Installation (10 seconds)

```bash
cd mcp_toolkit
python main.py verify
```

**Expected Output:**
```
Verification Status
============================================================
Tools registered: 0
Jupyter mode: False
nest_asyncio available: True
```

---

### 2. Run Interactive Demo (2 minutes)

```bash
python examples/interactive_demo.py
```

**Try these queries:**
```
What's the weather in Tokyo?
Get Bitcoin price
What's the weather in Paris?
quit
```

---

### 3. Run Basic Examples (1 minute)

```bash
python examples/basic_usage.py
```

This shows:
- How to register mock tools
- How to process user queries
- How the system works

---

### 4. Create Your First Script (2 minutes)

Create `my_first_query.py`:

```python
import sys
sys.path.insert(0, '.')

from mcp_toolkit.client import register_tool_handler
from mcp_toolkit.tools import get_weather_sync

# Register a mock weather tool
async def mock_weather(location: str):
    return {
        "location": location,
        "temperature": 22,
        "condition": "Sunny"
    }

register_tool_handler('weather_service__get_weather', mock_weather)

# Use it!
weather = get_weather_sync({"location": "London"})
print(f"Weather in {weather.location}:")
print(f"  Temperature: {weather.raw_data['temperature']}C")
print(f"  Condition: {weather.raw_data['condition']}")
```

**Run it:**
```bash
python my_first_query.py
```

---

## Command Reference

| Command | Description |
|---------|-------------|
| `python main.py verify` | Check installation |
| `python main.py debug` | Show debug info |
| `python examples/interactive_demo.py` | Interactive mode |
| `python examples/basic_usage.py` | See examples |
| `python examples/interactive_demo.py --mode batch --queries "query1" "query2"` | Batch mode |

---

## Processing User Queries

### Method 1: Command-Line Arguments

```python
# File: query_cli.py
import sys
sys.path.insert(0, '.')

from mcp_toolkit.client import register_tool_handler
from mcp_toolkit.tools import get_weather_sync

async def mock_weather(location: str):
    return {"temperature": 20, "condition": "Clear"}

register_tool_handler('weather_service__get_weather', mock_weather)

# Get location from command line
location = sys.argv[1] if len(sys.argv) > 1 else "Tokyo"

weather = get_weather_sync({"location": location})
print(f"{location}: {weather.raw_data['temperature']}C, {weather.raw_data['condition']}")
```

**Run:**
```bash
python query_cli.py Paris
python query_cli.py "New York"
```

### Method 2: Interactive Input

```python
# File: query_interactive.py
import sys
sys.path.insert(0, '.')

from mcp_toolkit.client import register_tool_handler
from mcp_toolkit.tools import get_weather_sync

async def mock_weather(location: str):
    return {"temperature": 25, "condition": "Cloudy"}

register_tool_handler('weather_service__get_weather', mock_weather)

while True:
    location = input("Enter location (or 'quit'): ")
    if location.lower() == 'quit':
        break

    weather = get_weather_sync({"location": location})
    print(f"Result: {weather.raw_data}\n")
```

**Run:**
```bash
python query_interactive.py
```

### Method 3: Process Multiple Queries

```python
# File: batch_queries.py
import sys
sys.path.insert(0, '.')

from mcp_toolkit.client import register_tool_handler
from mcp_toolkit.tools import get_weather_sync

async def mock_weather(location: str):
    temps = {"Tokyo": 18, "Paris": 15, "London": 12}
    return {"temperature": temps.get(location, 20), "condition": "Variable"}

register_tool_handler('weather_service__get_weather', mock_weather)

# Process multiple queries
queries = ["Tokyo", "Paris", "London", "Sydney"]

for location in queries:
    weather = get_weather_sync({"location": location})
    print(f"{location:10} {weather.raw_data['temperature']}C")
```

**Run:**
```bash
python batch_queries.py
```

---

## Common Use Cases

### Use Case 1: Chatbot Backend

```python
def handle_user_message(user_input: str) -> str:
    """Process user message and return response"""

    # Simple keyword matching (use NLP in production)
    if 'weather' in user_input.lower():
        # Extract location and call weather tool
        result = get_weather_sync({"location": "extracted_location"})
        return f"The weather is {result.raw_data['condition']}"

    return "I can help with weather queries!"
```

### Use Case 2: API Endpoint

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/weather', methods=['POST'])
def weather_api():
    data = request.json
    location = data.get('location', 'Tokyo')

    weather = get_weather_sync({"location": location})
    return jsonify(weather.raw_data)

if __name__ == '__main__':
    app.run()
```

### Use Case 3: Scheduled Tasks

```python
import schedule
import time

def fetch_daily_weather():
    """Fetch weather for multiple cities"""
    cities = ["Tokyo", "London", "New York"]

    for city in cities:
        weather = get_weather_sync({"location": city})
        print(f"{city}: {weather.raw_data}")

# Run every day at 8am
schedule.every().day.at("08:00").do(fetch_daily_weather)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Next Steps

1. **For mock testing:** Use the examples above
2. **For production:** Set up your MCP server (see `examples/mcp_integration.py`)
3. **For web apps:** Integrate with Flask/FastAPI
4. **For bots:** Build conversation handlers

---

## Troubleshooting

**Q: "Tool not found" error?**
```python
# Check registry
from mcp_toolkit.client import get_registry_status
print(get_registry_status())

# Register tools first
from mcp_toolkit.client import register_tool_handler
# ... register your tools
```

**Q: Import errors?**
```bash
# Make sure you're in the right directory
cd mcp_toolkit

# Or use full path
python /full/path/to/mcp_toolkit/examples/basic_usage.py
```

**Q: Want to see what's available?**
```python
from mcp_toolkit.client import list_available_tools
print(list_available_tools())
```

---

**Ready to code!** Start with one of the examples above. 🚀
