import json
from pathlib import Path
from main_agent import MainAgent
from evaluator_agent import EvaluatorAgent
from evaluator.feedback import FeedbackLoop
from schema import DesignSpec

class RLLoop:
    def __init__(self, max_iterations: int = 3):
        self.main_agent = MainAgent()
        self.evaluator_agent = EvaluatorAgent()
        self.feedback_loop = FeedbackLoop()
        self.max_iterations = max_iterations
        
        # Create logs directory
        Path("logs").mkdir(exist_ok=True)
    
    def run_training_loop(self, prompt: str) -> dict:
        """Run reinforcement learning training loop"""
        print(f"Starting RL training loop for prompt: '{prompt}'")
        
        results = {
            "prompt": prompt,
            "iterations": [],
            "final_spec": None,
            "learning_insights": None
        }
        
        current_spec = None
        previous_score = 0
        
        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")
            
            # Generate specification
            if iteration == 0:
                # Initial generation
                spec = self.main_agent.generate_spec(prompt)
            else:
                # Improve based on feedback
                feedback_suggestions = self.feedback_loop.get_feedback_for_prompt(prompt)
                spec = self.main_agent.improve_spec_with_feedback(
                    current_spec, 
                    evaluation.feedback, 
                    evaluation.suggestions + feedback_suggestions
                )
            
            # Save specification for each iteration
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            spec_filename = f"design_spec_{timestamp}_iter{iteration + 1}.json"
            spec_path = self.main_agent.spec_outputs_dir / spec_filename
            
            output_data = {
                "prompt": f"{prompt} (RL iteration {iteration + 1})",
                "specification": spec.model_dump(),
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "generator": "MainAgent",
                    "iteration": iteration + 1,
                    "rl_mode": True
                }
            }
            
            import json
            with open(spec_path, 'w') as f:
                json.dump(output_data, f, indent=2, default=str)
            
            print(f"Specification saved to: {spec_path}")
            
            # Evaluate specification
            evaluation = self.evaluator_agent.evaluate_spec(spec, prompt)
            
            # Calculate reward
            reward = self.feedback_loop.calculate_reward(evaluation, previous_score)
            
            # Log iteration (always log, use dummy spec for first iteration)
            if current_spec:
                self.feedback_loop.log_iteration(
                    prompt, current_spec, spec, evaluation, reward, iteration + 1
                )
            else:
                # Log first iteration with empty previous spec
                dummy_spec = DesignSpec(building_type="initial", stories=0)
                self.feedback_loop.log_iteration(
                    prompt, dummy_spec, spec, evaluation, reward, iteration + 1
                )
            
            # Store iteration results
            iteration_result = {
                "iteration": iteration + 1,
                "specification": spec.model_dump(),
                "evaluation": evaluation.model_dump(),
                "reward": reward,
                "improvement": evaluation.score - previous_score if iteration > 0 else 0,
                "spec_file": str(spec_path)
            }
            results["iterations"].append(iteration_result)
            
            print(f"Score: {evaluation.score:.2f}, Reward: {reward:.3f}")
            
            # Update for next iteration
            current_spec = spec
            previous_score = evaluation.score
            
            # Continue for at least 2 iterations to generate feedback
            if evaluation.score >= 95 and iteration > 0:
                print("Early stopping: High score achieved")
                break
        
        results["final_spec"] = current_spec.model_dump() if current_spec else None
        results["learning_insights"] = self.feedback_loop.get_learning_insights()
        
        # Save training results
        self._save_training_results(results)
        
        return results
    
    def _save_training_results(self, results: dict):
        """Save training results to logs"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Path("logs") / f"rl_training_{timestamp}.json"
        
        with open(log_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Training results saved to: {log_file}")
    
    def run_single_iteration(self, prompt: str, use_llm: bool = False) -> dict:
        """Run a single iteration of the loop"""
        # Generate specification
        spec = self.main_agent.generate_spec(prompt, use_llm=use_llm)
        
        # Evaluate specification
        evaluation = self.evaluator_agent.evaluate_spec(spec, prompt)
        
        # Calculate reward
        reward = self.feedback_loop.calculate_reward(evaluation)
        
        # Save specification
        spec_path = self.main_agent.save_spec(spec, prompt)
        
        return {
            "specification": spec,
            "evaluation": evaluation,
            "reward": reward,
            "spec_file": spec_path
        }
    
    def compare_approaches(self, prompt: str) -> dict:
        """Compare rule-based vs LLM approaches"""
        print("Comparing rule-based vs LLM approaches...")
        
        # Rule-based approach
        rule_result = self.run_single_iteration(prompt, use_llm=False)
        
        # LLM approach (stub)
        llm_result = self.run_single_iteration(prompt, use_llm=True)
        
        comparison = {
            "prompt": prompt,
            "rule_based": {
                "score": rule_result["evaluation"].score,
                "reward": rule_result["reward"]
            },
            "llm_based": {
                "score": llm_result["evaluation"].score,
                "reward": llm_result["reward"]
            },
            "winner": "rule_based" if rule_result["evaluation"].score > llm_result["evaluation"].score else "llm_based"
        }
        
        print(f"Rule-based score: {rule_result['evaluation'].score:.2f}")
        print(f"LLM-based score: {llm_result['evaluation'].score:.2f}")
        print(f"Winner: {comparison['winner']}")
        
        return comparison