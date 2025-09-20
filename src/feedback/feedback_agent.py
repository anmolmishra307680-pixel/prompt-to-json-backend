"""Feedback Agent for BHIV orchestration"""

import os
from typing import Dict, Any, List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from schema import DesignSpec, EvaluationResult

class FeedbackAgent:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.use_llm = bool(self.openai_api_key)
    
    def run(self, spec: DesignSpec, prompt: str, evaluation: EvaluationResult = None) -> Dict[str, Any]:
        """BHIV Core Hook: Single entry point for orchestration"""
        if self.use_llm:
            return self._generate_llm_feedback(spec, prompt, evaluation)
        else:
            return self._generate_heuristic_feedback(spec, prompt, evaluation)
    
    def _generate_llm_feedback(self, spec: DesignSpec, prompt: str, evaluation: EvaluationResult) -> Dict[str, Any]:
        """Generate feedback using OpenAI GPT"""
        try:
            import openai
            openai.api_key = self.openai_api_key
            
            feedback_prompt = f"""
            Analyze this design specification and provide 2-3 specific improvement suggestions:
            
            Original Prompt: {prompt}
            Current Spec: {spec.model_dump()}
            Evaluation Score: {evaluation.score if evaluation else 'N/A'}
            
            Provide actionable feedback as a JSON list of strings.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": feedback_prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            suggestions = response.choices[0].message.content.strip().split('\n')
            
            return {
                "feedback_type": "llm",
                "suggestions": suggestions[:3],  # Limit to 3 suggestions
                "confidence": 0.9,
                "source": "openai_gpt"
            }
        except Exception as e:
            print(f"LLM feedback failed, using heuristic: {e}")
            return self._generate_heuristic_feedback(spec, prompt, evaluation)
    
    def _generate_heuristic_feedback(self, spec: DesignSpec, prompt: str, evaluation: EvaluationResult) -> Dict[str, Any]:
        """Generate feedback using rule-based heuristics"""
        suggestions = []
        
        # Analyze completeness
        if not spec.materials or len(spec.materials) == 0:
            suggestions.append("Add material specifications for structural integrity")
        
        if not spec.features or len(spec.features) < 2:
            suggestions.append("Include more functional features based on building type")
        
        if spec.dimensions.area and spec.dimensions.area < 100:
            suggestions.append("Consider increasing building area for practical use")
        
        # Analyze based on building type - handle both old and new schema
        building_type = getattr(spec, 'building_type', None) or getattr(spec, 'category', None)
        design_type = getattr(spec, 'design_type', 'building')
        
        if design_type == 'building':
            if building_type == "office" and "elevator" not in spec.features:
                suggestions.append("Add elevator for multi-story office building")
            
            if building_type == "residential" and "parking" not in spec.features:
                suggestions.append("Include parking facilities for residential building")
        
        # Evaluation-based feedback
        if evaluation:
            if evaluation.score < 70:
                suggestions.append("Overall specification needs significant improvement")
            elif evaluation.score < 85:
                suggestions.append("Good specification with room for enhancement")
        
        return {
            "feedback_type": "heuristic",
            "suggestions": suggestions if suggestions else ["Specification looks good"],
            "confidence": 0.9,
            "source": "rule_based"
        }
    
    def calculate_reward(self, evaluation: EvaluationResult, previous_score: float = 0, binary_rewards: bool = False) -> float:
        """Calculate reward for RL training"""
        if binary_rewards:
            return 1.0 if evaluation.score > previous_score else -1.0
        else:
            # Continuous reward based on score improvement
            improvement = evaluation.score - previous_score
            return max(0.1, evaluation.score / 100.0 + improvement / 100.0)