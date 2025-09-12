"""Data scorer wrapper around criteria.py for grading compliance"""

from evaluator.criteria import EvaluationCriteria
from schema import DesignSpec, EvaluationResult

class DataScorer:
    """Thin wrapper around EvaluationCriteria for compliance"""
    
    def __init__(self):
        self.criteria = EvaluationCriteria()
    
    def score_completeness(self, spec: DesignSpec) -> float:
        """Score specification completeness"""
        score, _ = self.criteria.check_completeness(spec)
        return score
    
    def score_format_validity(self, spec: DesignSpec) -> float:
        """Score format validity"""
        score, _ = self.criteria.check_format_validity(spec)
        return score
    
    def score_feasibility(self, spec: DesignSpec) -> float:
        """Score structural feasibility"""
        score, _ = self.criteria.check_feasibility(spec)
        return score
    
    def calculate_overall_score(self, spec: DesignSpec) -> float:
        """Calculate weighted overall score"""
        completeness = self.score_completeness(spec)
        format_validity = self.score_format_validity(spec)
        feasibility = self.score_feasibility(spec)
        
        # Use same weights as criteria
        return (
            completeness * 0.4 +
            format_validity * 0.3 +
            feasibility * 0.3
        )
    
    def generate_evaluation(self, spec: DesignSpec, prompt: str = "") -> EvaluationResult:
        """Generate complete evaluation (delegates to criteria)"""
        return self.criteria.evaluate(spec)