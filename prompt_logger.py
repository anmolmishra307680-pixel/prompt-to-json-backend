import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class PromptLogger:
    def __init__(self, log_path: str = "logs/logs.json"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(exist_ok=True)
        
    def log_prompt_result(self, prompt: str, result: Dict[str, Any], mode: str = "single"):
        """Log prompt and result to logs.json"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "mode": mode,
            "result": result,
            "spec_file": result.get("spec_file", ""),
            "score": result.get("evaluation", {}).get("score", 0)
        }
        
        # Load existing logs
        logs = []
        if self.log_path.exists():
            try:
                with open(self.log_path, 'r') as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logs = []
        
        # Add new entry
        logs.append(log_entry)
        
        # Save updated logs
        with open(self.log_path, 'w') as f:
            json.dump(logs, f, indent=2, default=str)
    
    def get_last_n_prompts(self, n: int = 5) -> List[Dict[str, Any]]:
        """Retrieve last N prompts"""
        if not self.log_path.exists():
            return []
        
        try:
            with open(self.log_path, 'r') as f:
                logs = json.load(f)
            return logs[-n:] if logs else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def get_all_prompts(self) -> List[Dict[str, Any]]:
        """Retrieve all logged prompts"""
        if not self.log_path.exists():
            return []
        
        try:
            with open(self.log_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []