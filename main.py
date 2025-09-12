#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from main_agent import MainAgent
from evaluator_agent import EvaluatorAgent
from rl_loop import RLLoop
from prompt_logger import PromptLogger
from universal_agent import UniversalAgent
from universal_evaluator import UniversalEvaluator
from universal_schema import UniversalSpec
import json
from datetime import datetime

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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--cleanup", action="store_true", help="Clean old files before running")
    parser.add_argument("--final-only", action="store_true", help="Save only final results (not intermediate steps)")
    parser.add_argument("--universal", action="store_true", help="Use universal agent for any prompt type")
    parser.add_argument("--test", action="store_true", help="Run system tests")
    parser.add_argument("--cli-tools", action="store_true", help="Launch CLI tools interface")
    parser.add_argument("--score-only", action="store_true", help="Use data scorer for quick scoring")
    parser.add_argument("--examples", action="store_true", help="Show sample outputs and examples")

    
    args = parser.parse_args()
    
    # Handle tools first (no prompt needed)
    if args.test:
        run_system_tests()
        return
    if args.cli_tools:
        run_cli_tools()
        return
    if args.score_only:
        run_score_only_mode(args.prompt)
        return
    if args.examples:
        show_sample_outputs()
        return
    
    # Check if prompt is required for other modes
    if args.mode != "web" and not args.prompt:
        parser.error("--prompt is required for all modes except web")
    
    # Cleanup old files if requested
    if args.cleanup:
        cleanup_old_files()
    
    try:
        if args.mode == "single":
            if args.universal:
                run_universal_mode(args.prompt, use_db=args.use_db)
            else:
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
    
    # Log to main logs.json immediately
    from pathlib import Path
    logs_dir = Path("logs")
    logs_file = logs_dir / "logs.json"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "mode": "rl",
        "iterations_requested": iterations,
        "status": "started"
    }
    
    logs = []
    if logs_file.exists():
        with open(logs_file, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    
    logs.append(log_entry)
    
    with open(logs_file, 'w') as f:
        json.dump(logs, f, indent=2, default=str)
    
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
    
    # Log RL training result (with error handling)
    try:
        result = {
            "training_file": f"logs/rl_training_{results.get('timestamp', 'unknown')}.json",
            "iterations": len(results['iterations']),
            "final_score": results['iterations'][-1]['evaluation']['score'] if results['iterations'] else 0
        }
        prompt_logger.log_prompt_result(prompt, result, "rl")
    except Exception as e:
        print(f"Warning: Failed to log RL result: {e}")
    
    # Also log to main logs.json (with error handling)
    try:
        from pathlib import Path
        logs_dir = Path("logs")
        logs_file = logs_dir / "logs.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "mode": "rl",
            "iterations": len(results['iterations']),
            "final_score": results['iterations'][-1]['evaluation']['score'] if results['iterations'] else 0,
            "training_file": f"logs/rl_training_{results.get('timestamp', 'unknown')}.json"
        }
        
        logs = []
        if logs_file.exists():
            with open(logs_file, 'r') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
        
        logs.append(log_entry)
        
        with open(logs_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)
        
        print(f"RL training logged to: {logs_file}")
    except Exception as e:
        print(f"Warning: Failed to log to main logs.json: {e}")
    
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
    
    # Log to main logs.json
    from pathlib import Path
    logs_dir = Path("logs")
    logs_file = logs_dir / "logs.json"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "mode": "compare",
        "rule_based_score": comparison["rule_based"]["score"],
        "advanced_rl_score": comparison["advanced_rl"]["score"],
        "winner": comparison["winner"]
    }
    
    logs = []
    if logs_file.exists():
        with open(logs_file, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    
    logs.append(log_entry)
    
    with open(logs_file, 'w') as f:
        json.dump(logs, f, indent=2, default=str)
    
    print(f"Comparison logged to: {logs_file}")
    


def validate_prompt(prompt: str, use_deep_validation: bool = False, verbose: bool = False) -> bool:
    """Prompt validation with optional deep validation"""
    if use_deep_validation:
        from json_validator import InputSanitizer
        if verbose:
            print(f"[VERBOSE] Applying deep validation to prompt: '{prompt[:50]}...'")
        prompt = InputSanitizer.sanitize_prompt(prompt)
        if verbose:
            print(f"[VERBOSE] Sanitized prompt: '{prompt[:50]}...'")
    
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
    
    try:
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
        
        # Log to main logs.json
        from pathlib import Path
        logs_dir = Path("logs")
        logs_file = logs_dir / "logs.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "mode": "advanced_rl",
            "steps": result['steps'],
            "final_score": result['final_score'],
            "total_reward": result['total_reward'],
            "training_file": result['training_file']
        }
        
        logs = []
        if logs_file.exists():
            with open(logs_file, 'r') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
        
        logs.append(log_entry)
        
        with open(logs_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)
        
        print(f"Advanced RL logged to: {logs_file}")
        
        # Save to database if enabled
        if use_db:
            spec_id = db_storage.save_specification(result['final_spec'], f"{prompt} (Advanced RL)")
            print(f"Advanced RL result saved to database with ID: {spec_id}")
        
        print(f"\n--- Advanced RL Results ---")
        print(f"Final score: {result['final_score']:.2f}")
        print(f"Training file: {result['training_file']}")
        
    except Exception as e:
        print(f"Advanced RL training failed: {e}")
        # Still log the attempt
        try:
            from pathlib import Path
            logs_dir = Path("logs")
            logs_file = logs_dir / "logs.json"
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt,
                "mode": "advanced_rl",
                "status": "failed",
                "error": str(e)
            }
            
            logs = []
            if logs_file.exists():
                with open(logs_file, 'r') as f:
                    try:
                        logs = json.load(f)
                    except:
                        logs = []
            
            logs.append(log_entry)
            
            with open(logs_file, 'w') as f:
                json.dump(logs, f, indent=2, default=str)
        except Exception as log_error:
            print(f"Failed to log error: {log_error}")

def run_universal_mode(prompt: str, use_db: bool = False):
    """Run universal mode for any prompt type"""
    print(f"Processing prompt: '{prompt}'")
    print("Mode: Universal (Any Prompt Type)")
    
    # Initialize universal agents
    universal_agent = UniversalAgent()
    universal_evaluator = UniversalEvaluator()
    prompt_logger = PromptLogger()
    
    # Initialize database if requested
    db_storage = None
    if use_db:
        from database_integration import SQLiteStorage
        db_storage = SQLiteStorage()
        print("Database storage enabled")
    
    # Generate universal specification
    print("\n1. Generating universal specification...")
    spec = universal_agent.generate_spec(prompt)
    
    # Save specification
    spec_path = universal_agent.save_spec(spec, prompt)
    print(f"Universal specification saved to: {spec_path}")
    
    # Save to database if enabled
    if db_storage:
        # Convert UniversalSpec to DesignSpec for database compatibility
        from schema import DesignSpec, MaterialSpec, DimensionSpec
        db_spec = DesignSpec(
            building_type=spec.prompt_type,
            stories=1,
            materials=[MaterialSpec(type=comp.get('type', 'unknown')) for comp in spec.components[:3]],
            dimensions=DimensionSpec(length=1, width=1, height=1, area=1),
            features=[prop for prop in spec.properties.keys()][:5],
            requirements=spec.requirements
        )
        spec_id = db_storage.save_specification(db_spec, prompt)
        print(f"Universal specification saved to database with ID: {spec_id}")
    
    # Evaluate specification
    print("\n2. Evaluating specification...")
    evaluation = universal_evaluator.evaluate_spec(spec, prompt)
    
    # Save evaluation to database if enabled
    if db_storage and 'spec_id' in locals():
        eval_id = db_storage.save_evaluation(evaluation, spec_id)
        print(f"Evaluation saved to database with ID: {eval_id}")
    
    # Save evaluation report
    from evaluator.report import ReportGenerator
    report_generator = ReportGenerator()
    # Create dummy spec for report compatibility
    from schema import DesignSpec, MaterialSpec, DimensionSpec
    dummy_spec = DesignSpec(
        building_type=spec.prompt_type,
        stories=1,
        materials=[],
        dimensions=DimensionSpec(length=1, width=1, height=1, area=1),
        features=[],
        requirements=spec.requirements
    )
    report_path = report_generator.generate_report(dummy_spec, evaluation, prompt)
    print(f"Evaluation report saved to: {report_path}")
    
    # Save to logs
    from pathlib import Path
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    logs_file = logs_dir / "logs.json"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "mode": "universal",
        "prompt_type": spec.prompt_type,
        "score": evaluation.score,
        "spec_file": spec_path,
        "report_file": report_path
    }
    
    # Append to logs
    logs = []
    if logs_file.exists():
        with open(logs_file, 'r') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    
    logs.append(log_entry)
    
    with open(logs_file, 'w') as f:
        json.dump(logs, f, indent=2, default=str)
    
    print(f"Log entry saved to: {logs_file}")
    
    # Create feedback log entry for single mode
    feedback_logs_file = logs_dir / "feedback_log.json"
    feedback_entry = {
        "iteration": 1,
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "mode": "universal_single",
        "evaluation": evaluation.model_dump(),
        "improvements": {"single_mode": "no_iterations"}
    }
    
    feedback_logs = []
    if feedback_logs_file.exists():
        with open(feedback_logs_file, 'r') as f:
            try:
                feedback_logs = json.load(f)
            except:
                feedback_logs = []
    
    feedback_logs.append(feedback_entry)
    
    with open(feedback_logs_file, 'w') as f:
        json.dump(feedback_logs, f, indent=2, default=str)
    
    print(f"Feedback log entry saved to: {feedback_logs_file}")
    
    # Log result
    result = {
        "spec_file": spec_path,
        "evaluation": evaluation.model_dump(),
        "prompt_type": spec.prompt_type
    }
    prompt_logger.log_prompt_result(prompt, result, "universal")
    
    # Display results
    print(f"\n--- Universal Results ---")
    print(f"Prompt Type: {spec.prompt_type}")
    print(f"Overall Score: {evaluation.score:.2f}/100")
    print(f"Components: {len(spec.components)}")
    print(f"Confidence: {spec.metadata.get('confidence', 'N/A')}")

def run_system_tests():
    """Run comprehensive system tests"""
    print("Running system tests...")
    try:
        import test_system
        test_system.run_all_tests()
    except Exception as e:
        print(f"Test execution failed: {str(e)}")

def run_cli_tools():
    """Launch CLI tools interface"""
    print("Launching CLI tools...")
    try:
        import sys
        # Clear sys.argv to avoid argument conflicts
        original_argv = sys.argv.copy()
        sys.argv = ['cli_tools.py']
        
        import cli_tools
        cli_tools.main()
        
        # Restore original argv
        sys.argv = original_argv
    except Exception as e:
        print(f"CLI tools failed: {str(e)}")

def run_score_only_mode(prompt: str):
    """Run quick scoring mode using data_scorer"""
    print(f"Quick scoring for: '{prompt}'")
    print("Mode: Data Scorer (Fast)")
    
    # Generate spec quickly
    from main_agent import MainAgent
    agent = MainAgent()
    spec = agent.generate_spec(prompt)
    
    # Use data scorer for quick evaluation
    from data_scorer import DataScorer
    scorer = DataScorer()
    
    print("\n--- Quick Scores ---")
    completeness = scorer.score_completeness(spec)
    format_validity = scorer.score_format_validity(spec)
    feasibility = scorer.score_feasibility(spec)
    overall = scorer.calculate_overall_score(spec)
    
    print(f"Completeness: {completeness:.1f}/100")
    print(f"Format Validity: {format_validity:.1f}/100")
    print(f"Feasibility: {feasibility:.1f}/100")
    print(f"Overall Score: {overall:.1f}/100")
    
    # Quick save
    spec_path = agent.save_spec(spec, prompt)
    print(f"\nSpec saved to: {spec_path}")

def show_sample_outputs():
    """Display sample outputs and examples"""
    import json
    from pathlib import Path
    
    print("=== SAMPLE OUTPUTS & EXAMPLES ===")
    
    sample_dir = Path("sample_outputs")
    if not sample_dir.exists():
        print("No sample outputs directory found")
        return
    
    samples = {
        "sample_spec_1.json": "Perfect Office Building Specification",
        "sample_evaluation_1.json": "Complete Evaluation Report", 
        "sample_rl_training.json": "RL Training Session Results"
    }
    
    for filename, description in samples.items():
        filepath = sample_dir / filename
        if filepath.exists():
            print(f"\n--- {description} ---")
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if "specification" in data:
                    spec = data["specification"]
                    print(f"Type: {spec.get('building_type', 'N/A')}")
                    print(f"Stories: {spec.get('stories', 'N/A')}")
                    print(f"Materials: {len(spec.get('materials', []))}")
                elif "score" in data:
                    print(f"Score: {data.get('score', 'N/A')}/100")
                    print(f"Feedback: {len(data.get('feedback', []))} items")
                elif "iterations" in data:
                    print(f"Iterations: {len(data.get('iterations', []))}")
                    print(f"Final Score: {data.get('final_score', 'N/A')}")
                
                print(f"File: {filepath}")
                
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        else:
            print(f"\n--- {description} ---")
            print(f"Sample file not found: {filepath}")
    
    print("\n=== USAGE EXAMPLES ===")
    print("Generate similar outputs:")
    print("  python main.py --prompt 'Office building' --mode single")
    print("  python main.py --prompt 'Warehouse' --mode rl --iterations 2")
    print("  python main.py --prompt 'Hospital' --mode compare")
    
    print("\n=== SAMPLE TEMPLATES ===")
    print("Use these sample files as templates for:")
    print("  - Understanding output format")
    print("  - Testing system integration")
    print("  - Benchmarking new implementations")
    print("  - Documentation examples")

def run_web_mode():
    """Launch Streamlit web interface"""
    import subprocess
    import sys
    import os
    
    print("Launching Streamlit web interface...")
    try:
        # Set environment variable to fix path watcher issue
        env = os.environ.copy()
        env['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], env=env)
    except FileNotFoundError:
        print("Streamlit not installed. Install with: pip install streamlit")
    except KeyboardInterrupt:
        print("\nStreamlit app stopped by user.")
    except Exception as e:
        print(f"Failed to launch web interface: {str(e)}")

if __name__ == "__main__":
    main()