"""Advanced RL environment with policy gradient methods"""

import numpy as np
from typing import Dict, List, Tuple
from schema import DesignSpec, EvaluationResult

class PolicyGradientAgent:
    """Simple policy gradient agent for spec improvement"""
    
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
        self.policy_weights = np.random.randn(10)  # Simple policy
        self.action_history = []
        self.reward_history = []
    
    def select_action(self, state: np.ndarray) -> int:
        """Select action using policy"""
        logits = np.dot(state, self.policy_weights[:len(state)])
        if np.isscalar(logits):
            logits = np.array([logits, -logits, 0])  # 3 actions
        probabilities = self._softmax(logits)
        action = np.random.choice(len(probabilities), p=probabilities)
        return action
    
    def update_policy(self, states: List[np.ndarray], actions: List[int], rewards: List[float]):
        """Update policy using REINFORCE algorithm"""
        for state, action, reward in zip(states, actions, rewards):
            # Simple gradient update
            gradient = state * (reward - np.mean(rewards))
            self.policy_weights[:len(state)] += self.learning_rate * gradient
    
    def _softmax(self, x):
        """Softmax activation"""
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)

class AdvancedRLEnvironment:
    """Advanced RL environment for specification improvement"""
    
    def __init__(self):
        self.agent = PolicyGradientAgent()
        self.state_dim = 5  # [score, materials_count, features_count, stories, area]
    
    def get_state(self, spec: DesignSpec, evaluation: EvaluationResult) -> np.ndarray:
        """Convert spec and evaluation to state vector"""
        return np.array([
            evaluation.score / 100.0,
            len(spec.materials),
            len(spec.features),
            spec.stories,
            (spec.dimensions.area or 0) / 1000.0
        ])
    
    def apply_action(self, spec: DesignSpec, action: int) -> DesignSpec:
        """Apply action to modify specification"""
        from main_agent import MainAgent
        agent = MainAgent()
        
        if action == 0:  # Add material
            if len(spec.materials) < 3:
                from schema import MaterialSpec
                spec.materials.append(MaterialSpec(type="concrete"))
        elif action == 1:  # Add feature
            if "elevator" not in spec.features:
                spec.features.append("elevator")
        elif action == 2:  # Increase stories
            if spec.stories < 5:
                spec.stories += 1
                spec.dimensions.height = spec.stories * 3.5
        
        return spec
    
    def train_episode(self, prompt: str, max_steps: int = 5) -> Dict:
        """Train one episode using policy gradient with logging"""
        try:
            from main_agent import MainAgent
            from evaluator_agent import EvaluatorAgent
            from evaluator.feedback import FeedbackLoop
            from datetime import datetime
            import json
            from pathlib import Path
            
            main_agent = MainAgent()
            evaluator_agent = EvaluatorAgent()
            feedback_loop = FeedbackLoop()
            
            # Initial spec
            initial_spec = main_agent.generate_spec(prompt)
            spec = initial_spec
            
            states, actions, rewards = [], [], []
            iteration_results = []
            
            for step in range(max_steps):
                try:
                    # Get current state
                    evaluation = evaluator_agent.evaluate_spec(spec, prompt)
                    state = self.get_state(spec, evaluation)
                    
                    # Select action
                    action = self.agent.select_action(state)
                    
                    # Apply action
                    new_spec = self.apply_action(spec, action)
                    new_evaluation = evaluator_agent.evaluate_spec(new_spec, prompt)
                    
                    # Calculate reward
                    reward = (new_evaluation.score - evaluation.score) / 100.0
                    
                    # Log iteration to feedback system
                    try:
                        feedback_loop.log_iteration(
                            prompt, spec, new_spec, new_evaluation, reward, step + 1
                        )
                    except Exception as log_error:
                        print(f"Warning: Failed to log iteration {step + 1}: {log_error}")
                    
                    # Save spec for this step
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    spec_filename = f"design_spec_{timestamp}_advrl_step{step + 1}.json"
                    spec_path = main_agent.spec_outputs_dir / spec_filename
                    
                    output_data = {
                        "prompt": f"{prompt} (Advanced RL step {step + 1})",
                        "specification": new_spec.model_dump(),
                        "metadata": {
                            "generated_at": datetime.now().isoformat(),
                            "generator": "AdvancedRL",
                            "step": step + 1,
                            "action": int(action),
                            "reward": float(reward)
                        }
                    }
                    
                    with open(spec_path, 'w') as f:
                        json.dump(output_data, f, indent=2, default=str)
                    
                    # Store iteration result
                    iteration_results.append({
                        "step": step + 1,
                        "specification": new_spec.model_dump(),
                        "evaluation": new_evaluation.model_dump(),
                        "action": int(action),
                        "reward": float(reward),
                        "spec_file": str(spec_path)
                    })
                    
                    # Store experience
                    states.append(state)
                    actions.append(action)
                    rewards.append(reward)
                    
                    spec = new_spec
                    
                except Exception as step_error:
                    print(f"Warning: Step {step + 1} failed: {step_error}")
                    # Continue with current spec
                    continue
            
            # Update policy
            if states and actions and rewards:
                try:
                    self.agent.update_policy(states, actions, rewards)
                except Exception as policy_error:
                    print(f"Warning: Policy update failed: {policy_error}")
            
            # Save training results
            training_results = {
                "prompt": prompt,
                "algorithm": "REINFORCE",
                "steps": iteration_results,
                "final_spec": spec.model_dump(),
                "total_reward": sum(rewards) if rewards else 0.0,
                "learning_insights": None
            }
            
            # Save to logs
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = Path("logs") / f"advanced_rl_training_{timestamp}.json"
            try:
                with open(log_file, 'w') as f:
                    json.dump(training_results, f, indent=2, default=str)
            except Exception as save_error:
                print(f"Warning: Failed to save training results: {save_error}")
            
            # Ensure we have a final evaluation
            final_evaluation = evaluator_agent.evaluate_spec(spec, prompt)
            
            return {
                "final_spec": spec,
                "final_score": final_evaluation.score,
                "total_reward": sum(rewards) if rewards else 0.0,
                "steps": len(states),
                "training_file": str(log_file)
            }
            
        except Exception as e:
            print(f"Advanced RL training failed completely: {e}")
            # Return minimal fallback result
            from main_agent import MainAgent
            main_agent = MainAgent()
            fallback_spec = main_agent.generate_spec(prompt)
            
            return {
                "final_spec": fallback_spec,
                "final_score": 0.0,
                "total_reward": 0.0,
                "steps": 0,
                "training_file": "none",
                "error": str(e)
            }