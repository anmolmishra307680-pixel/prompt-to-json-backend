#!/usr/bin/env python3
"""
Main pipeline entrypoint for prompt-to-json agent.
Integrates extraction, generation, and evaluation components.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.extractor import extract_basic_fields
from src.schema import save_valid_spec
from src.logger import log_prompt
from evaluator_agent import evaluate_spec
from utils import apply_fallbacks, save_json

def create_slug(prompt):
    """Create URL-friendly slug from prompt."""
    import re
    slug = re.sub(r'[^\w\s-]', '', prompt.lower())
    slug = re.sub(r'[-\s]+', '_', slug)
    return slug[:30]  # Limit length

def run_pipeline(prompt):
    """Run complete prompt-to-JSON pipeline."""
    print(f"Processing prompt: {prompt}")
    
    # Step 1: Extract basic fields
    print("1. Extracting fields...")
    extracted = extract_basic_fields(prompt)
    print(f"   Extracted: {extracted}")
    
    # Step 2: Apply fallbacks for missing fields
    print("2. Applying fallbacks...")
    spec_data = apply_fallbacks(extracted)
    print(f"   Final spec: {spec_data}")
    
    # Step 3: Validate and save specification
    print("3. Validating and saving spec...")
    spec_path = save_valid_spec(spec_data, prompt=prompt)
    
    if not spec_path:
        print("   [ERROR] Spec validation failed, using fallback save")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = create_slug(prompt)
        spec_filename = f"{slug}_{timestamp}.json"
        spec_path = f"spec_outputs/{spec_filename}"
        os.makedirs("spec_outputs", exist_ok=True)
        save_json(spec_data, spec_path)
    
    print(f"   Saved to: {spec_path}")
    
    # Step 4: Evaluate specification
    print("4. Evaluating spec...")
    evaluation = evaluate_spec(prompt, spec_data)
    print(f"   Evaluation: {evaluation['severity']} - {evaluation['critic_feedback']}")
    
    # Step 5: Save evaluation
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = create_slug(prompt)
    eval_filename = f"eval_{slug}_{timestamp}.json"
    eval_path = f"evaluations/{eval_filename}"
    
    os.makedirs("evaluations", exist_ok=True)
    eval_data = {
        "prompt": prompt,
        "spec_path": spec_path,
        "timestamp": datetime.now().isoformat(),
        **evaluation
    }
    save_json(eval_data, eval_path)
    print(f"5. Saved evaluation to: {eval_path}")
    
    # Summary
    print("\n=== PIPELINE SUMMARY ===")
    print(f"Prompt: {prompt}")
    print(f"Spec: {spec_path}")
    # print(f"Validated: {'Yes' if validated else 'No'}")
    print(f"Evaluation: {evaluation['severity']} severity")
    print(f"Issues: {len(evaluation['issues'])}")
    print(f"Feedback: {evaluation['critic_feedback']}")
    
    # Step 6: Log the complete interaction
    print("6. Logging interaction...")
    log_prompt(
        prompt=prompt,
        spec_path=spec_path,
        evaluation=evaluation,
        validation_passed=spec_path is not None and 'validation_errors' not in str(spec_path),
        issues_count=len(evaluation['issues']),
        severity=evaluation['severity']
    )
    
    return {
        "spec_path": spec_path,
        "eval_path": eval_path,
        "spec_data": spec_data,
        "evaluation": evaluation,
        "validated": spec_path is not None and 'validation_errors' not in str(spec_path)
    }

def main():
    parser = argparse.ArgumentParser(description='Prompt-to-JSON Agent Pipeline')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prompt', help='Design prompt string')
    group.add_argument('--prompt-file', help='File containing design prompt')
    
    args = parser.parse_args()
    
    # Get prompt from argument or file
    if args.prompt:
        prompt = args.prompt
    else:
        with open(args.prompt_file, 'r') as f:
            prompt = f.read().strip()
    
    # Run pipeline
    try:
        result = run_pipeline(prompt)
        print(f"\n[SUCCESS] Pipeline completed successfully!")
        return 0
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())