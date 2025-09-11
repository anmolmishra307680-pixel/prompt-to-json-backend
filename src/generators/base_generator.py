"""Base generator class for all prompt types."""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseGenerator(ABC):
    """Abstract base class for all generators."""
    
    @abstractmethod
    def generate_spec(self, prompt: str) -> Dict[str, Any]:
        """Generate specification from prompt.
        
        Returns:
            dict: {
                "spec": dict,
                "llm_output": str,
                "method": "llm"|"rules"
            }
        """
        pass