#!/usr/bin/env python3
"""Main CLI entry point for Prompt-to-JSON system"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Prompt-to-JSON Agent System")
    parser.add_argument("--prompt", type=str, help="Design prompt to process")
    parser.add_argument("--mode", type=str, choices=["single", "rl", "web"], default="single",
                       help="Execution mode: single, RL training, or web interface")
    parser.add_argument("--iterations", type=int, default=3, help="Number of RL iterations")
    parser.add_argument("--api", action="store_true", help="Launch FastAPI server")
    
    args = parser.parse_args()
    
    if args.api:
        run_api_server()
        return
    
    if args.mode == "web":
        print("Web mode not available in streamlined version")
        print("Use: python main_api.py")
        return
    
    if not args.prompt:
        parser.error("--prompt is required")
    
    try:
        if args.mode == "single":
            run_single_mode(args.prompt)
        elif args.mode == "rl":
            run_rl_mode(args.prompt, args.iterations)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def run_single_mode(prompt: str):
    """Run single iteration mode"""
    print(f"Processing prompt: '{prompt}'")
    
    from prompt_agent import MainAgent
    from evaluator import EvaluatorAgent
    
    # Generate specification
    main_agent = MainAgent()
    spec = main_agent.run(prompt)
    
    # Evaluate specification
    evaluator_agent = EvaluatorAgent()
    evaluation = evaluator_agent.run(spec, prompt)
    
    # Display results
    print(f"\n--- Results ---")
    print(f"Overall Score: {evaluation.score:.2f}/100")
    print(f"Building Type: {spec.building_type}")
    print(f"Stories: {spec.stories}")

def run_rl_mode(prompt: str, iterations: int):
    """Run RL training mode"""
    print(f"Running RL training for {iterations} iterations")
    
    from rl_agent import RLLoop
    
    rl_loop = RLLoop(max_iterations=iterations)
    results = rl_loop.run(prompt, iterations)
    
    print(f"\n--- RL Training Results ---")
    print(f"Total iterations: {len(results.get('iterations', []))}")
    if results.get('iterations'):
        final_score = results['iterations'][-1]['score_after']
        print(f"Final score: {final_score:.2f}")

def run_api_server():
    """Launch FastAPI server"""
    print("Launching FastAPI server...")
    import subprocess
    import sys
    subprocess.run([sys.executable, "main_api.py"])

if __name__ == "__main__":
    main()