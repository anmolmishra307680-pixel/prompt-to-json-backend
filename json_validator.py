"""Deep JSON input validation and sanitization"""

import json
import re
from typing import Dict, Any, List, Union
from pydantic import ValidationError

class JSONValidator:
    """Comprehensive JSON input validation"""
    
    def __init__(self):
        self.max_string_length = 1000
        self.max_array_length = 100
        self.max_nesting_depth = 10
        self.allowed_keys = {
            'prompt', 'building_type', 'stories', 'materials', 'dimensions', 
            'features', 'requirements', 'type', 'grade', 'properties',
            'length', 'width', 'height', 'area'
        }
    
    def validate_json_input(self, json_data: Union[str, Dict]) -> Dict[str, Any]:
        """Validate and sanitize JSON input"""
        try:
            # Parse if string
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data
            
            # Deep validation
            validated_data = self._validate_recursive(data, depth=0)
            
            # Schema validation
            self._validate_schema(validated_data)
            
            return validated_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise ValueError(f"JSON validation failed: {str(e)}")
    
    def _validate_recursive(self, obj: Any, depth: int) -> Any:
        """Recursively validate JSON object"""
        if depth > self.max_nesting_depth:
            raise ValueError(f"JSON nesting too deep (max {self.max_nesting_depth})")
        
        if isinstance(obj, dict):
            return self._validate_dict(obj, depth)
        elif isinstance(obj, list):
            return self._validate_list(obj, depth)
        elif isinstance(obj, str):
            return self._validate_string(obj)
        elif isinstance(obj, (int, float, bool)) or obj is None:
            return obj
        else:
            raise ValueError(f"Unsupported data type: {type(obj)}")
    
    def _validate_dict(self, obj: Dict, depth: int) -> Dict:
        """Validate dictionary object"""
        if len(obj) > 50:  # Reasonable limit
            raise ValueError("Dictionary too large")
        
        validated = {}
        for key, value in obj.items():
            # Validate key
            clean_key = self._validate_string(key)
            if clean_key not in self.allowed_keys and not self._is_safe_key(clean_key):
                continue  # Skip unsafe keys
            
            # Validate value
            validated[clean_key] = self._validate_recursive(value, depth + 1)
        
        return validated
    
    def _validate_list(self, obj: List, depth: int) -> List:
        """Validate list object"""
        if len(obj) > self.max_array_length:
            raise ValueError(f"Array too large (max {self.max_array_length})")
        
        return [self._validate_recursive(item, depth + 1) for item in obj]
    
    def _validate_string(self, obj: str) -> str:
        """Validate and sanitize string"""
        if len(obj) > self.max_string_length:
            obj = obj[:self.max_string_length]
        
        # Remove potentially dangerous characters
        obj = re.sub(r'[<>"\']', '', obj)
        
        # Remove control characters
        obj = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', obj)
        
        return obj.strip()
    
    def _is_safe_key(self, key: str) -> bool:
        """Check if key is safe to use"""
        # Allow alphanumeric and underscore
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key) is not None
    
    def _validate_schema(self, data: Dict) -> None:
        """Validate against expected schema"""
        if not isinstance(data, dict):
            raise ValueError("Root object must be a dictionary")
        
        # Check for required fields in specification
        if 'specification' in data:
            spec = data['specification']
            required_fields = ['building_type', 'stories', 'materials', 'dimensions', 'features']
            
            for field in required_fields:
                if field not in spec:
                    raise ValueError(f"Missing required field: {field}")
        
        # Validate specific field types
        if 'stories' in data and not isinstance(data['stories'], int):
            raise ValueError("Stories must be an integer")
        
        if 'materials' in data and not isinstance(data['materials'], list):
            raise ValueError("Materials must be a list")

class InputSanitizer:
    """Input sanitization for prompts and text"""
    
    @staticmethod
    def sanitize_prompt(prompt: str) -> str:
        """Sanitize user prompt input"""
        if not isinstance(prompt, str):
            raise ValueError("Prompt must be a string")
        
        # Remove HTML tags
        prompt = re.sub(r'<[^>]+>', '', prompt)
        
        # Remove script tags and content
        prompt = re.sub(r'<script.*?</script>', '', prompt, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove potentially dangerous characters
        prompt = re.sub(r'[<>"\']', '', prompt)
        
        # Normalize whitespace
        prompt = re.sub(r'\s+', ' ', prompt).strip()
        
        # Length validation
        if len(prompt) < 3:
            raise ValueError("Prompt too short (minimum 3 characters)")
        if len(prompt) > 1000:
            raise ValueError("Prompt too long (maximum 1000 characters)")
        
        return prompt
    
    @staticmethod
    def validate_file_path(file_path: str) -> str:
        """Validate file path for security"""
        import os
        
        # Prevent directory traversal
        if '..' in file_path or file_path.startswith('/'):
            raise ValueError("Invalid file path")
        
        # Only allow specific extensions
        allowed_extensions = {'.json', '.txt', '.log'}
        _, ext = os.path.splitext(file_path)
        if ext not in allowed_extensions:
            raise ValueError(f"File extension not allowed: {ext}")
        
        return file_path