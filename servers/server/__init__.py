"""
server - MCP Server Tools

Available tools: 5
  - get_weather: 
Gets the weather given a location
Args:
    location: locat
  - perform_web_search: 
Performs a web search 

Args:
    query (str): _description
  - add_note_to_file: 
Appends the given content to the user's local notes.
Args:

  - read_notes: 
Reads and returns the contents of the user's local notes.

  - get_cryptocurrency_price: 
Gets the price of a cryptocurrency.
Args:
    crypto: symbo
"""

from .get_weather import get_weather
from .perform_web_search import perform_web_search
from .add_note_to_file import add_note_to_file
from .read_notes import read_notes
from .get_cryptocurrency_price import get_cryptocurrency_price

__all__ = [
    "get_weather",
    "perform_web_search",
    "add_note_to_file",
    "read_notes",
    "get_cryptocurrency_price",
]