"""Schema registry for mapping prompt types to schemas and examples."""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
try:
    import jsonschema
except ImportError:
    jsonschema = None

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

def validate_spec(spec: Dict[str, Any], prompt_type: str) -> Dict[str, Any]:
    """Validate spec against schema for given type."""
    if prompt_type not in REGISTER or not REGISTER[prompt_type]["schema_file"]:
        return {"valid": True, "errors": []}
    
    # Load schema
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), REGISTER[prompt_type]["schema_file"])
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
    except FileNotFoundError:
        return {"valid": False, "errors": [f"Schema file not found: {schema_path}"]}
    
    # Validate using jsonschema if available
    if jsonschema:
        try:
            jsonschema.validate(spec, schema)
            return {"valid": True, "errors": []}
        except jsonschema.ValidationError as e:
            return {"valid": False, "errors": [str(e)]}
        except Exception as e:
            return {"valid": False, "errors": [f"Validation error: {str(e)}"]}
    
    # Basic validation without jsonschema
    errors = []
    required = schema.get("required", [])
    for field in required:
        if field not in spec:
            errors.append(f"Missing required field: {field}")
    
    return {"valid": len(errors) == 0, "errors": errors}

def save_valid_spec(spec: Dict[str, Any], prompt_type: str, out_dir: str = "spec_outputs") -> str:
    """Save validated spec to output directory."""
    # Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    spec_type = spec.get("type", prompt_type)
    filename = f"{spec_type}_{timestamp}.json"
    filepath = os.path.join(out_dir, filename)
    
    # Save spec
    with open(filepath, 'w') as f:
        json.dump(spec, f, indent=2)
    
    return filepath

def save_invalid_spec(spec: Dict[str, Any], errors: List[str], prompt_type: str) -> Dict[str, str]:
    """Save invalid spec and errors for debugging."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save invalid spec
    os.makedirs("spec_outputs", exist_ok=True)
    spec_filename = f"invalid_{prompt_type}_{timestamp}.json"
    spec_path = os.path.join("spec_outputs", spec_filename)
    
    with open(spec_path, 'w') as f:
        json.dump({"spec": spec, "errors": errors, "timestamp": timestamp}, f, indent=2)
    
    # Save validation errors
    os.makedirs("reports", exist_ok=True)
    error_path = os.path.join("reports", "validation_errors.txt")
    
    with open(error_path, 'a') as f:
        f.write(f"\n=== Validation Error {timestamp} ===\n")
        f.write(f"Type: {prompt_type}\n")
        f.write(f"Spec: {json.dumps(spec, indent=2)}\n")
        f.write(f"Errors: {errors}\n")
        f.write("=" * 50 + "\n")
    
    return {"spec_path": spec_path, "error_path": error_path}