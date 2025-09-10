import json
import os
import argparse
from datetime import datetime
from src.extractor import extract_basic_fields
from src.schema import validate_and_save
from evaluator_agent import evaluate_spec
from data_scorer import score_spec, create_dashboard
from utils import apply_fallbacks

def compute_reward(evaluator_result, spec_score=None):
    """Compute reward based on evaluator result and optional spec score."""
    severity = evaluator_result.get('severity', 'major')
    issues = evaluator_result.get('issues', [])
    
    # Base reward calculation
    if not issues:
        base_reward = 1.0
    elif severity == 'minor':
        base_reward = 0.2
    else:  # major
        base_reward = -1.0
    
    # Scale with spec_score if available
    if spec_score is not None:
        reward = base_reward * (spec_score / 10.0)
    else:
        reward = base_reward
    
    return {
        "reward": reward,
        "base_reward": base_reward,
        "spec_score": spec_score
    }

def rl_iteration(prompt):
    """Run one RL iteration: generate spec, evaluate, compute reward, log."""
    # Generate spec using extractor
    extracted_fields = extract_basic_fields(prompt)
    
    # Apply unified fallback values
    fallback_data = apply_fallbacks(extracted_fields)
    
    # Save spec
    timestamp = datetime.now().isoformat().replace(':', '-').split('.')[0]
    spec_filename = f"rl_spec_{timestamp}.json"
    spec = validate_and_save(fallback_data, spec_filename)
    spec_path = f"spec_outputs/{spec_filename}"
    
    # Evaluate spec
    evaluator_result = evaluate_spec(prompt, spec.dict())
    
    # Score spec
    score_result = score_spec(spec.dict(), prompt)
    spec_score = score_result['format_score']
    
    # Compute reward with spec score
    reward_result = compute_reward(evaluator_result, spec_score)
    
    # Create dashboard
    dashboard = create_dashboard(prompt, spec.dict(), evaluator_result, reward_result.get('reward'))
    
    # Log to RL history
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "spec_path": spec_path,
        "critic_issues": evaluator_result.get('issues', []),
        "spec_score": spec_score,
        "reward": reward_result.get('reward'),
        "dashboard": dashboard,
        "notes": "auto"
    }
    
    # Save to RL logs
    os.makedirs("rl_logs", exist_ok=True)
    rl_history_path = "rl_logs/rl_history.json"
    
    if os.path.exists(rl_history_path):
        with open(rl_history_path, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    history.append(log_entry)
    
    with open(rl_history_path, 'w') as f:
        json.dump(history, f, indent=2)
    
    return log_entry

def main():
    parser = argparse.ArgumentParser(description='Run RL loop iterations')
    parser.add_argument('--prompts', help='Path to prompts file')
    parser.add_argument('--runs', type=int, default=5, help='Number of runs')
    
    args = parser.parse_args()
    
    # Default test prompts if no file provided
    test_prompts = [
        "Create a wooden dining table",
        "Design a metal office chair",
        "Make a glass coffee table",
        "Build a storage cabinet",
        "Design an eco-friendly bookshelf"
    ]
    
    if args.prompts and os.path.exists(args.prompts):
        with open(args.prompts, 'r') as f:
            test_prompts = [line.strip() for line in f if line.strip()]
    
    print(f"Running {args.runs} RL iterations...")
    
    for i in range(min(args.runs, len(test_prompts))):
        prompt = test_prompts[i]
        print(f"\nIteration {i+1}: {prompt}")
        
        result = rl_iteration(prompt)
        print(f"Spec Score: {result['spec_score']}")
        print(f"Reward: {result['reward']}")
        print(f"Issues: {result['critic_issues']}")
        print(f"Dashboard: {result['dashboard']['critic'][:50]}...")
    
    print(f"\nCompleted {args.runs} iterations. Check rl_logs/rl_history.json")

if __name__ == "__main__":
    main()