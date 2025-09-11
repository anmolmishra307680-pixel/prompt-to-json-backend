"""Data scorer wrapper around criteria.py for grading compliance"""

from evaluator.criteria import EvaluationCriteria
from schema import DesignSpec, EvaluationResult

class DataScorer:
    """Thin wrapper around EvaluationCriteria for compliance"""
    
    def __init__(self):
        self.criteria = EvaluationCriteria()
    
    def score_completeness(self, spec: DesignSpec) -> float:
        """Score specification completeness"""
        return self.criteria.evaluate_completeness(spec)
    
    def score_format_validity(self, spec: DesignSpec) -> float:
        """Score format validity"""
        return self.criteria.evaluate_format_validity(spec)
    
    def score_feasibility(self, spec: DesignSpec) -> float:
        """Score structural feasibility"""
        return self.criteria.evaluate_feasibility(spec)
    
    def calculate_overall_score(self, spec: DesignSpec) -> float:
        """Calculate weighted overall score"""
        completeness = self.score_completeness(spec)
        format_validity = self.score_format_validity(spec)
        feasibility = self.score_feasibility(spec)
        
        return self.criteria.calculate_weighted_score(completeness, format_validity, feasibility)
    
    def generate_evaluation(self, spec: DesignSpec, prompt: str) -> EvaluationResult:
        """Generate complete evaluation (delegates to criteria)"""
        return self.criteria.evaluate_specification(spec, prompt)