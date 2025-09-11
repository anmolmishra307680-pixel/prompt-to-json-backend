#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from main_agent import MainAgent
from evaluator_agent import EvaluatorAgent
from rl_loop import RLLoop
from prompt_logger import PromptLogger
from daily_logger import DailyLogger

def main():
    parser = argparse.ArgumentParser(description="Prompt-to-JSON Agent System")
    parser.add_argument("--prompt", type=str, required=True, help="Design prompt to process")
    parser.add_argument("--mode", type=str, choices=["single", "rl", "compare"], default="single",
                       help="Execution mode: single iteration, RL training, or comparison")
    parser.add_argument("--iterations", type=int, default=3, help="Number of RL iterations")
    parser.add_argument("--use-llm", action="store_true", help="Use LLM generation (stub)")
    
    args = parser.parse_args()
    
    try:
        if args.mode == "single":
            run_single_mode(args.prompt, args.use_llm)
        elif args.mode == "rl":
            run_rl_mode(args.prompt, args.iterations)
        elif args.mode == "compare":
            run_compare_mode(args.prompt)
    
    except ValueError as e:
        print(f"Input Error: {str(e)}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"File Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        print("Please check your input and try again.")
        sys.exit(1)

def run_single_mode(prompt: str, use_llm: bool = False):
    """Run single iteration mode"""
    validate_prompt(prompt)
    print(f"Processing prompt: '{prompt}'")
    print(f"Mode: {'LLM' if use_llm else 'Rule-based'}")
    
    # Initialize agents and logger
    main_agent = MainAgent()
    evaluator_agent = EvaluatorAgent()
    prompt_logger = PromptLogger()
    
    # Generate specification
    print("\n1. Generating specification...")
    spec = main_agent.generate_spec(prompt, use_llm=use_llm)
    
    # Save specification
    spec_path = main_agent.save_spec(spec, prompt)
    print(f"Specification saved to: {spec_path}")
    
    # Evaluate specification
    print("\n2. Evaluating specification...")
    evaluation = evaluator_agent.evaluate_spec(spec, prompt)
    
    # Log prompt and result
    result = {
        "spec_file": spec_path,
        "evaluation": evaluation.model_dump()
    }
    prompt_logger.log_prompt_result(prompt, result, "single")
    
    # Display results
    print(f"\n--- Results ---")
    print(f"Overall Score: {evaluation.score:.2f}/100")
    print(f"Completeness: {evaluation.completeness:.2f}/100")
    print(f"Format Validity: {evaluation.format_validity:.2f}/100")
    
    if evaluation.feedback:
        print(f"\nFeedback:")
        for feedback in evaluation.feedback:
            print(f"  - {feedback}")
    
    if evaluation.suggestions:
        print(f"\nSuggestions:")
        for suggestion in evaluation.suggestions:
            print(f"  - {suggestion}")

def run_rl_mode(prompt: str, iterations: int):
    """Run reinforcement learning mode"""
    validate_prompt(prompt)
    print(f"Running RL training for {iterations} iterations")
    
    # Initialize logger
    prompt_logger = PromptLogger()
    
    rl_loop = RLLoop(max_iterations=iterations)
    results = rl_loop.run_training_loop(prompt)
    
    # Log RL training result
    result = {
        "training_file": f"logs/rl_training_{results.get('timestamp', 'unknown')}.json",
        "iterations": len(results['iterations']),
        "final_score": results['iterations'][-1]['evaluation']['score'] if results['iterations'] else 0
    }
    prompt_logger.log_prompt_result(prompt, result, "rl")
    
    print(f"\n--- RL Training Results ---")
    print(f"Total iterations: {len(results['iterations'])}")
    
    if results['iterations']:
        final_score = results['iterations'][-1]['evaluation']['score']
        initial_score = results['iterations'][0]['evaluation']['score']
        improvement = final_score - initial_score
        
        print(f"Initial score: {initial_score:.2f}")
        print(f"Final score: {final_score:.2f}")
        print(f"Improvement: {improvement:+.2f}")
    
    if results['learning_insights']:
        insights = results['learning_insights']
        print(f"\n--- Learning Insights ---")
        print(f"Average score: {insights.get('average_score', 0):.2f}")
        print(f"Score trend: {insights.get('score_trend', 'unknown')}")
        print(f"Best iteration: {insights.get('best_iteration', 'unknown')}")

def run_compare_mode(prompt: str):
    """Run comparison mode"""
    print("Comparing rule-based vs LLM approaches")
    
    rl_loop = RLLoop()
    comparison = rl_loop.compare_approaches(prompt)
    
    print(f"\n--- Comparison Results ---")
    print(f"Rule-based approach: {comparison['rule_based']['score']:.2f}")
    print(f"LLM approach: {comparison['llm_based']['score']:.2f}")
    print(f"Winner: {comparison['winner']}")

def validate_prompt(prompt: str) -> bool:
    """Validate input prompt"""
    if not prompt or len(prompt.strip()) < 10:
        raise ValueError("Prompt must be at least 10 characters long")
    
    if len(prompt) > 1000:
        raise ValueError("Prompt too long (max 1000 characters)")
    
    return True

if __name__ == "__main__":
    # Example usage if run directly
    if len(sys.argv) == 1:
        print("Example usage:")
        print("python main.py --prompt 'Design a two-story steel building with glass facade'")
        print("python main.py --prompt 'Modern office building' --mode rl --iterations 5")
        print("python main.py --prompt 'Residential complex' --mode compare")
        sys.exit(0)
    
    main()