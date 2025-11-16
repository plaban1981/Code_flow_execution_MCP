"""
MCP Tool Wrappers

Type-safe wrappers for all MCP tools
"""
from .weather import get_weather, get_weather_sync
from .web import perform_web_search, perform_web_search_sync
from .notes import add_note_to_file, add_note_to_file_sync, read_notes, read_notes_sync
from .crypto import get_cryptocurrency_price, get_cryptocurrency_price_sync

__all__ = [
    # Weather
    'get_weather',
    'get_weather_sync',
    # Web
    'perform_web_search',
    'perform_web_search_sync',
    # Notes
    'add_note_to_file',
    'add_note_to_file_sync',
    'read_notes',
    'read_notes_sync',
    # Crypto
    'get_cryptocurrency_price',
    'get_cryptocurrency_price_sync',
]
