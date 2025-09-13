"""Feedback Agent for BHIV orchestration"""

import os
from typing import Dict, Any, List
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
        """Generate feedback using OpenAI GPT (stub implementation)"""
        try:
            # Stub for LLM integration
            feedback_prompt = f"""
            Analyze this design specification and provide improvement feedback:
            
            Original Prompt: {prompt}
            Current Spec: {spec.model_dump()}
            Evaluation Score: {evaluation.score if evaluation else 'N/A'}
            
            Provide specific, actionable feedback for improvement.
            """
            
            # TODO: Implement actual OpenAI API call
            # response = openai.ChatCompletion.create(...)
            
            return {
                "feedback_type": "llm",
                "suggestions": [
                    "LLM feedback would be generated here",
                    "Specific improvements based on GPT analysis"
                ],
                "confidence": 0.8,
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
        
        # Analyze based on building type
        if spec.building_type == "office" and "elevator" not in spec.features:
            suggestions.append("Add elevator for multi-story office building")
        
        if spec.building_type == "residential" and "parking" not in spec.features:
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