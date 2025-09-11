"""Automated editor for applying feedback to prompts and improving specifications."""

import re
from typing import Dict, List, Any

def create_augmentation(prompt: str, eval_report: Dict[str, Any]) -> str:
    """Create type-aware prompt augmentation based on evaluation report."""
    
    issues = eval_report.get('issues', [])
    scores = eval_report.get('scores', {})
    spec_type = eval_report.get('type', 'design')
    
    suggestions = []
    
    # Type-specific augmentations
    if spec_type == 'email':
        suggestions.extend(_get_email_suggestions(prompt, issues, scores))
    else:
        suggestions.extend(_get_design_suggestions(prompt, issues, scores))
    
    # Apply augmentations
    if suggestions:
        augmentation = " -- " + "; ".join(suggestions)
        return prompt + augmentation
    
    return prompt

def _get_email_suggestions(prompt: str, issues: List[str], scores: Dict[str, Any]) -> List[str]:
    """Get email-specific suggestions."""
    suggestions = []
    
    # Check for missing recipient
    if any('recipient' in issue.lower() or 'missing' in issue.lower() for issue in issues):
        if '@' not in prompt and 'to ' not in prompt.lower():
            suggestions.append("specify recipient email or team name")
    
    # Check for missing subject
    if any('subject' in issue.lower() for issue in issues):
        if 'about' not in prompt.lower() and 'regarding' not in prompt.lower():
            suggestions.append("include email subject with 'about' or 'regarding'")
    
    # Check for missing date context
    if 'october' in prompt.lower() or 'oct' in prompt.lower():
        if not any(word in prompt.lower() for word in ['launch', 'date', 'schedule']):
            suggestions.append("mention specific launch date 'October 1'")
    
    # Check tone requirements
    if scores.get('tone_score', 0) < 2.0:
        if not any(tone in prompt.lower() for tone in ['formal', 'professional', 'casual', 'friendly']):
            suggestions.append("specify tone (formal, professional, casual, or friendly)")
    
    # Check body content
    if scores.get('body_score', 0) < 2.0:
        suggestions.append("provide more context for email content")
    
    return suggestions

def _get_design_suggestions(prompt: str, issues: List[str], scores: Dict[str, Any]) -> List[str]:
    """Get design-specific suggestions."""
    suggestions = []
    
    # Check completeness
    if scores.get('completeness_score', 0) < 3:
        if not any(dim in prompt.lower() for dim in ['feet', 'cm', 'meter', 'inch', 'size']):
            suggestions.append("specify dimensions with units (e.g., 6 feet, 120 cm)")
        
        if not any(mat in prompt.lower() for mat in ['wood', 'metal', 'glass', 'plastic', 'concrete']):
            suggestions.append("specify material (wood, metal, glass, etc.)")
    
    # Check material realism
    if scores.get('material_realism_score', 0) < 2:
        suggestions.append("use standard materials like wood, steel, or glass")
    
    # Check dimensions
    if scores.get('dimension_validity_score', 0) < 1:
        object_type = 'furniture'
        if 'table' in prompt.lower():
            suggestions.append("add table dimensions (length x width x height)")
        elif 'chair' in prompt.lower():
            suggestions.append("add chair dimensions (seat height, width)")
        elif 'building' in prompt.lower():
            suggestions.append("add building size (floors, area)")
        else:
            suggestions.append("add specific measurements")
    
    # Check type clarity
    if scores.get('type_match_score', 0) < 1:
        suggestions.append("clearly specify the type of object to create")
    
    return suggestions

def apply_feedback_to_prompt(original_prompt: str, feedback: Dict[str, Any]) -> str:
    """Apply feedback to prompt by augmenting it with specific instructions."""
    
    feedback_text = feedback.get('feedback_text', '')
    actions = feedback.get('actions', [])
    
    # Start with original prompt
    enhanced_prompt = original_prompt.strip()
    
    # Apply specific action-based enhancements
    enhancements = []
    
    # Handle dimension-related feedback
    if any(action in actions for action in ['add_dimensions_with_units', 'add_dimension_units', 'add_dimensional_measurements']):
        enhancements.append("specify exact dimensions with units (e.g., 6 feet, 2 meters, 150 cm)")
    
    if 'add_detailed_dimensions' in actions:
        enhancements.append("include length, width, and height measurements")
    
    if 'add_floor_count' in actions:
        enhancements.append("specify number of floors")
    
    # Handle material-related feedback
    if any(action in actions for action in ['add_material_specification', 'use_standard_materials']):
        enhancements.append("use standard materials like wood, metal, glass, concrete, or plastic")
    
    if 'specify_material_grade' in actions:
        enhancements.append("specify material quality or grade")
    
    # Handle type and purpose feedback
    if 'specify_object_type' in actions:
        enhancements.append("clearly state the type of object")
    
    if 'specify_purpose' in actions:
        enhancements.append("describe the intended use or purpose")
    
    # Handle completeness feedback
    if 'improve_completeness' in actions:
        enhancements.append("provide complete specifications including all relevant details")
    
    # Handle sustainable features
    if 'add_sustainable_features' in actions:
        enhancements.append("include eco-friendly or energy-efficient features")
    
    # Handle furniture-specific feedback
    if 'add_furniture_dimensions' in actions:
        if 'table' in original_prompt.lower():
            enhancements.append("specify table dimensions (length x width x height)")
        elif 'chair' in original_prompt.lower():
            enhancements.append("specify chair dimensions (seat height, width, depth)")
        else:
            enhancements.append("specify furniture dimensions")
    
    # Handle building-specific feedback
    if 'reduce_floor_count' in actions:
        enhancements.append("limit to reasonable floor count (1-10 floors)")
    
    if 'consider_area_subdivision' in actions:
        enhancements.append("consider breaking large areas into sections")
    
    # Apply text-based enhancements from feedback
    if 'add units' in feedback_text.lower() or 'units' in feedback_text.lower():
        if not any('unit' in enh for enh in enhancements):
            enhancements.append("include measurement units (meters, feet, cm)")
    
    if 'material' in feedback_text.lower() and 'grade' in feedback_text.lower():
        if not any('grade' in enh for enh in enhancements):
            enhancements.append("specify material grade or quality")
    
    if 'floor' in feedback_text.lower() and 'count' in feedback_text.lower():
        if not any('floor' in enh for enh in enhancements):
            enhancements.append("specify number of floors")
    
    # Combine enhancements
    if enhancements:
        # Remove duplicates while preserving order
        unique_enhancements = []
        for enh in enhancements:
            if enh not in unique_enhancements:
                unique_enhancements.append(enh)
        
        enhancement_text = " -- " + "; ".join(unique_enhancements)
        enhanced_prompt = original_prompt + enhancement_text
    
    return enhanced_prompt

def apply_direct_spec_edits(spec: Dict[str, Any], feedback: Dict[str, Any]) -> Dict[str, Any]:
    """Apply direct edits to spec based on feedback (alternative to prompt augmentation)."""
    
    edited_spec = spec.copy()
    actions = feedback.get('actions', [])
    
    # Add default dimensions if missing
    if any(action in actions for action in ['add_dimensions_with_units', 'add_dimensional_measurements']):
        if not edited_spec.get('dimensions') or not edited_spec['dimensions'].get('raw'):
            spec_type = edited_spec.get('type', '').lower()
            
            if spec_type == 'table':
                edited_spec['dimensions'] = {'raw': '6x4 feet', 'length_ft': 6, 'width_ft': 4}
            elif spec_type == 'chair':
                edited_spec['dimensions'] = {'raw': '18 inches seat height', 'seat_height_in': 18}
            elif spec_type == 'building':
                floors = edited_spec.get('dimensions', {}).get('floors', 1)
                edited_spec['dimensions'] = {'raw': f'{floors}-floor', 'floors': floors}
            else:
                edited_spec['dimensions'] = {'raw': 'standard size'}
    
    # Fix material issues
    if 'use_standard_materials' in actions:
        current_material = edited_spec.get('material', [])
        if isinstance(current_material, str):
            current_material = [current_material]
        
        # Replace unknown materials with reasonable defaults
        known_materials = ['wood', 'metal', 'glass', 'plastic', 'concrete', 'fabric', 'leather']
        fixed_materials = []
        
        for mat in current_material:
            if any(known in mat.lower() for known in known_materials):
                fixed_materials.append(mat)
            else:
                # Default material based on type
                spec_type = edited_spec.get('type', '').lower()
                if spec_type in ['table', 'chair', 'cabinet']:
                    fixed_materials.append('wood')
                elif spec_type == 'building':
                    fixed_materials.append('concrete')
                else:
                    fixed_materials.append('metal')
        
        if fixed_materials:
            edited_spec['material'] = fixed_materials
    
    # Add purpose if missing
    if 'specify_purpose' in actions and not edited_spec.get('purpose'):
        spec_type = edited_spec.get('type', '').lower()
        
        if spec_type == 'table':
            edited_spec['purpose'] = 'dining'
        elif spec_type == 'chair':
            edited_spec['purpose'] = 'seating'
        elif spec_type == 'building':
            edited_spec['purpose'] = 'commercial'
        elif spec_type == 'cabinet':
            edited_spec['purpose'] = 'storage'
        else:
            edited_spec['purpose'] = 'general'
    
    return edited_spec

def generate_improvement_suggestions(original_spec: Dict[str, Any], improved_spec: Dict[str, Any]) -> List[str]:
    """Generate list of improvements made between original and improved spec."""
    
    suggestions = []
    
    # Check dimensions improvements
    orig_dims = original_spec.get('dimensions', {})
    impr_dims = improved_spec.get('dimensions', {})
    
    if not orig_dims.get('raw') and impr_dims.get('raw'):
        suggestions.append("Added dimensional specifications")
    
    # Check material improvements
    orig_mat = original_spec.get('material', [])
    impr_mat = improved_spec.get('material', [])
    
    if len(impr_mat) > len(orig_mat):
        suggestions.append("Enhanced material specifications")
    
    # Check purpose improvements
    if not original_spec.get('purpose') and improved_spec.get('purpose'):
        suggestions.append("Added purpose specification")
    
    # Check type improvements
    if not original_spec.get('type') and improved_spec.get('type'):
        suggestions.append("Added type specification")
    
    return suggestions

if __name__ == "__main__":
    # Test type-aware augmentation
    test_email_prompt = "Write email to team about launch"
    test_email_report = {
        "issues": ["Missing subject", "Missing date"],
        "scores": {"subject_score": 0, "body_score": 1.5},
        "type": "email"
    }
    
    augmented_email = create_augmentation(test_email_prompt, test_email_report)
    print("Email augmentation:")
    print(f"Original: {test_email_prompt}")
    print(f"Augmented: {augmented_email}")
    
    # Test design augmentation
    test_design_prompt = "Create a table"
    test_design_report = {
        "issues": ["Missing dimensions"],
        "scores": {"completeness_score": 2, "dimension_validity_score": 0},
        "type": "design"
    }
    
    augmented_design = create_augmentation(test_design_prompt, test_design_report)
    print("\nDesign augmentation:")
    print(f"Original: {test_design_prompt}")
    print(f"Augmented: {augmented_design}")