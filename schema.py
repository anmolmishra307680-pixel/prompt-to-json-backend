from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MaterialSpec(BaseModel):
    type: str = Field(description="Material type (steel, concrete, wood, etc.)")
    grade: Optional[str] = Field(default=None, description="Material grade or specification")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Material properties")

class DimensionSpec(BaseModel):
    length: Optional[float] = Field(default=None, description="Length in meters")
    width: Optional[float] = Field(default=None, description="Width in meters") 
    height: Optional[float] = Field(default=None, description="Height in meters")
    area: Optional[float] = Field(default=None, description="Area in square meters")

class DesignSpec(BaseModel):
    building_type: str = Field(description="Type of building")
    stories: int = Field(description="Number of stories")
    materials: List[MaterialSpec] = Field(default_factory=list, description="Building materials")
    dimensions: DimensionSpec = Field(default_factory=DimensionSpec, description="Building dimensions")
    features: List[str] = Field(default_factory=list, description="Special features")
    requirements: List[str] = Field(default_factory=list, description="Design requirements")
    timestamp: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EvaluationResult(BaseModel):
    score: float = Field(description="Overall evaluation score (0-100)")
    completeness: float = Field(description="Completeness score (0-100)")
    format_validity: float = Field(description="Format validity score (0-100)")
    feedback: List[str] = Field(default_factory=list, description="Feedback comments")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Evaluation timestamp")