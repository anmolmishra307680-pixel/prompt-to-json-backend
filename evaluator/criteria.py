from schema import DesignSpec, EvaluationResult
from typing import List, Tuple

class EvaluationCriteria:
    def __init__(self):
        self.weights = {
            'completeness': 0.4,
            'format_validity': 0.3,
            'feasibility': 0.3
        }
    
    def check_completeness(self, spec: DesignSpec) -> Tuple[float, List[str]]:
        """Check completeness of design specification"""
        score = 0
        feedback = []
        
        # Required fields check
        if spec.building_type and spec.building_type != 'general':
            score += 20
        else:
            feedback.append("Building type not specified or too generic")
        
        if spec.stories > 0:
            score += 20
        else:
            feedback.append("Number of stories not specified")
        
        if spec.materials:
            score += 20
        else:
            feedback.append("No materials specified")
        
        if spec.dimensions.length or spec.dimensions.width or spec.dimensions.area:
            score += 20
        else:
            feedback.append("No dimensions specified")
        
        if spec.features:
            score += 20
        else:
            feedback.append("No special features specified")
        
        return score, feedback
    
    def check_format_validity(self, spec: DesignSpec) -> Tuple[float, List[str]]:
        """Check format validity of specification"""
        score = 100
        feedback = []
        
        try:
            # Validate Pydantic model
            spec.model_validate(spec.model_dump())
        except Exception as e:
            score -= 50
            feedback.append(f"Schema validation error: {str(e)}")
        
        # Check data types
        if not isinstance(spec.stories, int) or spec.stories < 1:
            score -= 25
            feedback.append("Invalid number of stories")
        
        if spec.dimensions.length and spec.dimensions.length <= 0:
            score -= 25
            feedback.append("Invalid dimensions")
        
        return max(0, score), feedback
    
    def check_feasibility(self, spec: DesignSpec) -> Tuple[float, List[str]]:
        """Check feasibility of design"""
        score = 100
        feedback = []
        
        # Basic feasibility checks
        if spec.stories > 50:
            score -= 30
            feedback.append("Excessive number of stories may not be feasible")
        
        if spec.dimensions.height and spec.dimensions.height > 200:
            score -= 20
            feedback.append("Building height may be excessive")
        
        # Material compatibility
        materials = [m.type for m in spec.materials]
        if 'wood' in materials and spec.stories > 5:
            score -= 25
            feedback.append("Wood construction may not be suitable for high-rise buildings")
        
        return max(0, score), feedback
    
    def evaluate(self, spec: DesignSpec) -> EvaluationResult:
        """Perform complete evaluation of design specification"""
        completeness_score, completeness_feedback = self.check_completeness(spec)
        format_score, format_feedback = self.check_format_validity(spec)
        feasibility_score, feasibility_feedback = self.check_feasibility(spec)
        
        # Calculate weighted overall score
        overall_score = (
            completeness_score * self.weights['completeness'] +
            format_score * self.weights['format_validity'] +
            feasibility_score * self.weights['feasibility']
        )
        
        all_feedback = completeness_feedback + format_feedback + feasibility_feedback
        
        # Generate suggestions
        suggestions = []
        if completeness_score < 80:
            suggestions.append("Add more detailed specifications")
        if format_score < 90:
            suggestions.append("Fix format and validation issues")
        if feasibility_score < 80:
            suggestions.append("Review design feasibility constraints")
        
        return EvaluationResult(
            score=round(overall_score, 2),
            completeness=completeness_score,
            format_validity=format_score,
            feedback=all_feedback,
            suggestions=suggestions
        )