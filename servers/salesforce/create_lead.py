"""
createLead - Creates a new lead in Salesforce

Server: salesforce
"""

from typing import Dict, Any, Optional, List
from ..mcp_client import call_mcp_tool


def create_lead(company: str, name: str, email: str, phone: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a new lead in Salesforce
    
    Args:
        company (string, required): Company name
        name (string, required): Lead contact name
        email (string, required): Email address
        phone (string, optional): Phone number
    
    Returns:
        Dict containing the tool execution result
    """
    # Prepare parameters
    params = {
        "company": company,
        "name": name,
        "email": email,
        "phone": phone,
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Call MCP tool
    return call_mcp_tool("salesforce__createLead", params)