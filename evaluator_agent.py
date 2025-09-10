import json
import os
import argparse
import hashlib
from datetime import datetime

# Known materials list (supports multi-material specs)
KNOWN_MATERIALS = ["steel", "aluminum", "wood", "concrete", "glass", "carbon fiber", "plastic", "metal", "fabric", "leather", "stainless steel", "oak", "pine"]

def load_spec(path):
    """Read JSON spec from file."""
    with open(path, 'r') as f:
        return json.load(f)

def evaluate_spec(prompt, spec):
    """Evaluate spec against prompt and return critic feedback."""
    issues = []
    critic_parts = []
    
    # Check if type is present
    if not spec.get('type') or spec.get('type') == 'unknown':
        issues.append("type_missing")
        critic_parts.append("Type specification is missing or unclear")
    
    # Check material (handle both string and list formats)
    material = spec.get('material', '')
    if isinstance(material, list):
        material_str = ', '.join(material).lower()
        material_list = [m.lower() for m in material]
    else:
        material_str = str(material).lower()
        material_list = [material_str]
    
    if not material_str or material_str in ['unspecified', 'default']:
        issues.append("material_missing")
        critic_parts.append("Material not specified")
    elif not any(known.lower() in mat for mat in material_list for known in KNOWN_MATERIALS):
        issues.append("material_unrecognized")
        critic_parts.append(f"Material '{material_str}' not recognized")
    
    # Check dimensions (handle both string and dict formats)
    dimensions = spec.get('dimensions', '')
    if isinstance(dimensions, dict):
        dim_str = str(dimensions.get('raw', ''))
    else:
        dim_str = str(dimensions)
    
    if not dim_str or dim_str in ['standard', 'default', 'None']:
        issues.append("dimensions_missing")
        critic_parts.append("Dimensions are missing (provide specific measurements)")
    elif dim_str != 'None' and not any(unit in dim_str.lower() for unit in ['feet', 'ft', 'cm', 'm', 'inches', 'in', 'floor']):
        issues.append("dimensions_unparseable")
        critic_parts.append("Dimensions format unclear or missing units")
    
    # Check purpose consistency
    purpose = spec.get('purpose', '').lower()
    if not purpose or purpose == 'general':
        issues.append("purpose_missing")
        critic_parts.append("Purpose or intended use not specified")
    
    # Check for eco-friendly requirements in prompt
    if 'eco' in prompt.lower() or 'green' in prompt.lower() or 'sustainable' in prompt.lower():
        if 'energy' not in str(spec).lower() and 'sustainable' not in str(spec).lower():
            issues.append("energy_source_missing")
            critic_parts.append("No mention of energy efficiency or sustainable features")
    
    # Determine severity
    severity = "major" if len(issues) >= 3 else "minor" if issues else "none"
    
    # Generate human-style feedback
    if not critic_parts:
        critic_feedback = "Specification looks complete and well-defined."
    else:
        critic_feedback = ". ".join(critic_parts) + "."
    
    return {
        "critic_feedback": critic_feedback,
        "issues": issues,
        "severity": severity
    }

def save_evaluation(prompt, spec_path, evaluation):
    """Save evaluation to evaluations/ folder."""
    os.makedirs("evaluations", exist_ok=True)
    
    timestamp = datetime.now().isoformat()
    hash_obj = hashlib.md5(f"{prompt}{spec_path}".encode())
    filename = f"{timestamp.replace(':', '-').split('.')[0]}_{hash_obj.hexdigest()[:8]}.json"
    
    output = {
        "prompt": prompt,
        "spec_path": spec_path,
        "timestamp": timestamp,
        **evaluation
    }
    
    with open(f"evaluations/{filename}", 'w') as f:
        json.dump(output, f, indent=2)
    
    return filename

def main():
    parser = argparse.ArgumentParser(description='Evaluate furniture design specifications')
    parser.add_argument('--prompt', required=True, help='Original design prompt')
    parser.add_argument('--spec', required=True, help='Path to JSON spec file')
    
    args = parser.parse_args()
    
    # Load and evaluate spec
    spec = load_spec(args.spec)
    evaluation = evaluate_spec(args.prompt, spec)
    
    # Save evaluation
    filename = save_evaluation(args.prompt, args.spec, evaluation)
    
    print(f"Evaluation saved to evaluations/{filename}")
    print(f"Feedback: {evaluation['critic_feedback']}")
    print(f"Issues: {evaluation['issues']}")
    print(f"Severity: {evaluation['severity']}")

if __name__ == "__main__":
    main()