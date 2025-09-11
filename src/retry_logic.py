"""Retry logic with editor-guided improvements."""

import json
import os
from datetime import datetime
from typing import Dict, Any, Tuple
from .agent.editor import create_augmentation
from .generators import DesignGenerator, EmailGenerator
from .evaluators.evaluation_runner import run_evaluation
from .data_scorer import score_spec
from .schema_registry import validate_spec, save_valid_spec

def should_retry(scores: Dict[str, Any], validation: Dict[str, Any]) -> bool:
    """Determine if retry is needed based on scores and validation."""
    
    # Always retry if validation failed
    if not validation.get('valid', True):
        return True
    
    # Retry if format score is low
    format_score = scores.get('format_score', 0)
    if format_score < 6.0:
        return True
    
    # Retry if completeness is very low
    completeness = scores.get('completeness_score', 0)
    if completeness < 2:
        return True
    
    return False

def run_with_retry(prompt: str, spec_type: str, max_retries: int = 1) -> Dict[str, Any]:
    """Run generation with retry logic and improvement tracking."""
    
    results = {
        'attempts': [],
        'final_result': None,
        'improved': False
    }
    
    current_prompt = prompt
    
    for attempt in range(max_retries + 1):
        print(f"Attempt {attempt + 1}: {current_prompt}")
        
        # Generate specification
        if spec_type == 'email':
            generator = EmailGenerator()
        else:
            generator = DesignGenerator()
        
        gen_result = generator.generate_spec(current_prompt)
        spec = gen_result['spec']
        
        # Validate specification
        validation = validate_spec(spec, spec_type)
        
        # Save spec
        if validation['valid']:
            spec_path = save_valid_spec(spec, spec_type)
        else:
            spec_path = f"invalid_{spec_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Calculate scores
        scores = score_spec(spec, current_prompt, spec_type)
        
        # Run evaluation
        eval_path = run_evaluation(current_prompt, spec, spec_path, spec_type)
        
        # Load evaluation report
        with open(eval_path, 'r') as f:
            eval_report = json.load(f)
        
        # Store attempt result
        attempt_result = {
            'attempt': attempt + 1,
            'prompt': current_prompt,
            'spec': spec,
            'validation': validation,
            'scores': scores,
            'eval_report': eval_report,
            'spec_path': spec_path,
            'eval_path': eval_path
        }
        results['attempts'].append(attempt_result)
        
        # Check if retry is needed
        if attempt < max_retries and should_retry(scores, validation):
            # Create augmented prompt for retry
            eval_report_with_type = {**eval_report, 'type': spec_type}
            augmented_prompt = create_augmentation(current_prompt, eval_report_with_type)
            
            if augmented_prompt != current_prompt:
                current_prompt = augmented_prompt
                results['improved'] = True
                print(f"Retrying with improved prompt: {current_prompt}")
            else:
                print("No improvements suggested, stopping retries")
                break
        else:
            print(f"Stopping after attempt {attempt + 1}")
            break
    
    results['final_result'] = results['attempts'][-1]
    return results

def save_before_after_comparison(results: Dict[str, Any], output_dir: str = "sample_outputs") -> str:
    """Save before/after comparison for analysis."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    if len(results['attempts']) < 2:
        return None
    
    before = results['attempts'][0]
    after = results['attempts'][-1]
    
    comparison = {
        "improved": results['improved'],
        "timestamp": datetime.now().isoformat(),
        "before": {
            "prompt": before['prompt'],
            "spec": before['spec'],
            "scores": before['scores'],
            "validation_valid": before['validation']['valid'],
            "format_score": before['scores'].get('format_score', 0)
        },
        "after": {
            "prompt": after['prompt'],
            "spec": after['spec'],
            "scores": after['scores'],
            "validation_valid": after['validation']['valid'],
            "format_score": after['scores'].get('format_score', 0)
        },
        "improvements": {
            "format_score_delta": after['scores'].get('format_score', 0) - before['scores'].get('format_score', 0),
            "validation_improved": after['validation']['valid'] and not before['validation']['valid'],
            "prompt_augmented": before['prompt'] != after['prompt']
        }
    }
    
    # Generate filename
    spec_type = after['spec'].get('type', 'unknown')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"before_after_{spec_type}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save comparison
    with open(filepath, 'w') as f:
        json.dump(comparison, f, indent=2)
    
    return filepath

if __name__ == "__main__":
    # Test retry logic with email
    test_email_prompt = "Write email to team about launch"
    results = run_with_retry(test_email_prompt, 'email', max_retries=1)
    
    print(f"\nEmail retry results:")
    print(f"Attempts: {len(results['attempts'])}")
    print(f"Improved: {results['improved']}")
    
    if len(results['attempts']) > 1:
        before_score = results['attempts'][0]['scores'].get('format_score', 0)
        after_score = results['attempts'][-1]['scores'].get('format_score', 0)
        print(f"Score improvement: {before_score:.1f} -> {after_score:.1f}")
        
        # Save comparison
        comparison_path = save_before_after_comparison(results)
        if comparison_path:
            print(f"Comparison saved to: {comparison_path}")