"""
Web Search Service Data Models

Pydantic models for web search service input/output
"""
from pydantic import BaseModel, Field


class PerformWebSearchInput(BaseModel):
    """Input parameters for web search"""
    query: str = Field(description="Search query string")


class PerformWebSearchResponse(BaseModel):
    """Response from web search"""
    query: str
    results: str
    raw_data: dict = Field(default_factory=dict)
