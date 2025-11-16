"""
read_notes - 
Reads and returns the contents of the user's local notes.


Server: server
Tool ID: server__read_notes
"""

from typing import Dict, Any, Optional, List
import sys
import os

# Add parent directory to path to import mcp_client
_current_dir = os.path.dirname(os.path.abspath(__file__))
_servers_dir = os.path.dirname(_current_dir)
if _servers_dir not in sys.path:
    sys.path.insert(0, _servers_dir)

from mcp_client import call_mcp_tool


def read_notes() -> Dict[str, Any]:
    """
    
Reads and returns the contents of the user's local notes.

    
    
    Returns:
        Dict containing the tool execution result
    """
    # Prepare parameters
    params = {
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Call MCP tool
    return call_mcp_tool("server__read_notes", params)