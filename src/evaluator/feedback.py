"""Feedback generator for design specifications with heuristic and LLM enhancement."""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

# Configuration
LLM_AVAILABLE = False  # Set to True to enable LLM enhancement

def generate_heuristic_feedback(prompt: str, spec: dict, report: dict) -> Dict[str, Any]:
    """Generate feedback using heuristic rules."""
    
    feedback_parts = []
    actions = []
    
    issues = report.get('issues', [])
    quality_scores = report.get('quality_scores', {})
    
    # Handle missing or unclear type
    if 'type_missing' in issues or 'type_requirements_missing' in issues:
        feedback_parts.append("Specify the object type clearly")
        actions.append("specify_object_type")
    
    # Handle material issues
    if 'material_invalid' in issues or 'material_missing' in issues:
        if not spec.get('material'):
            feedback_parts.append("Add material specifications")
            actions.append("add_material_specification")
        else:
            feedback_parts.append("Use recognized material names (wood, metal, glass, etc.)")
            actions.append("use_standard_materials")
    
    # Handle dimension issues
    if 'dimensions_invalid' in issues or 'dimensions_missing' in issues:
        dimensions = spec.get('dimensions')
        if not dimensions:
            feedback_parts.append("Provide specific measurements with units")
            actions.append("add_dimensions_with_units")
        elif isinstance(dimensions, dict):
            if not dimensions.get('raw') or dimensions.get('raw') in ['None', '']:
                feedback_parts.append("Add dimensional measurements (length, width, height)")
                actions.append("add_dimensional_measurements")
            elif dimensions.get('raw') and not any(unit in str(dimensions.get('raw')).lower() 
                                                 for unit in ['feet', 'ft', 'cm', 'm', 'inches', 'in']):
                feedback_parts.append("Include units in dimensions (feet, meters, cm)")
                actions.append("add_dimension_units")
        
        # Check for unreasonable dimensions
        if isinstance(dimensions, dict):
            floors = dimensions.get('floors')
            area_m2 = dimensions.get('area_m2')
            
            if floors and floors > 10:
                feedback_parts.append("Consider reducing floor count for practical design")
                actions.append("reduce_floor_count")
            
            if area_m2 and area_m2 > 1000:
                feedback_parts.append("Large area specification may need subdivision")
                actions.append("consider_area_subdivision")
    
    # Handle purpose issues
    if 'purpose_missing' in issues:
        feedback_parts.append("Specify the intended use or purpose")
        actions.append("specify_purpose")
    
    # Handle eco-friendly requirements
    if 'energy_source_missing' in issues:
        feedback_parts.append("Add sustainable or energy-efficient features as requested")
        actions.append("add_sustainable_features")
    
    # Quality-based suggestions
    completeness_score = quality_scores.get('completeness_score', 0)
    material_score = quality_scores.get('material_realism_score', 0)
    dimension_score = quality_scores.get('dimension_validity_score', 0)
    
    if completeness_score < 3:
        feedback_parts.append("Improve specification completeness")
        actions.append("improve_completeness")
    
    if material_score < 2:
        feedback_parts.append("Consider material grade or quality specifications")
        actions.append("specify_material_grade")
    
    if dimension_score < 1:
        feedback_parts.append("Provide more detailed dimensional information")
        actions.append("add_detailed_dimensions")
    
    # Type-specific suggestions
    spec_type = spec.get('type', '').lower()
    if spec_type == 'building':
        if not any('floor' in str(dimensions).lower() for dimensions in [spec.get('dimensions', {})]):
            feedback_parts.append("Buildings should specify floor count")
            actions.append("add_floor_count")
    
    elif spec_type in ['table', 'chair', 'cabinet']:
        if not spec.get('dimensions'):
            feedback_parts.append(f"{spec_type.title()} should include size specifications")
            actions.append("add_furniture_dimensions")
    
    # Default positive feedback for good specs
    if not feedback_parts:
        feedback_parts.append("Specification is well-defined and complete")
        actions.append("maintain_quality")
    
    feedback_text = "; ".join(feedback_parts)
    
    return {
        "feedback_text": feedback_text,
        "actions": actions,
        "source": "heuristic"
    }

def enhance_with_llm(feedback: Dict[str, Any], prompt: str, spec: dict) -> Dict[str, Any]:
    """Enhance feedback using LLM (placeholder for actual LLM integration)."""
    
    if not LLM_AVAILABLE:
        return feedback
    
    # Placeholder for LLM enhancement
    # In a real implementation, this would call an LLM to paraphrase and expand
    enhanced_text = feedback['feedback_text']
    
    # Simple enhancement rules (would be replaced by actual LLM)
    if "Add material" in enhanced_text:
        enhanced_text = enhanced_text.replace("Add material", "Consider specifying high-quality materials such as")
    
    if "Provide specific measurements" in enhanced_text:
        enhanced_text = enhanced_text.replace("Provide specific measurements", 
                                            "Include precise dimensional specifications")
    
    feedback['feedback_text'] = enhanced_text
    feedback['source'] = "heuristic+llm"
    
    return feedback

def generate_feedback(prompt: str, spec: dict, report: dict) -> Dict[str, Any]:
    """Main feedback generation function."""
    
    # Generate heuristic feedback
    feedback = generate_heuristic_feedback(prompt, spec, report)
    
    # Enhance with LLM if available
    if LLM_AVAILABLE:
        feedback = enhance_with_llm(feedback, prompt, spec)
    
    # Add metadata
    feedback['timestamp'] = datetime.now().isoformat()
    feedback['prompt'] = prompt
    feedback['severity'] = report.get('severity', 'unknown')
    
    return feedback

def log_feedback(feedback: Dict[str, Any]) -> str:
    """Log feedback to feedback_log.jsonl."""
    
    os.makedirs("rl_logs", exist_ok=True)
    
    log_entry = {
        "timestamp": feedback.get('timestamp', datetime.now().isoformat()),
        "prompt": feedback.get('prompt', ''),
        "feedback_text": feedback.get('feedback_text', ''),
        "actions": feedback.get('actions', []),
        "source": feedback.get('source', 'unknown'),
        "severity": feedback.get('severity', 'unknown')
    }
    
    with open("feedback_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    return "feedback_log.jsonl"

if __name__ == "__main__":
    # Test feedback generation
    test_spec = {
        "type": "table",
        "material": ["unknown_material"],
        "dimensions": {},
        "purpose": None
    }
    
    test_report = {
        "issues": ["material_invalid", "dimensions_missing", "purpose_missing"],
        "severity": "major",
        "quality_scores": {
            "completeness_score": 1,
            "material_realism_score": 0,
            "dimension_validity_score": 0
        }
    }
    
    feedback = generate_feedback("Design a dining table", test_spec, test_report)
    log_feedback(feedback)
    
    print("Test feedback generation:")
    print(f"Feedback: {feedback['feedback_text']}")
    print(f"Actions: {feedback['actions']}")
    print(f"Source: {feedback['source']}")