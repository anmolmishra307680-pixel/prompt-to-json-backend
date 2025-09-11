"""Pydantic models for email specifications."""

from pydantic import BaseModel, Field
from typing import Optional

class EmailSpec(BaseModel):
    type: str = Field(default="email", description="Type of specification")
    to: str = Field(..., description="Email recipient")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    tone: Optional[str] = Field(None, description="Email tone (formal, casual, friendly, etc.)")