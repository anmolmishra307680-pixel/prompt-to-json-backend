import json
import os
from datetime import datetime
from src.extractor import extract_basic_fields
from src.schema import validate_and_save
from evaluator_agent import evaluate_spec
from data_scorer import score_spec, create_dashboard
from rl_loop import compute_reward
from utils import apply_fallbacks

def run_full_pipeline(prompt, output_name):
    """Run complete pipeline: extract -> validate -> evaluate -> score -> reward."""
    print(f"\n=== Running pipeline for: {prompt} ===")
    
    # Step 1: Extract fields
    extracted = extract_basic_fields(prompt)
    print(f"1. Extracted: {extracted}")
    
    # Step 2: Apply fallbacks and validate
    fallback_data = apply_fallbacks(extracted)
    
    spec_filename = f"{output_name}_spec.json"
    spec = validate_and_save(fallback_data, spec_filename)
    print(f"2. Spec saved: {spec_filename}")
    
    # Step 3: Evaluate
    evaluation = evaluate_spec(prompt, spec.dict())
    print(f"3. Evaluation: {evaluation['severity']} - {len(evaluation['issues'])} issues")
    
    # Step 4: Score
    score_result = score_spec(spec.dict(), prompt)
    print(f"4. Score: {score_result['format_score']}/10")
    
    # Step 5: Compute reward
    reward_result = compute_reward(evaluation, score_result['format_score'])
    print(f"5. Reward: {reward_result['reward']}")
    
    # Create full result
    full_result = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "extracted_fields": extracted,
        "spec": spec.dict(),
        "spec_path": f"spec_outputs/{spec_filename}",
        "evaluation": evaluation,
        "scoring": score_result,
        "reward": reward_result['reward'],
        "dashboard": create_dashboard(prompt, spec.dict(), evaluation, reward_result['reward'])
    }
    
    # Save full result
    os.makedirs("sample_outputs", exist_ok=True)
    result_filename = f"sample_outputs/{output_name}_full_pipeline.json"
    with open(result_filename, 'w') as f:
        json.dump(full_result, f, indent=2)
    
    print(f"6. Full result saved: {result_filename}")
    return full_result

if __name__ == "__main__":
    # 5 distinct demo prompts
    demo_prompts = [
        ("Design a 2-floor eco-friendly library with glass and concrete", "architectural"),
        ("Create a lightweight drone body using carbon fiber", "mechanical"),
        ("Build a medieval wooden throne with gold accents", "props"),
        ("Design a modern glass coffee table for living room", "scene"),
        ("Create a stainless steel surgical instrument cabinet", "medical")
    ]
    
    print("Running 5 end-to-end pipeline demonstrations...")
    
    results = []
    for prompt, category in demo_prompts:
        result = run_full_pipeline(prompt, category)
        results.append(result)
    
    # Create summary report
    summary = {
        "total_runs": len(results),
        "timestamp": datetime.now().isoformat(),
        "average_score": sum(r['scoring']['format_score'] for r in results) / len(results),
        "average_reward": sum(r['reward'] for r in results) / len(results),
        "results_summary": [
            {
                "category": demo_prompts[i][1],
                "prompt": r['prompt'][:50] + "...",
                "score": r['scoring']['format_score'],
                "reward": r['reward'],
                "issues_count": len(r['evaluation']['issues'])
            }
            for i, r in enumerate(results)
        ]
    }
    
    with open("sample_outputs/pipeline_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n=== Pipeline Summary ===")
    print(f"Total runs: {summary['total_runs']}")
    print(f"Average score: {summary['average_score']:.1f}/10")
    print(f"Average reward: {summary['average_reward']:.2f}")
    print("Summary saved to sample_outputs/pipeline_summary.json")