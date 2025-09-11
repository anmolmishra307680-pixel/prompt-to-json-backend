"""Base evaluator class for all prompt types."""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseEvaluator(ABC):
    """Abstract base class for all evaluators."""
    
    @abstractmethod
    def evaluate(self, prompt: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate specification against prompt.
        
        Returns:
            dict: {
                "critic_feedback": str,
                "issues": List[str],
                "severity": str,
                "scores": Dict[str, float]
            }
        """
        pass