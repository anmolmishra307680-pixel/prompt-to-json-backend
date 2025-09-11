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

class SQLiteStorage(DatabaseInterface):
    """SQLite database implementation"""
    
    def __init__(self, db_path: str = "prompt_to_json.db"):
        import sqlite3
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS specifications (
                id INTEGER PRIMARY KEY,
                prompt TEXT,
                spec_json TEXT,
                score REAL,
                timestamp TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY,
                spec_id INTEGER,
                evaluation_json TEXT,
                timestamp TEXT,
                FOREIGN KEY (spec_id) REFERENCES specifications (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_specification(self, spec: DesignSpec, prompt: str) -> str:
        """Save specification to database"""
        import sqlite3
        import json
        from datetime import datetime
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO specifications (prompt, spec_json, timestamp) VALUES (?, ?, ?)",
            (prompt, json.dumps(spec.model_dump(), default=str), datetime.now().isoformat())
        )
        
        spec_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return str(spec_id)
    
    def save_evaluation(self, evaluation: EvaluationResult, spec_id: str) -> str:
        """Save evaluation to database"""
        import sqlite3
        import json
        from datetime import datetime
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO evaluations (spec_id, evaluation_json, timestamp) VALUES (?, ?, ?)",
            (int(spec_id), json.dumps(evaluation.model_dump(), default=str), datetime.now().isoformat())
        )
        
        eval_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return str(eval_id)
    
    def get_specifications(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve specifications from database"""
        import sqlite3
        import json
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, prompt, spec_json, score, timestamp FROM specifications ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "prompt": row[1],
                "specification": json.loads(row[2]),
                "score": row[3],
                "timestamp": row[4]
            })
        
        conn.close()
        return results
    
    def get_feedback_history(self, prompt_similarity: float = 0.3) -> List[Dict[str, Any]]:
        """Get feedback history for similar prompts"""
        # Simple implementation - return recent specs
        return self.get_specifications(50)