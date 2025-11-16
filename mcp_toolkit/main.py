#!/usr/bin/env python
"""
MCP Toolkit - Main Entry Point

Command-line interface for MCP toolkit operations
"""
import sys
import logging
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


def setup_async():
    """Setup async environment"""
    try:
        import nest_asyncio
        nest_asyncio.apply()
        logger.debug("nest_asyncio configured")
    except ImportError:
        logger.warning("nest_asyncio not available")


def cmd_demo():
    """Run token efficiency demonstration"""
    setup_async()
    print("Token Efficiency Demonstration")
    print("="*60)
    print("This feature requires the tracking module to be fully implemented.")
    print("See examples/token_demo.py for usage")


def cmd_verify():
    """Verify installation"""
    setup_async()
    from mcp_toolkit.client import get_registry_status

    print("Verification Status")
    print("="*60)

    status = get_registry_status()
    print(f"Tools registered: {status['total_tools']}")
    print(f"Jupyter mode: {status['jupyter_mode']}")
    print(f"nest_asyncio available: {status['nest_asyncio_available']}")

    if status['total_tools'] > 0:
        print(f"\nRegistered tools:")
        for tool in status['tools']:
            print(f"  - {tool}")
    else:
        print("\nNo tools registered yet.")
        print("Use register_langchain_tools_sync() to register tools.")


def cmd_debug():
    """Show debug information"""
    setup_async()
    print("MCP Toolkit Debug Information")
    print("="*60)

    try:
        from mcp_toolkit.client import get_registry_status, list_available_tools

        status = get_registry_status()
        tools = list_available_tools()

        print(f"Registry Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")

        print(f"\nAvailable Tools ({len(tools)}):")
        for tool_id, handler in tools.items():
            print(f"  {tool_id}: {handler}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="MCP Toolkit - Type-safe MCP tool wrappers"
    )
    parser.add_argument(
        'command',
        choices=['demo', 'verify', 'debug'],
        help='Command to execute'
    )

    args = parser.parse_args()

    commands = {
        'demo': cmd_demo,
        'verify': cmd_verify,
        'debug': cmd_debug
    }

    commands[args.command]()


if __name__ == '__main__':
    main()
