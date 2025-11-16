"""
listFiles - List files in Google Drive

Server: google-drive
"""

from typing import Dict, Any, Optional, List
from ..mcp_client import call_mcp_tool


def list_files(folder_id: Optional[str] = None, max_results: Optional[int] = None) -> Dict[str, Any]:
    """
    List files in Google Drive
    
    Args:
        folder_id (string, optional): Folder ID to list files from
        max_results (integer, optional): Maximum number of results
    
    Returns:
        Dict containing the tool execution result
    """
    # Prepare parameters
    params = {
        "folder_id": folder_id,
        "max_results": max_results,
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Call MCP tool
    return call_mcp_tool("google-drive__listFiles", params)