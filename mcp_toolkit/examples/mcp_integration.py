#!/usr/bin/env python
"""
MCP Integration Example

Template for integrating with actual MCP servers
"""
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_toolkit.bridge import register_langchain_tools_sync
from mcp_toolkit.client import get_registry_status, list_available_tools, call_mcp_tool


async def setup_mcp_client():
    """
    Setup MCP client and get tools

    Using LangChain MCP Adapter with configured servers
    """
    print("Setting up MCP client...")

    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient

        # Configure MCP servers using existing Master_MCP servers
        server_params = {
            "crypto": {
                "command": "uv",
                "args": [
                    "--directory",
                    "C:\\Users\\nayak\\Documents\\Master_MCP\\mcp-server-deep-functionality",
                    "run",
                    "crypto.py"
                ],
                "transport": "stdio"
            },
            "websearch": {
                "command": "uv",
                "args": [
                    "--directory",
                    "C:\\Users\\nayak\\Documents\\Master_MCP\\mcp-server-deep-functionality",
                    "run",
                    "websearch.py"
                ],
                "transport": "stdio"
            },
            "local": {
                "command": "uv",
                "args": [
                    "--directory",
                    "C:\\Users\\nayak\\Documents\\Master_MCP\\mcp-server-deep-functionality",
                    "run",
                    "local.py"
                ],
                "transport": "stdio"
            }
        }

        print("Connecting to MCP servers...")
        client = MultiServerMCPClient(server_params)
        tools = await client.get_tools()

        print(f"[OK] Retrieved {len(tools)} tools from MCP servers")
        for tool in tools:
            print(f"  - {tool.name}")

        return tools

    except ImportError as e:
        print(f"[X] Missing dependency: {e}")
        print("[!] Install with: pip install langchain-mcp-adapters")
        return []
    except Exception as e:
        print(f"[X] Error connecting to MCP servers: {e}")
        print("[!] Make sure the server paths are correct")
        return []


def register_and_verify_tools(tools):
    """
    Register tools and verify registration

    Args:
        tools: List of LangChain StructuredTool objects
    """
    if not tools:
        print("\n[X] No tools to register")
        print("[!] Configure your MCP server in setup_mcp_client()")
        return False

    print(f"\nRegistering {len(tools)} tools...")

    # Register with the bridge
    register_langchain_tools_sync(tools)

    # Verify registration
    status = get_registry_status()
    registered_tools = list_available_tools()

    print(f"\n[OK] Registration complete!")
    print(f"   Total tools registered: {status['total_tools']}")
    print(f"   Registered tools:")
    for tool_id in registered_tools:
        print(f"     • {tool_id}")

    return True


async def use_registered_tools():
    """
    Example of using registered tools
    """
    print("\n" + "="*70)
    print("USING REGISTERED TOOLS")
    print("="*70)

    # Check registry
    status = get_registry_status()

    if status['total_tools'] == 0:
        print("\n[X] No tools registered")
        print("[!] Run setup first to register tools")
        return

    # Example: Using cryptocurrency price tool
    try:
        print("\n[*] Getting Bitcoin price...")

        # Call the registered tool directly
        result = await call_mcp_tool(
            "crypto_service__get_cryptocurrency_price",
            {"crypto": "bitcoin"}
        )

        print(f"\n[OK] Cryptocurrency Price Results:")
        print(f"   Result: {result}")

    except Exception as e:
        print(f"\n[X] Error: {e}")
        import traceback
        traceback.print_exc()


async def main_async():
    """Async main function"""
    print("="*70)
    print("MCP INTEGRATION EXAMPLE")
    print("="*70)

    # Step 1: Setup MCP client and get tools
    print("\n[Step 1] Setting up MCP client...")
    tools = await setup_mcp_client()

    if not tools:
        print("\n[!]  Running in demo mode without MCP server")
        print("\n[!] To use with actual MCP server:")
        print("   1. Edit examples/mcp_integration.py")
        print("   2. Uncomment and configure your MCP server")
        print("   3. Run this script again")
        return

    # Step 2: Register tools
    print("\n[Step 2] Registering tools...")
    success = register_and_verify_tools(tools)

    if not success:
        return

    # Step 3: Use the tools
    print("\n[Step 3] Using registered tools...")
    await use_registered_tools()

    print("\n" + "="*70)
    print("[OK] Integration example completed!")
    print("="*70)


def main():
    """Main entry point"""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n[X] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
