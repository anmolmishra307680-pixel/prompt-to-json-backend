"""Pydantic models for design/furniture specifications."""

from pydantic import BaseModel, Field
from typing import Optional, Union, List, Dict, Any

class Dimensions(BaseModel):
    raw: Optional[str] = None
    width_cm: Optional[float] = None
    height_cm: Optional[float] = None
    depth_cm: Optional[float] = None

class Metadata(BaseModel):
    generated_by: Optional[str] = None
    confidence: Optional[float] = None

class DesignSpec(BaseModel):
    type: str = Field(..., description="Type of furniture/design item")
    material: Optional[Union[str, List[str]]] = None
    color: Optional[str] = None
    dimensions: Optional[Dimensions] = None
    purpose: Optional[str] = None
    metadata: Optional[Metadata] = None