from typing import Dict, List, Any
from schema import DesignSpec, EvaluationResult

class DataScorer:
    """Standalone data scoring module for evaluation metrics"""
    
    def __init__(self):
        self.weights = {
            "completeness": 0.4,
            "format_validity": 0.3,
            "feasibility": 0.3
        }
    
    def score_completeness(self, spec: DesignSpec) -> float:
        """Score specification completeness"""
        score = 0
        max_score = 100
        
        # Building type (20 points)
        if spec.building_type and spec.building_type != "general":
            score += 20
        elif spec.building_type == "general":
            score += 10
        
        # Stories (15 points)
        if spec.stories and spec.stories > 0:
            score += 15
        
        # Materials (25 points)
        if spec.materials:
            score += 20
            if any(m.grade for m in spec.materials):
                score += 5
        
        # Dimensions (25 points)
        if spec.dimensions.length and spec.dimensions.width:
            score += 20
            if spec.dimensions.area:
                score += 5
        
        # Features (15 points)
        if spec.features:
            score += min(15, len(spec.features) * 5)
        
        return min(score, max_score)
    
    def score_format_validity(self, spec: DesignSpec) -> float:
        """Score format validity"""
        try:
            # Pydantic validation handles most format checks
            spec.model_validate(spec.model_dump())
            return 100.0
        except Exception:
            return 0.0
    
    def score_feasibility(self, spec: DesignSpec) -> float:
        """Score structural and design feasibility"""
        score = 100
        
        # Check material compatibility
        if spec.materials:
            material_types = [m.type for m in spec.materials]
            if "wood" in material_types and spec.stories > 5:
                score -= 20  # Wood not suitable for tall buildings
        
        # Check dimension reasonableness
        if spec.dimensions.length and spec.dimensions.width:
            area = spec.dimensions.length * spec.dimensions.width
            if area < 50:  # Too small
                score -= 15
            elif area > 10000:  # Too large without justification
                score -= 10
        
        # Check story height consistency
        if spec.stories and spec.dimensions.height:
            avg_height = spec.dimensions.height / spec.stories
            if avg_height < 2.5 or avg_height > 5.0:
                score -= 10
        
        return max(score, 0)
    
    def calculate_overall_score(self, completeness: float, format_validity: float, feasibility: float) -> float:
        """Calculate weighted overall score"""
        return (
            completeness * self.weights["completeness"] +
            format_validity * self.weights["format_validity"] +
            feasibility * self.weights["feasibility"]
        )
    
    def generate_feedback(self, spec: DesignSpec, scores: Dict[str, float]) -> List[str]:
        """Generate feedback based on scores"""
        feedback = []
        
        if scores["completeness"] < 80:
            if not spec.building_type or spec.building_type == "general":
                feedback.append("Building type not specified or too generic")
            if not spec.materials:
                feedback.append("Materials not specified")
            if not spec.dimensions.length or not spec.dimensions.width:
                feedback.append("Dimensions incomplete")
        
        if scores["feasibility"] < 80:
            if spec.stories > 5 and any(m.type == "wood" for m in spec.materials):
                feedback.append("Wood material not suitable for buildings over 5 stories")
            if spec.dimensions.area and spec.dimensions.area < 50:
                feedback.append("Building area seems too small for practical use")
        
        return feedback