"""
updateRecord - Updates a record in Salesforce

Server: salesforce
"""

from typing import Dict, Any, Optional, List
from ..mcp_client import call_mcp_tool


def update_record(object_type: str, record_id: str, data: Dict) -> Dict[str, Any]:
    """
    Updates a record in Salesforce
    
    Args:
        object_type (string, required): Type of Salesforce object (Lead, Contact, Account, etc.)
        record_id (string, required): The ID of the record to update
        data (object, required): Fields to update with their new values
    
    Returns:
        Dict containing the tool execution result
    """
    # Prepare parameters
    params = {
        "object_type": object_type,
        "record_id": record_id,
        "data": data,
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Call MCP tool
    return call_mcp_tool("salesforce__updateRecord", params)