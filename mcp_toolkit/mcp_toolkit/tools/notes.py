"""
Notes Tool Wrappers

Type-safe wrappers for notes MCP tools
"""
from typing import Union
import asyncio

from ..models.notes import AddNoteToFileInput, AddNoteToFileResponse, ReadNotesInput, ReadNotesResponse
from ..client import call_mcp_tool


async def add_note_to_file(input_data: Union[AddNoteToFileInput, dict]) -> AddNoteToFileResponse:
    """
    Appends the given content to the user's local notes

    Args:
        input_data: Input parameters containing content to append

    Returns:
        Confirmation of note addition
    """
    if isinstance(input_data, dict):
        input_data = AddNoteToFileInput(**input_data)

    result = await call_mcp_tool(
        'notes_service__add_note_to_file',
        input_data.model_dump(exclude_none=True)
    )

    return AddNoteToFileResponse(
        success=True,
        message="Note added successfully",
        raw_data=result if isinstance(result, dict) else {"response": result}
    )


def add_note_to_file_sync(input_data: Union[AddNoteToFileInput, dict]) -> AddNoteToFileResponse:
    """Synchronous version of add_note_to_file"""
    return asyncio.run(add_note_to_file(input_data))


async def read_notes(input_data: Union[ReadNotesInput, dict, None] = None) -> ReadNotesResponse:
    """
    Reads and returns the contents of the user's local notes

    Args:
        input_data: No parameters required (can be None)

    Returns:
        Contents of the notes file
    """
    if input_data is None:
        input_data = ReadNotesInput()
    elif isinstance(input_data, dict):
        input_data = ReadNotesInput(**input_data)

    result = await call_mcp_tool(
        'notes_service__read_notes',
        input_data.model_dump(exclude_none=True)
    )

    return ReadNotesResponse(
        content=str(result) if not isinstance(result, dict) else result.get('content', str(result)),
        raw_data=result if isinstance(result, dict) else {"response": result}
    )


def read_notes_sync(input_data: Union[ReadNotesInput, dict, None] = None) -> ReadNotesResponse:
    """Synchronous version of read_notes"""
    return asyncio.run(read_notes(input_data))
