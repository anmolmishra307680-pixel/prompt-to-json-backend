"""Optional Gymnasium RL Environment for advanced RL training

WARNING: This module requires external dependencies:
- gymnasium>=0.29.0
- numpy>=1.21.0

Install with: pip install gymnasium numpy
"""

try:
    import gymnasium as gym
    import numpy as np
    from gymnasium import spaces
    GYMNASIUM_AVAILABLE = True
except ImportError:
    GYMNASIUM_AVAILABLE = False
    print("[WARNING] Gymnasium not available. Install with: pip install gymnasium numpy")

from main_agent import MainAgent
from evaluator_agent import EvaluatorAgent

class PromptToJSONEnv:
    """Gymnasium environment for prompt-to-JSON RL training"""
    
    def __init__(self, prompt: str):
        if not GYMNASIUM_AVAILABLE:
            raise ImportError("Gymnasium not installed. Use: pip install gymnasium")
            
        self.prompt = prompt
        self.main_agent = MainAgent()
        self.evaluator_agent = EvaluatorAgent()
        
        # Action space: discrete actions for spec modifications
        self.action_space = spaces.Discrete(5)  # 0-4 different improvement actions
        
        # Observation space: simplified spec representation
        self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)
        
        self.current_spec = None
        self.step_count = 0
        self.max_steps = 10
    
    def reset(self, seed=None):
        """Reset environment to initial state"""
        self.current_spec = self.main_agent.generate_spec(self.prompt)
        self.step_count = 0
        return self._get_observation(), {}
    
    def step(self, action):
        """Take action and return new state"""
        self.step_count += 1
        
        # Apply action to modify spec
        self.current_spec = self._apply_action(action)
        
        # Evaluate current spec
        evaluation = self.evaluator_agent.evaluate_spec(self.current_spec, self.prompt)
        
        # Calculate reward
        reward = evaluation.score / 100.0
        
        # Check if done
        done = self.step_count >= self.max_steps or evaluation.score >= 95
        
        return self._get_observation(), reward, done, False, {"evaluation": evaluation}
    
    def _get_observation(self):
        """Convert spec to observation vector"""
        if not self.current_spec:
            return np.zeros(4, dtype=np.float32)
            
        return np.array([
            len(self.current_spec.materials),
            self.current_spec.stories,
            len(self.current_spec.features),
            self.current_spec.dimensions.area or 0
        ], dtype=np.float32)
    
    def _apply_action(self, action):
        """Apply action to modify specification"""
        # Simple action mapping
        if action == 0:  # Add material
            return self.main_agent.add_material(self.current_spec, "concrete")
        elif action == 1:  # Add feature
            return self.main_agent.add_feature(self.current_spec, "elevator")
        elif action == 2:  # Increase stories
            return self.main_agent.modify_stories(self.current_spec, self.current_spec.stories + 1)
        elif action == 3:  # Improve dimensions
            return self.main_agent.improve_dimensions(self.current_spec)
        else:  # No change
            return self.current_spec

def create_gym_environment(prompt: str):
    """Factory function to create Gymnasium environment"""
    if not GYMNASIUM_AVAILABLE:
        return None
    return PromptToJSONEnv(prompt)