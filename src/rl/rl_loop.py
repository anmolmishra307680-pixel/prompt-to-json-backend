"""Reinforcement Learning loop for design specification generation."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent))

from src.extractor import extract_basic_fields
from src.evaluator.report import evaluate_spec
from data_scorer import score_spec
from src.evaluator.feedback import generate_feedback, log_feedback
from src.agent.editor import apply_feedback_to_prompt, apply_direct_spec_edits, generate_improvement_suggestions
from utils import apply_fallbacks

def compute_reward(report: Dict[str, Any], scores: Dict[str, Any]) -> float:
    """Compute reward based on evaluation report and quality scores."""
    
    severity = report.get('severity', 'major')
    issues_count = len(report.get('issues', []))
    format_score = scores.get('format_score', 0.0)
    
    # Base reward based on severity
    if severity == 'none' and issues_count == 0:
        base_reward = 1.0  # Perfect spec
    elif severity == 'minor':
        base_reward = 0.2  # Minor issues only
    elif severity == 'major':
        base_reward = -1.0  # Major issues
    else:
        base_reward = -0.5  # Unknown severity
    
    # Scale by format score (0-10 scale)
    format_multiplier = format_score / 10.0
    
    # Final reward
    reward = base_reward * format_multiplier
    
    # Bonus for high completeness
    completeness = scores.get('completeness_score', 0)
    if completeness >= 4:
        reward += 0.1
    
    # Penalty for very low scores
    if format_score < 3.0:
        reward -= 0.2
    
    return round(reward, 3)

def rl_iteration(prompt: str, iteration_id: int = 1, reward_threshold: float = 0.2) -> Dict[str, Any]:
    """Run single RL iteration with optional feedback application and retry."""
    
    print(f"RL Iteration {iteration_id}: {prompt}")
    
    # Step 1: Generate spec
    print("  1. Generating spec...")
    extracted_fields = extract_basic_fields(prompt)
    spec = apply_fallbacks(extracted_fields)
    
    # Step 2: Evaluate spec
    print("  2. Evaluating spec...")
    report = evaluate_spec(prompt, spec)
    
    # Step 3: Score spec
    print("  3. Scoring spec...")
    scores = score_spec(spec, prompt)
    
    # Step 4: Compute reward
    print("  4. Computing reward...")
    reward = compute_reward(report, scores)
    
    # Step 5: Generate feedback
    print("  5. Generating feedback...")
    feedback = generate_feedback(prompt, spec, report)
    log_feedback(feedback)
    
    # Store original results
    original_spec = spec.copy()
    original_report = report.copy()
    original_scores = scores.copy()
    original_reward = reward
    
    # Step 6: Apply feedback if reward is below threshold
    retry_attempted = False
    if reward < reward_threshold:
        print(f"  6. Reward {reward:.3f} < {reward_threshold}, applying feedback...")
        
        # Try prompt augmentation approach
        enhanced_prompt = apply_feedback_to_prompt(prompt, feedback)
        print(f"     Enhanced prompt: {enhanced_prompt[:80]}...")
        
        # Regenerate with enhanced prompt
        try:
            enhanced_fields = extract_basic_fields(enhanced_prompt)
            enhanced_spec = apply_fallbacks(enhanced_fields)
            
            # Re-evaluate enhanced spec
            enhanced_report = evaluate_spec(enhanced_prompt, enhanced_spec)
            enhanced_scores = score_spec(enhanced_spec, enhanced_prompt)
            enhanced_reward = compute_reward(enhanced_report, enhanced_scores)
            
            print(f"     Enhanced reward: {enhanced_reward:.3f}")
            
            # Use enhanced results if better
            if enhanced_reward > reward:
                print("     -> Using enhanced spec (improvement achieved)")
                spec = enhanced_spec
                report = enhanced_report
                scores = enhanced_scores
                reward = enhanced_reward
                prompt = enhanced_prompt  # Update prompt for logging
                retry_attempted = True
            else:
                print("     -> No improvement, keeping original spec")
                retry_attempted = True
                
        except Exception as e:
            print(f"     -> Enhancement failed: {e}")
            retry_attempted = True
    
    # Create full trace with retry information
    trace = {
        "iteration_id": iteration_id,
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "spec": spec,
        "extracted_fields": extracted_fields,
        "evaluation": {
            "critic_feedback": report.get('critic_feedback', ''),
            "issues": report.get('issues', []),
            "severity": report.get('severity', 'unknown'),
            "recommendations": report.get('recommendations', [])
        },
        "quality_scores": scores,
        "reward": reward,
        "feedback": {
            "text": feedback.get('feedback_text', ''),
            "actions": feedback.get('actions', []),
            "source": feedback.get('source', 'unknown')
        },
        "retry_info": {
            "attempted": retry_attempted,
            "threshold": reward_threshold,
            "original_reward": original_reward,
            "improvement": reward - original_reward if retry_attempted else 0.0
        }
    }
    
    # Save before/after comparison if retry was attempted
    if retry_attempted:
        save_before_after_comparison({
            "iteration_id": iteration_id,
            "original": {
                "prompt": prompt if not retry_attempted else prompt.split(' -- ')[0],
                "spec": original_spec,
                "evaluation": original_report,
                "scores": original_scores,
                "reward": original_reward
            },
            "enhanced": {
                "prompt": prompt,
                "spec": spec,
                "evaluation": report,
                "scores": scores,
                "reward": reward
            },
            "feedback_applied": feedback,
            "improvement_achieved": reward > original_reward
        })
    
    # Log to RL history
    log_rl_iteration(trace)
    
    print(f"  -> Final Reward: {reward:.3f}, Severity: {report.get('severity')}, Score: {scores.get('format_score')}")
    if retry_attempted:
        improvement = reward - original_reward
        print(f"     Improvement: {improvement:+.3f} ({'SUCCESS' if improvement > 0 else 'NO_CHANGE'})")
    
    return trace

def log_rl_iteration(trace: Dict[str, Any]) -> str:
    """Log RL iteration to rl_history.jsonl."""
    
    os.makedirs("rl_logs", exist_ok=True)
    
    with open("rl_logs/rl_history.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(trace, ensure_ascii=False) + "\n")
    
    return "rl_logs/rl_history.jsonl"

def run_rl_experiment(prompts: List[str], iterations_per_prompt: int = 2) -> List[Dict[str, Any]]:
    """Run RL experiment on multiple prompts."""
    
    print("=== RL Experiment Starting ===")
    
    all_traces = []
    iteration_counter = 1
    
    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        
        for i in range(iterations_per_prompt):
            trace = rl_iteration(prompt, iteration_counter)
            all_traces.append(trace)
            iteration_counter += 1
    
    # Summary statistics
    rewards = [trace['reward'] for trace in all_traces]
    avg_reward = sum(rewards) / len(rewards) if rewards else 0
    
    print(f"\n=== RL Experiment Complete ===")
    print(f"Total iterations: {len(all_traces)}")
    print(f"Average reward: {avg_reward:.3f}")
    print(f"Reward range: {min(rewards):.3f} to {max(rewards):.3f}")
    
    # Generate improvement report
    generate_feedback_attempts_report(all_traces)
    
    return all_traces

def analyze_rl_history() -> Dict[str, Any]:
    """Analyze RL history and provide insights."""
    
    history_file = "rl_logs/rl_history.jsonl"
    
    if not os.path.exists(history_file):
        return {"error": "No RL history found"}
    
    traces = []
    with open(history_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                traces.append(json.loads(line))
    
    if not traces:
        return {"error": "No traces in history"}
    
    # Calculate statistics
    rewards = [trace['reward'] for trace in traces]
    severities = [trace['evaluation']['severity'] for trace in traces]
    format_scores = [trace['quality_scores']['format_score'] for trace in traces]
    
    analysis = {
        "total_iterations": len(traces),
        "reward_stats": {
            "mean": sum(rewards) / len(rewards),
            "min": min(rewards),
            "max": max(rewards),
            "positive_count": sum(1 for r in rewards if r > 0)
        },
        "severity_distribution": {
            "none": severities.count('none'),
            "minor": severities.count('minor'),
            "major": severities.count('major')
        },
        "format_score_stats": {
            "mean": sum(format_scores) / len(format_scores),
            "min": min(format_scores),
            "max": max(format_scores)
        },
        "latest_timestamp": traces[-1]['timestamp']
    }
    
    return analysis

def save_before_after_comparison(comparison: Dict[str, Any]) -> str:
    """Save before/after comparison to sample_outputs."""
    
    os.makedirs("sample_outputs", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"before_after_{timestamp}.json"
    filepath = f"sample_outputs/{filename}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)
    
    print(f"     Saved before/after comparison: {filepath}")
    return filepath

def generate_feedback_attempts_report(traces: List[Dict[str, Any]]) -> str:
    """Generate summary report of feedback application attempts."""
    
    os.makedirs("reports", exist_ok=True)
    
    report_lines = []
    report_lines.append("FEEDBACK APPLICATION ATTEMPTS REPORT")
    report_lines.append("=" * 50)
    report_lines.append(f"Generated: {datetime.now().isoformat()}")
    report_lines.append("")
    
    retry_attempts = [t for t in traces if t.get('retry_info', {}).get('attempted', False)]
    
    report_lines.append(f"Total iterations: {len(traces)}")
    report_lines.append(f"Retry attempts: {len(retry_attempts)}")
    report_lines.append(f"Retry rate: {len(retry_attempts)/len(traces)*100:.1f}%")
    report_lines.append("")
    
    if retry_attempts:
        improvements = [t['retry_info']['improvement'] for t in retry_attempts]
        successful_improvements = [imp for imp in improvements if imp > 0]
        
        report_lines.append("RETRY OUTCOMES:")
        report_lines.append(f"Successful improvements: {len(successful_improvements)}/{len(retry_attempts)}")
        report_lines.append(f"Average improvement: {sum(improvements)/len(improvements):.3f}")
        report_lines.append(f"Best improvement: {max(improvements):.3f}")
        report_lines.append("")
        
        report_lines.append("DETAILED ATTEMPTS:")
        for i, trace in enumerate(retry_attempts, 1):
            retry_info = trace['retry_info']
            report_lines.append(f"{i}. Iteration {trace['iteration_id']}")
            report_lines.append(f"   Prompt: {trace['prompt'][:60]}...")
            report_lines.append(f"   Original reward: {retry_info['original_reward']:.3f}")
            report_lines.append(f"   Final reward: {trace['reward']:.3f}")
            report_lines.append(f"   Improvement: {retry_info['improvement']:.3f}")
            report_lines.append(f"   Status: {'SUCCESS' if retry_info['improvement'] > 0 else 'NO_IMPROVEMENT'}")
            report_lines.append("")
    else:
        report_lines.append("No retry attempts made (all rewards above threshold)")
    
    report_content = "\n".join(report_lines)
    
    with open("reports/day9_feedback_attempts.txt", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"Feedback attempts report saved to: reports/day9_feedback_attempts.txt")
    return "reports/day9_feedback_attempts.txt"

if __name__ == "__main__":
    # Test RL loop with sample prompts
    test_prompts = [
        "Design a wooden dining table",
        "Create a steel office chair", 
        "Build a 2-floor library with glass walls"
    ]
    
    # Run RL experiment
    traces = run_rl_experiment(test_prompts, iterations_per_prompt=2)
    
    # Analyze results
    analysis = analyze_rl_history()
    
    print(f"\n=== Analysis ===")
    print(f"Total iterations: {analysis['total_iterations']}")
    print(f"Average reward: {analysis['reward_stats']['mean']:.3f}")
    print(f"Positive rewards: {analysis['reward_stats']['positive_count']}/{analysis['total_iterations']}")
    print(f"Severity distribution: {analysis['severity_distribution']}")
    print(f"Average format score: {analysis['format_score_stats']['mean']:.1f}/10")