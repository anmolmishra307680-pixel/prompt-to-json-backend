"""Design evaluator for furniture/design specifications."""

from typing import Dict, Any, List
from .base_evaluator import BaseEvaluator
from ..data_scorer import score_design_spec

class DesignEvaluator(BaseEvaluator):
    """Evaluator for design/furniture specifications."""
    
    def evaluate(self, prompt: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate design specification."""
        # Use existing scoring logic
        scores = score_design_spec(spec, prompt)
        
        # Generate issues and feedback
        issues = []
        feedback_parts = []
        
        # Check completeness
        if scores["completeness_score"] < 3:
            issues.append("Specification incomplete")
        else:
            feedback_parts.append("specification complete")
        
        # Check material realism
        if scores["material_realism_score"] < 2:
            issues.append("Material choices questionable")
        else:
            feedback_parts.append("materials realistic")
        
        # Check dimensions
        if scores["dimension_validity_score"] < 1:
            issues.append("Dimensions missing or invalid")
        else:
            feedback_parts.append("dimensions provided")
        
        # Check type match
        if scores["type_match_score"] < 1:
            issues.append("Type may not match prompt")
        else:
            feedback_parts.append("type matches prompt")
        
        # Determine severity
        severity = self._determine_severity(scores["format_score"])
        
        # Generate feedback
        if not feedback_parts:
            feedback_parts.append("Design specification needs improvement")
        
        critic_feedback = "; ".join(feedback_parts) + "."
        
        return {
            "critic_feedback": critic_feedback,
            "issues": issues,
            "severity": severity,
            "scores": scores
        }
    
    def _determine_severity(self, format_score: float) -> str:
        """Determine severity based on format score."""
        if format_score >= 8.0:
            return "none"
        elif format_score >= 6.0:
            return "minor"
        elif format_score >= 4.0:
            return "moderate"
        else:
            return "major"