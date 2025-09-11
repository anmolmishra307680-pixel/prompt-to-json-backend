"""Schema registry for mapping prompt types to schemas and examples."""

import json
import os
from typing import Dict, List, Any

REGISTER = {
    "design": {
        "schema_file": "spec_schemas/design_schema.json",
        "pydantic": "src/schemas/design.py",
        "examples": [
            "Create a wooden dining table",
            "Design a modern steel chair with leather cushions",
            "Build a glass coffee table with metal legs"
        ],
        "help": "Use furniture/design prompts like 'Create a wooden table' or 'Design a modern chair'"
    },
    "email": {
        "schema_file": "spec_schemas/email_schema.json", 
        "pydantic": "src/schemas/email.py",
        "examples": [
            "Write an email to john@example.com about the meeting",
            "Send a formal email to the team about project updates",
            "Draft a friendly email to customers about new features"
        ],
        "help": "Use email prompts like 'Write an email to...' or 'Send a message about...'"
    },
    "code": {
        "schema_file": None,
        "pydantic": None,
        "examples": [
            "Write a Python function to sort a list",
            "Create a JavaScript component for login",
            "Generate SQL query to find users"
        ],
        "help": "Use code prompts like 'Write a function...' or 'Create a script...'"
    },
    "document": {
        "schema_file": None,
        "pydantic": None,
        "examples": [
            "Write a report on quarterly sales",
            "Create documentation for the API",
            "Draft a proposal for the new project"
        ],
        "help": "Use document prompts like 'Write a report...' or 'Create documentation...'"
    },
    "unknown": {
        "schema_file": None,
        "pydantic": None,
        "examples": [
            "What is the weather today?",
            "Explain quantum physics",
            "Tell me a joke"
        ],
        "help": "General prompts that don't fit specific categories"
    }
}

def get_schema_for_type(prompt_type: str) -> Dict[str, Any]:
    """Get schema and examples for a prompt type."""
    if prompt_type not in REGISTER:
        prompt_type = "unknown"
    
    config = REGISTER[prompt_type]
    result = {
        "type": prompt_type,
        "examples": config["examples"],
        "help": config["help"],
        "schema": None
    }
    
    # Load JSON schema if available
    if config["schema_file"]:
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config["schema_file"])
        try:
            with open(schema_path, 'r') as f:
                result["schema"] = json.load(f)
        except FileNotFoundError:
            pass
    
    return result

def get_available_types() -> List[str]:
    """Get list of available prompt types."""
    return list(REGISTER.keys())

def get_examples_for_type(prompt_type: str) -> List[str]:
    """Get example prompts for a type."""
    return REGISTER.get(prompt_type, REGISTER["unknown"])["examples"]