"""
Weather Service Data Models

Pydantic models for weather service input/output
"""
from typing import Optional
from pydantic import BaseModel, Field


class GetWeatherInput(BaseModel):
    """Input parameters for getting weather information"""
    location: str = Field(description="Location, can be city, country, state, etc.")


class GetWeatherResponse(BaseModel):
    """Response from weather service"""
    location: str
    temperature: Optional[float] = None
    condition: Optional[str] = None
    humidity: Optional[int] = None
    wind_speed: Optional[str] = None
    raw_data: dict = Field(default_factory=dict, description="Raw response data")
