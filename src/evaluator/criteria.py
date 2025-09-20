import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from schema import DesignSpec, EvaluationResult
from universal_schema import UniversalDesignSpec
from typing import List, Tuple

class EvaluationCriteria:
    def __init__(self):
        self.weights = {
            'completeness': 0.4,
            'format_validity': 0.3,
            'feasibility': 0.3
        }

    def check_completeness(self, spec) -> Tuple[float, List[str]]:
        """Check completeness of design specification"""
        score = 0
        feedback = []

        # Detect design type
        design_type = getattr(spec, 'design_type', 'building')

        # Type/category check - handle both old and new schema
        category = getattr(spec, 'building_type', None) or getattr(spec, 'category', None)
        if category and category != 'general':
            score += 20
        else:
            type_name = design_type.title() if design_type != 'building' else 'Building'
            feedback.append(f"{type_name} type not specified or too generic")

        # Design-specific completeness checks
        if design_type == 'building':
            stories = getattr(spec, 'stories', 1)
            if stories and stories > 0:
                score += 20
            else:
                feedback.append("Number of stories not specified")
        elif design_type == 'vehicle':
            # Check for vehicle-specific dimensions
            if (spec.dimensions.height or spec.dimensions.width or
                spec.dimensions.diameter or spec.dimensions.length):
                score += 20
            else:
                feedback.append("Vehicle dimensions not specified")
        else:
            # For electronics, appliances, furniture - check any dimension
            if (spec.dimensions.length or spec.dimensions.width or
                spec.dimensions.height or spec.dimensions.diameter):
                score += 20
            else:
                feedback.append(f"{design_type.title()} dimensions not specified")

        if spec.materials:
            score += 20
        else:
            feedback.append("No materials specified")

        if spec.dimensions.length or spec.dimensions.width or spec.dimensions.area or spec.dimensions.height:
            score += 20
        else:
            feedback.append("No dimensions specified")

        if spec.features:
            score += 20
        else:
            feedback.append("No special features specified")

        return score, feedback

    def check_format_validity(self, spec) -> Tuple[float, List[str]]:
        """Check format validity of specification"""
        score = 100
        feedback = []

        try:
            # Validate Pydantic model
            spec.model_validate(spec.model_dump())
        except Exception as e:
            score -= 50
            feedback.append(f"Schema validation error: {str(e)}")

        # Check data types - handle both schemas
        stories = getattr(spec, 'stories', 1)
        if stories and (not isinstance(stories, int) or stories < 1):
            score -= 25
            feedback.append("Invalid number of stories")

        if spec.dimensions.length and spec.dimensions.length <= 0:
            score -= 25
            feedback.append("Invalid dimensions")

        return max(0, score), feedback

    def check_feasibility(self, spec) -> Tuple[float, List[str]]:
        """Check feasibility of design"""
        score = 100
        feedback = []

        # Get design type
        design_type = getattr(spec, 'design_type', 'building')

        if design_type == 'building':
            # Building-specific feasibility checks
            stories = getattr(spec, 'stories', 1)
            if stories and stories > 50:
                score -= 30
                feedback.append("Excessive number of stories may not be feasible")

            if spec.dimensions.height and spec.dimensions.height > 200:
                score -= 20
                feedback.append("Building height may be excessive")

            # Material compatibility for buildings
            materials = [m.type for m in spec.materials] if spec.materials else []
            if 'wood' in materials and stories and stories > 5:
                score -= 25
                feedback.append("Wood construction may not be suitable for high-rise buildings")

        elif design_type == 'vehicle':
            # Vehicle-specific feasibility checks
            if spec.dimensions.length and spec.dimensions.length > 20:
                score -= 20
                feedback.append("Vehicle length may be excessive for standard roads")

            if spec.dimensions.height and spec.dimensions.height > 4:
                score -= 15
                feedback.append("Vehicle height may exceed bridge clearances")

            materials = [m.type for m in spec.materials] if spec.materials else []
            if 'wood' in materials:
                score -= 20
                feedback.append("Wood may not be suitable for vehicle construction")

        elif design_type == 'electronics':
            # Electronics feasibility checks
            if spec.dimensions.weight and spec.dimensions.weight > 10:
                score -= 15
                feedback.append("Device may be too heavy for portable use")

        elif design_type == 'appliance':
            # Appliance feasibility checks
            if spec.dimensions.width and spec.dimensions.width > 3:
                score -= 10
                feedback.append("Appliance may be too wide for standard spaces")

        elif design_type == 'furniture':
            # Furniture feasibility checks
            materials = [m.type for m in spec.materials] if spec.materials else []
            if 'steel' in materials and spec.dimensions.weight and spec.dimensions.weight > 100:
                score -= 15
                feedback.append("Steel furniture may be too heavy for practical use")

        return max(0, score), feedback

    def evaluate(self, spec) -> EvaluationResult:
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
