"""
MCP Toolkit Data Models

All Pydantic models for type-safe tool interactions
"""
from .weather import GetWeatherInput, GetWeatherResponse
from .web import PerformWebSearchInput, PerformWebSearchResponse
from .notes import (
    AddNoteToFileInput,
    AddNoteToFileResponse,
    ReadNotesInput,
    ReadNotesResponse
)
from .crypto import GetCryptocurrencyPriceInput, GetCryptocurrencyPriceResponse

__all__ = [
    # Weather
    'GetWeatherInput',
    'GetWeatherResponse',
    # Web
    'PerformWebSearchInput',
    'PerformWebSearchResponse',
    # Notes
    'AddNoteToFileInput',
    'AddNoteToFileResponse',
    'ReadNotesInput',
    'ReadNotesResponse',
    # Crypto
    'GetCryptocurrencyPriceInput',
    'GetCryptocurrencyPriceResponse',
]
