"""
Cryptocurrency Service Data Models

Pydantic models for cryptocurrency price service input/output
"""
from typing import Optional
from pydantic import BaseModel, Field


class GetCryptocurrencyPriceInput(BaseModel):
    """Input parameters for getting cryptocurrency price"""
    crypto: str = Field(description="Symbol of the cryptocurrency (e.g., 'bitcoin', 'ethereum')")


class GetCryptocurrencyPriceResponse(BaseModel):
    """Response from cryptocurrency price service"""
    crypto: str
    price: Optional[float] = None
    currency: str = "USD"
    raw_data: dict = Field(default_factory=dict)
