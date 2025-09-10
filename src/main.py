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

try:
    from src.extractor import extract_basic_fields
    from src.schema import save_valid_spec
    from src.logger import log_prompt
    from evaluator_agent import evaluate_spec
    from utils import apply_fallbacks, save_json
    from data_scorer import score_spec
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def create_slug(prompt):
    """Create URL-friendly slug from prompt."""
    import re
    slug = re.sub(r'[^\w\s-]', '', prompt.lower())
    slug = re.sub(r'[-\s]+', '_', slug)
    return slug[:30]  # Limit length

def run_pipeline(prompt, save_report=False, run_rl=False):
    """Run complete prompt-to-JSON pipeline."""
    try:
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
        
        # Step 5: Score specification
        print("5. Scoring spec...")
        scores = score_spec(spec_data)
        print(f"   Quality score: {scores['format_score']}/10")
        
        # Step 6: Save evaluation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = create_slug(prompt)
        eval_filename = f"eval_{slug}_{timestamp}.json"
        eval_path = f"evaluations/{eval_filename}"
        
        os.makedirs("evaluations", exist_ok=True)
        eval_data = {
            "prompt": prompt,
            "spec_path": spec_path,
            "timestamp": datetime.now().isoformat(),
            "scores": scores,
            **evaluation
        }
        save_json(eval_data, eval_path)
        print(f"6. Saved evaluation to: {eval_path}")
        
        # Step 7: Optional report generation
        if save_report:
            try:
                from src.evaluator.report import save_report as save_eval_report
                report_data = {
                    "prompt": prompt,
                    "spec_path": spec_path,
                    "timestamp": datetime.now().isoformat(),
                    "critic_feedback": evaluation['critic_feedback'],
                    "issues": evaluation['issues'],
                    "severity": evaluation['severity'],
                    "quality_scores": scores,
                    "recommendations": [],
                    "spec_summary": {
                        "type": spec_data.get('type', 'unspecified'),
                        "material_count": len(spec_data.get('material', [])) if isinstance(spec_data.get('material'), list) else (1 if spec_data.get('material') else 0),
                        "has_dimensions": bool(spec_data.get('dimensions')),
                        "has_purpose": bool(spec_data.get('purpose')),
                        "completeness_score": scores.get('completeness_score', 0) * 2.5  # Scale to 0-10
                    }
                }
                json_path, txt_path = save_eval_report(report_data)
                print(f"7. Saved report to: {txt_path}")
            except ImportError:
                print("7. Report generation not available")
        
        # Step 8: Optional RL loop
        reward = 0.0
        if run_rl:
            try:
                from src.rl.rl_loop import compute_reward
                reward = compute_reward(evaluation, scores)
                print(f"8. RL reward: {reward:.3f}")
            except ImportError:
                print("8. RL loop not available")
        
        # Summary
        print("\n=== PIPELINE SUMMARY ===")
        print(f"Prompt: {prompt}")
        print(f"Spec: {spec_path}")
        print(f"Evaluation: {evaluation['severity']} severity")
        print(f"Issues: {len(evaluation['issues'])}")
        print(f"Quality Score: {scores['format_score']}/10")
        if run_rl:
            print(f"Reward: {reward:.3f}")
        print(f"Feedback: {evaluation['critic_feedback']}")
        
        # Step 9: Log the complete interaction
        print(f"{'9' if not save_report else '8'}. Logging interaction...")
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
            "scores": scores,
            "reward": reward,
            "validated": spec_path is not None and 'validation_errors' not in str(spec_path)
        }
    
    except Exception as e:
        print(f"Error in pipeline: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Prompt-to-JSON Agent Pipeline')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prompt', help='Design prompt string')
    group.add_argument('--prompt-file', help='File containing design prompt')
    
    parser.add_argument('--save-report', action='store_true', help='Generate and save evaluation report')
    parser.add_argument('--run-rl', action='store_true', help='Run RL reward computation')
    
    args = parser.parse_args()
    
    # Get prompt from argument or file
    try:
        if args.prompt:
            prompt = args.prompt
        else:
            if not os.path.exists(args.prompt_file):
                print(f"Error: Prompt file '{args.prompt_file}' not found")
                return 1
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
                if not prompt:
                    print("Error: Prompt file is empty")
                    return 1
    except Exception as e:
        print(f"Error reading prompt: {e}")
        return 1
    
    # Run pipeline
    try:
        result = run_pipeline(prompt, save_report=args.save_report, run_rl=args.run_rl)
        print(f"\n[SUCCESS] Pipeline completed successfully!")
        return 0
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Pipeline cancelled by user")
        return 1
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] JSON parsing failed: {e}")
        return 1
    except FileNotFoundError as e:
        print(f"\n[ERROR] File not found: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())