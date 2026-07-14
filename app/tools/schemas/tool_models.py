from typing import Any, Optional
from pydantic import BaseModel, Field


class ToolRequest(BaseModel):
    """
    Base request sent to a tool.
    Specific tools can inherit from this class.
    """
    pass


class ToolResponse(BaseModel):
    """
    Standard response returned by every tool.
    """
    success: bool = Field(..., description="Whether the tool executed successfully.")
    message: str = Field(..., description="Human-readable result.")
    data: Optional[Any] = Field(
        default=None,
        description="Structured data returned by the tool."
    )