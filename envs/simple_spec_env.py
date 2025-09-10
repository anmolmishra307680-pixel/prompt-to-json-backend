import numpy as np
from typing import Tuple, Dict, Any

class SimpleSpecEnv:
    """Simple gymnasium-style environment for furniture spec generation."""
    
    def __init__(self):
        self.state = None
        self.current_prompt = ""
        self.step_count = 0
        self.max_steps = 10
    
    def reset(self) -> Dict[str, Any]:
        """Reset environment and return initial state."""
        self.state = {
            "prompt_embedding": np.random.rand(10),  # Dummy embedding
            "spec_fields": np.zeros(5),  # type, material, color, dimensions, purpose
            "step": 0
        }
        self.step_count = 0
        return self.state
    
    def step(self, action: Dict[str, str]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """Take action and return (state, reward, done, info)."""
        self.step_count += 1
        
        # Update state based on action
        if action.get('type'):
            self.state["spec_fields"][0] = 1.0
        if action.get('material'):
            self.state["spec_fields"][1] = 1.0
        if action.get('color'):
            self.state["spec_fields"][2] = 1.0
        if action.get('dimensions'):
            self.state["spec_fields"][3] = 1.0
        if action.get('purpose'):
            self.state["spec_fields"][4] = 1.0
        
        self.state["step"] = self.step_count
        
        # Compute dummy reward
        completeness = np.sum(self.state["spec_fields"]) / 5.0
        reward = completeness - 0.1 * self.step_count  # Reward completeness, penalize steps
        
        # Check if done
        done = self.step_count >= self.max_steps or completeness == 1.0
        
        info = {
            "completeness": completeness,
            "fields_filled": int(np.sum(self.state["spec_fields"]))
        }
        
        return self.state, reward, done, info
    
    def render(self):
        """Render current state."""
        print(f"Step: {self.step_count}")
        print(f"Fields filled: {np.sum(self.state['spec_fields'])}/5")
        print(f"Completeness: {np.sum(self.state['spec_fields'])/5:.2f}")

if __name__ == "__main__":
    # Test environment
    env = SimpleSpecEnv()
    state = env.reset()
    
    print("Testing Simple Spec Environment")
    print("Initial state:", state)
    
    # Take some dummy actions
    actions = [
        {"type": "table"},
        {"material": "wood"},
        {"color": "brown", "dimensions": "6 feet"},
        {"purpose": "dining"}
    ]
    
    for i, action in enumerate(actions):
        state, reward, done, info = env.step(action)
        print(f"\nStep {i+1}: Action={action}")
        print(f"Reward: {reward:.2f}, Done: {done}")
        print(f"Info: {info}")
        env.render()
        
        if done:
            break