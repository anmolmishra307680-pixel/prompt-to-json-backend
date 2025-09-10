"""Report generation for design specification evaluation."""

import json
import os
import re
from datetime import datetime
from typing import Dict, Any, List

try:
    from .criteria import (
        check_type_presence,
        check_material_validity,
        check_dimensions_validity,
        check_purpose_consistency,
        check_eco_requirements,
        check_type_specific_requirements,
        generate_recommendations
    )
except ImportError:
    from criteria import (
        check_type_presence,
        check_material_validity,
        check_dimensions_validity,
        check_purpose_consistency,
        check_eco_requirements,
        check_type_specific_requirements,
        generate_recommendations
    )

# Import data scorer
try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from data_scorer import score_spec
except ImportError:
    def score_spec(spec, prompt=""):
        return {"format_score": 5.0, "explanations": ["scorer unavailable"]}

def create_slug(text: str) -> str:
    """Create URL-friendly slug from text."""
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '_', slug)
    return slug[:30]

def evaluate_spec(prompt: str, spec: dict, spec_path: str = "") -> dict:
    """Comprehensive evaluation of design specification."""
    
    issues = []
    critic_parts = []
    
    # Run all validation checks
    checks = [
        check_type_presence(spec),
        check_material_validity(spec),
        check_dimensions_validity(spec),
        check_purpose_consistency(spec, prompt),
        check_eco_requirements(spec, prompt),
        check_type_specific_requirements(spec)
    ]
    
    # Collect issues and feedback
    for i, (is_valid, message) in enumerate(checks):
        if not is_valid and message:
            issue_types = [
                "type_missing",
                "material_invalid", 
                "dimensions_invalid",
                "purpose_missing",
                "energy_source_missing",
                "type_requirements_missing"
            ]
            
            if i < len(issue_types):
                issues.append(issue_types[i])
            
            critic_parts.append(message)
    
    # Determine severity
    if len(issues) >= 3:
        severity = "major"
    elif len(issues) >= 1:
        severity = "minor"
    else:
        severity = "none"
    
    # Generate human-style feedback
    if not critic_parts:
        critic_feedback = "Specification looks complete and well-defined."
    else:
        critic_feedback = ". ".join(critic_parts) + "."
    
    # Generate recommendations
    recommendations = generate_recommendations(issues, spec, prompt)
    
    # Get quality scores from data scorer
    quality_scores = score_spec(spec, prompt)
    
    # Create comprehensive report
    report = {
        "prompt": prompt,
        "spec_path": spec_path,
        "timestamp": datetime.now().isoformat(),
        "critic_feedback": critic_feedback,
        "issues": issues,
        "severity": severity,
        "recommendations": recommendations,
        "quality_scores": quality_scores,
        "spec_summary": {
            "type": spec.get('type', 'unspecified'),
            "material_count": len(spec.get('material', [])) if isinstance(spec.get('material'), list) else (1 if spec.get('material') else 0),
            "has_dimensions": bool(spec.get('dimensions')),
            "has_purpose": bool(spec.get('purpose')),
            "completeness_score": calculate_completeness_score(spec)
        }
    }
    
    return report

def calculate_completeness_score(spec: dict) -> float:
    """Calculate completeness score (0-10) based on filled fields."""
    required_fields = ['type', 'material', 'color', 'dimensions', 'purpose']
    score = 0
    
    for field in required_fields:
        value = spec.get(field)
        if value and value not in ['unspecified', 'default', 'none', '', None]:
            if field == 'material' and isinstance(value, list) and len(value) > 0:
                score += 2
            elif field == 'dimensions' and isinstance(value, dict):
                if value.get('floors') or value.get('area_m2') or value.get('raw'):
                    score += 2
            else:
                score += 2
    
    return min(score, 10.0)

def save_report(report: dict, output_dir: str = "evaluations") -> tuple:
    """Save report as both JSON and human-readable text."""
    
    # Create directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = create_slug(report['prompt'])
    
    json_filename = f"{slug}_{timestamp}.json"
    txt_filename = f"{slug}_{timestamp}.txt"
    
    json_path = os.path.join(output_dir, json_filename)
    txt_path = os.path.join("reports", txt_filename)
    
    # Save JSON report
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Generate and save human-readable report
    human_report = generate_human_report(report)
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(human_report)
    
    return json_path, txt_path

def generate_human_report(report: dict) -> str:
    """Generate human-readable text report."""
    
    lines = []
    lines.append("=" * 60)
    lines.append("DESIGN SPECIFICATION EVALUATION REPORT")
    lines.append("=" * 60)
    lines.append("")
    
    # Header information
    lines.append(f"Evaluation Date: {report['timestamp']}")
    lines.append(f"Prompt: {report['prompt']}")
    lines.append(f"Spec Path: {report.get('spec_path', 'N/A')}")
    lines.append("")
    
    # Summary
    summary = report.get('spec_summary', {})
    lines.append("SPECIFICATION SUMMARY")
    lines.append("-" * 30)
    lines.append(f"Type: {summary.get('type', 'N/A')}")
    lines.append(f"Materials: {summary.get('material_count', 0)} specified")
    lines.append(f"Has Dimensions: {'Yes' if summary.get('has_dimensions') else 'No'}")
    lines.append(f"Has Purpose: {'Yes' if summary.get('has_purpose') else 'No'}")
    lines.append(f"Completeness Score: {summary.get('completeness_score', 0)}/10")
    lines.append("")
    
    # Quality Scores
    quality_scores = report.get('quality_scores', {})
    if quality_scores:
        lines.append("QUALITY SCORES")
        lines.append("-" * 30)
        lines.append(f"Overall Format Score: {quality_scores.get('format_score', 0)}/10")
        lines.append(f"Completeness: {quality_scores.get('completeness_score', 0)}/4")
        lines.append(f"Material Realism: {quality_scores.get('material_realism_score', 0)}/3")
        lines.append(f"Dimension Validity: {quality_scores.get('dimension_validity_score', 0)}/2")
        lines.append(f"Type Match: {quality_scores.get('type_match_score', 0)}/1")
        lines.append("")
    
    # Evaluation Results
    lines.append("EVALUATION RESULTS")
    lines.append("-" * 30)
    lines.append(f"Overall Severity: {report['severity'].upper()}")
    lines.append(f"Issues Found: {len(report['issues'])}")
    lines.append("")
    
    # Critic Feedback
    lines.append("CRITIC FEEDBACK")
    lines.append("-" * 30)
    lines.append(report['critic_feedback'])
    lines.append("")
    
    # Issues Detail
    if report['issues']:
        lines.append("ISSUES IDENTIFIED")
        lines.append("-" * 30)
        for i, issue in enumerate(report['issues'], 1):
            lines.append(f"{i}. {issue.replace('_', ' ').title()}")
        lines.append("")
    
    # Recommendations
    if report['recommendations']:
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 30)
        for i, rec in enumerate(report['recommendations'], 1):
            lines.append(f"{i}. {rec}")
        lines.append("")
    
    # Quality Explanations
    quality_scores = report.get('quality_scores', {})
    if quality_scores.get('explanations'):
        lines.append("QUALITY ANALYSIS")
        lines.append("-" * 30)
        for i, explanation in enumerate(quality_scores['explanations'], 1):
            lines.append(f"{i}. {explanation}")
        lines.append("")
    
    # Footer
    lines.append("=" * 60)
    lines.append("End of Report")
    lines.append("=" * 60)
    
    return "\n".join(lines)

def run_evaluation_demo():
    """Run evaluation on sample specs."""
    
    # Sample specs for testing
    test_specs = [
        {
            "prompt": "Design a wooden dining table",
            "spec": {
                "type": "table",
                "material": ["wood"],
                "color": "brown",
                "dimensions": {"raw": "6x4 feet"},
                "purpose": "dining"
            }
        },
        {
            "prompt": "Create a steel office chair with wheels",
            "spec": {
                "type": "chair", 
                "material": ["metal"],
                "color": "black",
                "purpose": "office"
            }
        },
        {
            "prompt": "Build a 3-floor eco-friendly library",
            "spec": {
                "type": "building",
                "material": ["concrete", "glass"],
                "dimensions": {"floors": 3, "raw": "3-floor"},
                "purpose": "library"
            }
        }
    ]
    
    print("=== Evaluator Demo ===")
    
    for i, test in enumerate(test_specs, 1):
        print(f"\nEvaluating spec {i}: {test['prompt']}")
        
        # Run evaluation
        report = evaluate_spec(test['prompt'], test['spec'])
        
        # Save reports
        json_path, txt_path = save_report(report)
        
        print(f"Severity: {report['severity']}")
        print(f"Issues: {len(report['issues'])}")
        print(f"JSON saved: {json_path}")
        print(f"TXT saved: {txt_path}")

if __name__ == "__main__":
    run_evaluation_demo()