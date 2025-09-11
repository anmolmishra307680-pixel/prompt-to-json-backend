import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from schema import DesignSpec, EvaluationResult

class FeedbackLoop:
    def __init__(self, feedback_log_path: str = "logs/feedback_log.json"):
        self.feedback_log_path = Path(feedback_log_path)
        self.feedback_log_path.parent.mkdir(exist_ok=True)
        self.feedback_history = self._load_feedback_history()
    
    def _load_feedback_history(self) -> List[Dict[str, Any]]:
        """Load existing feedback history"""
        if self.feedback_log_path.exists():
            try:
                with open(self.feedback_log_path, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        return []
                    return json.loads(content)
            except (json.JSONDecodeError, FileNotFoundError):
                # Reset corrupted file
                with open(self.feedback_log_path, 'w') as f:
                    json.dump([], f)
                return []
        return []
    
    def _save_feedback_history(self):
        """Save feedback history to file"""
        with open(self.feedback_log_path, 'w') as f:
            json.dump(self.feedback_history, f, indent=2, default=str)
    
    def log_iteration(self, prompt: str, spec_before: DesignSpec, spec_after: DesignSpec, 
                     evaluation: EvaluationResult, reward: float, iteration: int):
        """Log a feedback iteration"""
        feedback_entry = {
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "spec_before": spec_before.model_dump(),
            "spec_after": spec_after.model_dump(),
            "evaluation": evaluation.model_dump(),
            "reward": reward,
            "improvements": self._calculate_improvements(spec_before, spec_after, evaluation)
        }
        
        self.feedback_history.append(feedback_entry)
        self._save_feedback_history()
    
    def _calculate_improvements(self, spec_before: DesignSpec, spec_after: DesignSpec, 
                              evaluation: EvaluationResult) -> Dict[str, Any]:
        """Calculate improvements between iterations"""
        improvements = {
            "added_materials": len(spec_after.materials) - len(spec_before.materials),
            "added_features": len(spec_after.features) - len(spec_before.features),
            "dimension_changes": {},
            "evaluation_score": evaluation.score
        }
        
        # Check dimension improvements
        if spec_before.dimensions.length != spec_after.dimensions.length:
            improvements["dimension_changes"]["length"] = {
                "before": spec_before.dimensions.length,
                "after": spec_after.dimensions.length
            }
        
        return improvements
    
    def get_feedback_for_prompt(self, prompt: str) -> List[str]:
        """Get feedback suggestions based on similar prompts"""
        suggestions = []
        
        # Find similar prompts in history
        for entry in self.feedback_history:
            if self._is_similar_prompt(prompt, entry["prompt"]):
                if entry["evaluation"]["score"] > 80:
                    # Extract successful patterns
                    spec = entry["spec_after"]
                    if spec["materials"]:
                        suggestions.append(f"Consider using {spec['materials'][0]['type']} material")
                    if spec["features"]:
                        suggestions.append(f"Add features like {', '.join(spec['features'][:2])}")
        
        return list(set(suggestions))  # Remove duplicates
    
    def _is_similar_prompt(self, prompt1: str, prompt2: str) -> bool:
        """Check if two prompts are similar"""
        words1 = set(prompt1.lower().split())
        words2 = set(prompt2.lower().split())
        
        # Simple similarity based on common words
        common_words = words1.intersection(words2)
        return len(common_words) / max(len(words1), len(words2)) > 0.3
    
    def calculate_reward(self, evaluation: EvaluationResult, previous_score: float = 0) -> float:
        """Calculate reward based on evaluation results"""
        base_reward = evaluation.score / 100.0  # Normalize to 0-1
        
        # Bonus for improvement
        improvement_bonus = max(0, (evaluation.score - previous_score) / 100.0)
        
        # Penalty for low scores
        penalty = 0
        if evaluation.score < 50:
            penalty = -0.2
        
        return base_reward + improvement_bonus + penalty
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Generate learning insights from feedback history"""
        if not self.feedback_history:
            return {"message": "No feedback history available"}
        
        scores = [entry["evaluation"]["score"] for entry in self.feedback_history]
        rewards = [entry["reward"] for entry in self.feedback_history]
        
        return {
            "total_iterations": len(self.feedback_history),
            "average_score": sum(scores) / len(scores),
            "score_trend": "improving" if scores[-1] > scores[0] else "declining",
            "average_reward": sum(rewards) / len(rewards),
            "best_iteration": max(self.feedback_history, key=lambda x: x["evaluation"]["score"])["iteration"],
            "common_successful_patterns": self._extract_successful_patterns()
        }
    
    def _extract_successful_patterns(self) -> List[str]:
        """Extract patterns from successful iterations"""
        successful_entries = [e for e in self.feedback_history if e["evaluation"]["score"] > 80]
        
        patterns = []
        if successful_entries:
            # Find common materials in successful specs
            materials = []
            for entry in successful_entries:
                materials.extend([m["type"] for m in entry["spec_after"]["materials"]])
            
            if materials:
                most_common_material = max(set(materials), key=materials.count)
                patterns.append(f"Using {most_common_material} material leads to better results")
        
        return patterns