"""Simple data scorer for backward compatibility."""

def score_spec(spec, prompt=""):
    """Score specification quality (0-10 scale)."""
    score = 0
    explanations = []
    
    # Type score (0-2)
    if spec.get('type') and spec.get('type') != 'unknown':
        score += 2
        explanations.append("Type specified")
    
    # Material score (0-3)
    material = spec.get('material', [])
    if material and material != ['unspecified']:
        score += 3
        explanations.append("Material specified")
    
    # Dimensions score (0-2)
    dimensions = spec.get('dimensions')
    if dimensions and str(dimensions).strip():
        score += 2
        explanations.append("Dimensions provided")
    
    # Purpose score (0-1)
    if spec.get('purpose') and spec.get('purpose') != 'general':
        score += 1
        explanations.append("Purpose specified")
    
    # Color bonus (0-2)
    if spec.get('color') and spec.get('color') != 'default':
        score += 2
        explanations.append("Color specified")
    
    return {
        "format_score": min(score, 10),
        "completeness_score": min(score // 2.5, 4),
        "material_realism_score": 3 if material and material != ['unspecified'] else 0,
        "dimension_validity_score": 2 if dimensions else 0,
        "type_match_score": 1 if spec.get('type') != 'unknown' else 0,
        "explanations": explanations
    }