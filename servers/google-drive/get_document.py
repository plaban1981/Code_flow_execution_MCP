"""
getDocument - Retrieves a document from Google Drive

Server: google-drive
"""

from typing import Dict, Any, Optional, List
from ..mcp_client import call_mcp_tool


def get_document(document_id: str, fields: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves a document from Google Drive
    
    Args:
        document_id (string, required): The ID of the document to retrieve
        fields (string, optional): Specific fields to return (comma-separated)
    
    Returns:
        Dict containing the tool execution result
    """
    # Prepare parameters
    params = {
        "document_id": document_id,
        "fields": fields,
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Call MCP tool
    return call_mcp_tool("google-drive__getDocument", params)