"""Optional RL environment for spec generation using gymnasium interface."""

import numpy as np
from typing import Dict, Tuple, Any, Optional
from src.extractor import extract_basic_fields
from evaluator_agent import evaluate_spec
from data_scorer import score_spec
from utils import apply_fallbacks

class SpecGenerationEnv:
    """Gymnasium-style environment for furniture specification generation."""
    
    def __init__(self):
        self.current_prompt = ""
        self.current_spec = {}
        self.step_count = 0
        self.max_steps = 10
        
        # Action space: modify spec fields
        self.field_names = ['type', 'material', 'color', 'dimensions', 'purpose']
        
    def reset(self, prompt: str = "Create a wooden table") -> Dict[str, Any]:
        """Reset environment with new prompt."""
        self.current_prompt = prompt
        self.step_count = 0
        
        # Initialize with extracted fields
        extracted = extract_basic_fields(prompt)
        self.current_spec = apply_fallbacks(extracted)
        
        return self._get_observation()
    
    def step(self, action: Dict[str, str]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """Take action to modify spec and return (obs, reward, done, info)."""
        self.step_count += 1
        
        # Apply action to modify spec
        for field, value in action.items():
            if field in self.field_names and value:
                self.current_spec[field] = value
        
        # Evaluate current spec
        evaluation = evaluate_spec(self.current_prompt, self.current_spec)
        scoring = score_spec(self.current_spec, self.current_prompt)
        
        # Calculate reward
        reward = self._calculate_reward(evaluation, scoring)
        
        # Check if done
        done = (self.step_count >= self.max_steps or 
                evaluation['severity'] == 'none' or
                scoring['format_score'] >= 9.0)
        
        # Prepare info
        info = {
            'evaluation': evaluation,
            'scoring': scoring,
            'step_count': self.step_count,
            'spec_score': scoring['format_score']
        }
        
        return self._get_observation(), reward, done, info
    
    def _get_observation(self) -> Dict[str, Any]:
        """Get current environment observation."""
        return {
            'prompt': self.current_prompt,
            'spec': self.current_spec.copy(),
            'step': self.step_count,
            'prompt_embedding': self._encode_prompt(self.current_prompt)
        }
    
    def _encode_prompt(self, prompt: str) -> np.ndarray:
        """Simple prompt encoding for observation space."""
        # Basic word count features
        words = prompt.lower().split()
        features = np.zeros(10)
        
        # Feature engineering
        features[0] = len(words)  # Word count
        features[1] = len([w for w in words if w in ['wooden', 'metal', 'glass']])  # Material words
        features[2] = len([w for w in words if w in ['table', 'chair', 'cabinet']])  # Type words
        features[3] = len([w for w in words if any(c.isdigit() for c in w)])  # Numeric words
        features[4] = 1 if 'eco' in prompt.lower() else 0  # Eco-friendly flag
        
        return features
    
    def _calculate_reward(self, evaluation: Dict, scoring: Dict) -> float:
        """Calculate reward based on evaluation and scoring."""
        base_reward = scoring['format_score'] / 10.0  # 0-1 scale
        
        # Penalty for issues
        issue_penalty = len(evaluation['issues']) * 0.1
        
        # Bonus for completion
        completion_bonus = 0.2 if evaluation['severity'] == 'none' else 0
        
        # Step penalty to encourage efficiency
        step_penalty = self.step_count * 0.01
        
        return base_reward - issue_penalty + completion_bonus - step_penalty
    
    def render(self, mode: str = 'human') -> Optional[str]:
        """Render current environment state."""
        if mode == 'human':
            print(f"Step: {self.step_count}")
            print(f"Prompt: {self.current_prompt}")
            print(f"Current Spec: {self.current_spec}")
            
            # Quick evaluation
            evaluation = evaluate_spec(self.current_prompt, self.current_spec)
            scoring = score_spec(self.current_spec, self.current_prompt)
            
            print(f"Score: {scoring['format_score']}/10")
            print(f"Issues: {len(evaluation['issues'])}")
            print("-" * 50)
        
        return None

def demo_rl_env():
    """Demonstrate the RL environment."""
    env = SpecGenerationEnv()
    
    # Test prompts
    test_prompts = [
        "Create a wooden dining table",
        "Design a carbon fiber drone body",
        "Build a steel medical cabinet"
    ]
    
    for prompt in test_prompts:
        print(f"\n=== Testing: {prompt} ===")
        
        obs = env.reset(prompt)
        print(f"Initial observation: {obs['spec']}")
        
        # Take some improvement actions
        actions = [
            {'dimensions': '6x4 feet'},
            {'color': 'brown'},
            {'purpose': 'dining'}
        ]
        
        for i, action in enumerate(actions):
            obs, reward, done, info = env.step(action)
            print(f"Step {i+1}: Action={action}, Reward={reward:.3f}, Done={done}")
            print(f"  Score: {info['spec_score']}/10")
            
            if done:
                print("  Environment completed!")
                break
        
        env.render()

if __name__ == "__main__":
    demo_rl_env()