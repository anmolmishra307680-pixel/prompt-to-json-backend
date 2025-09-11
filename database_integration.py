"""Database integration placeholder for future scalability

This module provides interfaces for database storage when file-based
storage needs to be replaced with persistent database solutions.

Recommended implementations:
- PostgreSQL for relational data
- MongoDB for document storage
- SQLite for lightweight local storage
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from schema import DesignSpec, EvaluationResult

class DatabaseInterface(ABC):
    """Abstract interface for database operations"""
    
    @abstractmethod
    def save_specification(self, spec: DesignSpec, prompt: str) -> str:
        """Save specification to database"""
        pass
    
    @abstractmethod
    def save_evaluation(self, evaluation: EvaluationResult, spec_id: str) -> str:
        """Save evaluation to database"""
        pass
    
    @abstractmethod
    def get_specifications(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve specifications from database"""
        pass
    
    @abstractmethod
    def get_feedback_history(self, prompt_similarity: float = 0.3) -> List[Dict[str, Any]]:
        """Get feedback history for similar prompts"""
        pass

class FileBasedStorage(DatabaseInterface):
    """Current file-based storage implementation"""
    
    def save_specification(self, spec: DesignSpec, prompt: str) -> str:
        """Save to JSON file (current implementation)"""
        # Delegate to existing file-based system
        from main_agent import MainAgent
        agent = MainAgent()
        return agent.save_spec(spec, prompt)
    
    def save_evaluation(self, evaluation: EvaluationResult, spec_id: str) -> str:
        """Save evaluation to file (current implementation)"""
        # Delegate to existing evaluator system
        return "file_based_evaluation"
    
    def get_specifications(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get specifications from files"""
        # TODO: Implement file scanning
        return []
    
    def get_feedback_history(self, prompt_similarity: float = 0.3) -> List[Dict[str, Any]]:
        """Get feedback from JSON files"""
        # TODO: Implement feedback file reading
        return []

# Future database implementations would inherit from DatabaseInterface
# class PostgreSQLStorage(DatabaseInterface): ...
# class MongoDBStorage(DatabaseInterface): ...