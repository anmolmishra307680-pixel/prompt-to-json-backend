"""Simple evaluator for backward compatibility."""

def evaluate_spec(prompt, spec):
    """Evaluate spec against prompt and return critic feedback."""
    issues = []
    critic_parts = []
    
    # Check basic fields
    if not spec.get('type') or spec.get('type') == 'unknown':
        issues.append("type_missing")
        critic_parts.append("Type specification is missing or unclear")
    
    # Check material
    material = spec.get('material', [])
    if not material or material == ['unspecified']:
        issues.append("material_missing")
        critic_parts.append("Material not specified")
    
    # Check dimensions
    dimensions = spec.get('dimensions')
    if not dimensions or not str(dimensions).strip():
        issues.append("dimensions_missing")
        critic_parts.append("Dimensions are missing (provide specific measurements)")
    
    # Determine severity
    severity = "major" if len(issues) >= 3 else "minor" if issues else "none"
    
    # Generate feedback
    if not critic_parts:
        critic_feedback = "Specification looks complete and well-defined."
    else:
        critic_feedback = ". ".join(critic_parts) + "."
    
    return {
        "critic_feedback": critic_feedback,
        "issues": issues,
        "severity": severity
    }