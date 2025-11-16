"""
Notes Service Data Models

Pydantic models for notes service input/output
"""
from pydantic import BaseModel, Field


class AddNoteToFileInput(BaseModel):
    """Input parameters for adding note to file"""
    content: str = Field(description="The text content to append")


class AddNoteToFileResponse(BaseModel):
    """Response from add note operation"""
    success: bool = True
    message: str = "Note added successfully"
    raw_data: dict = Field(default_factory=dict)


class ReadNotesInput(BaseModel):
    """Input parameters for reading notes (no parameters required)"""
    pass


class ReadNotesResponse(BaseModel):
    """Response from read notes operation"""
    content: str = Field(description="Contents of the notes file")
    raw_data: dict = Field(default_factory=dict)
