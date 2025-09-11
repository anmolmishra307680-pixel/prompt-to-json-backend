#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from main_agent import MainAgent
from evaluator_agent import EvaluatorAgent
from rl_loop import RLLoop
from prompt_logger import PromptLogger

def main():
    parser = argparse.ArgumentParser(description="Prompt-to-JSON Agent System")
    parser.add_argument("--prompt", type=str, help="Design prompt to process (not required for web mode)")
    parser.add_argument("--mode", type=str, choices=["single", "rl", "compare", "advanced-rl", "web"], default="single",
                       help="Execution mode: single, RL training, comparison, advanced RL, or web interface")
    parser.add_argument("--iterations", type=int, default=3, help="Number of RL iterations")
# LLM option removed - only rule-based generation available
    parser.add_argument("--binary-rewards", action="store_true", help="Use binary reward system (1/-1)")
    parser.add_argument("--use-db", action="store_true", help="Use database storage")
    parser.add_argument("--validate-json", action="store_true", help="Enable deep JSON validation")

    
    args = parser.parse_args()
    
    # Check if prompt is required
    if args.mode != "web" and not args.prompt:
        parser.error("--prompt is required for all modes except web")
    
    try:
        if args.mode == "single":
            run_single_mode(args.prompt, use_db=args.use_db)
        elif args.mode == "rl":
            run_rl_mode(args.prompt, args.iterations, args.binary_rewards, args.use_db)
        elif args.mode == "compare":
            run_compare_mode(args.prompt)
        elif args.mode == "advanced-rl":
            run_advanced_rl_mode(args.prompt, args.iterations, args.use_db)
        elif args.mode == "web":
            run_web_mode()
    
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

def run_single_mode(prompt: str, use_llm: bool = False, use_db: bool = False):
    """Run single iteration mode"""
    validate_prompt(prompt)
    print(f"Processing prompt: '{prompt}'")
    print("Mode: Rule-based")
    
    # Initialize agents and logger
    main_agent = MainAgent()
    evaluator_agent = EvaluatorAgent()
    prompt_logger = PromptLogger()
    
    # Initialize database if requested
    db_storage = None
    if use_db:
        from database_integration import SQLiteStorage
        db_storage = SQLiteStorage()
        print("Database storage enabled")
    
    # Generate specification
    print("\n1. Generating specification...")
    spec = main_agent.generate_spec(prompt)
    
    # Save specification
    spec_path = main_agent.save_spec(spec, prompt)
    print(f"Specification saved to: {spec_path}")
    
    # Save to database if enabled
    if db_storage:
        spec_id = db_storage.save_specification(spec, prompt)
        print(f"Specification saved to database with ID: {spec_id}")
    
    # Evaluate specification
    print("\n2. Evaluating specification...")
    evaluation = evaluator_agent.evaluate_spec(spec, prompt)
    
    # Save evaluation to database if enabled
    if db_storage and 'spec_id' in locals():
        eval_id = db_storage.save_evaluation(evaluation, spec_id)
        print(f"Evaluation saved to database with ID: {eval_id}")
    
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

def run_rl_mode(prompt: str, iterations: int, binary_rewards: bool = False, use_db: bool = False):
    """Run reinforcement learning mode"""
    validate_prompt(prompt)
    print(f"Running RL training for {iterations} iterations")
    
    # Initialize logger
    prompt_logger = PromptLogger()
    
    # Initialize database if requested
    if use_db:
        from database_integration import SQLiteStorage
        db_storage = SQLiteStorage()
        print("Database storage enabled for RL training")
    
    rl_loop = RLLoop(max_iterations=iterations, binary_rewards=binary_rewards)
    results = rl_loop.run_training_loop(prompt)
    
    # Save to database if enabled
    if use_db:
        for iteration in results['iterations']:
            spec_data = iteration['specification']
            from schema import DesignSpec
            spec = DesignSpec(**spec_data)
            spec_id = db_storage.save_specification(spec, f"{prompt} (RL iter {iteration['iteration']})")
            
            eval_data = iteration['evaluation']
            from schema import EvaluationResult
            evaluation = EvaluationResult(**eval_data)
            db_storage.save_evaluation(evaluation, spec_id)
        print(f"RL training data saved to database ({len(results['iterations'])} iterations)")
    
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
    print("Comparing rule-based configurations")
    
    rl_loop = RLLoop()
    comparison = rl_loop.compare_approaches(prompt)
    
    print(f"\n--- Comparison Results ---")
    print(f"Standard approach: {comparison['standard']['score']:.2f}")
    print(f"Enhanced approach: {comparison['enhanced']['score']:.2f}")
    print(f"Result: {comparison['result']}")

def validate_prompt(prompt: str, use_deep_validation: bool = False) -> bool:
    """Prompt validation with optional deep validation"""
    if use_deep_validation:
        from json_validator import InputSanitizer
        prompt = InputSanitizer.sanitize_prompt(prompt)
    
    if not prompt:
        raise ValueError("Prompt cannot be empty")
    
    prompt = prompt.strip()
    
    if len(prompt) < 3:
        raise ValueError(f"Prompt too short ({len(prompt)} chars). Minimum 3 characters required.")
    
    if len(prompt) > 1000:
        raise ValueError(f"Prompt too long ({len(prompt)} chars). Maximum 1000 characters allowed.")
    
    return True

def run_advanced_rl_mode(prompt: str, iterations: int, use_db: bool = False):
    """Run advanced RL mode with policy gradient"""
    validate_prompt(prompt)
    print(f"Running Advanced RL training for {iterations} steps")
    
    from advanced_rl import AdvancedRLEnvironment
    env = AdvancedRLEnvironment()
    
    # Initialize database if requested
    if use_db:
        from database_integration import SQLiteStorage
        db_storage = SQLiteStorage()
        print("Database storage enabled for Advanced RL")
    
    # Run single episode with specified number of steps
    result = env.train_episode(prompt, max_steps=iterations)
    print(f"Training completed: {result['steps']} steps, Final Score {result['final_score']:.2f}, Total Reward {result['total_reward']:.3f}")
    
    # Save to database if enabled
    if use_db:
        spec_id = db_storage.save_specification(result['final_spec'], f"{prompt} (Advanced RL)")
        print(f"Advanced RL result saved to database with ID: {spec_id}")
    
    print(f"\n--- Advanced RL Results ---")
    print(f"Final score: {result['final_score']:.2f}")
    print(f"Training file: {result['training_file']}")

def run_web_mode():
    """Launch Streamlit web interface"""
    import subprocess
    import sys
    
    print("Launching Streamlit web interface...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except FileNotFoundError:
        print("Streamlit not installed. Install with: pip install streamlit")
    except Exception as e:
        print(f"Failed to launch web interface: {str(e)}")

if __name__ == "__main__":
    main()