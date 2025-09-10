from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import json
import os
import re

class DesignSpec(BaseModel):
    type: str = Field(..., min_length=1)
    material: List[str] = []
    color: Optional[str] = None
    dimensions: Optional[str] = None
    purpose: Optional[str] = None
    extras: Optional[str] = None

    @field_validator('type')
    @classmethod
    def type_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('type cannot be empty')
        return v.strip()

def save_spec(raw: dict, filename: str = None):
    spec = DesignSpec(**raw)
    os.makedirs("data/spec_outputs", exist_ok=True)
    if not filename:
        safe_type = re.sub(r'[^a-z0-9-_]', '_', spec.type.lower())
        filename = f"data/spec_outputs/{safe_type}.json"
    with open(filename, "w") as f:
        f.write(spec.model_dump_json(indent=4))
    return filename