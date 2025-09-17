"""Advanced Agent Coordination System"""

import asyncio
from typing import Dict, Any, Optional
from prompt_agent import MainAgent
from evaluator import EvaluatorAgent
from rl_agent import RLLoop
from feedback import FeedbackAgent
from schema import DesignSpec

class AgentCoordinator:
    def __init__(self):
        self.agents = {
            'prompt': MainAgent(),
            'evaluator': EvaluatorAgent(), 
            'rl': RLLoop(),
            'feedback': FeedbackAgent()
        }
        
    async def coordinated_improvement(self, prompt: str, target_score: float = 90.0) -> Dict[str, Any]:
        """Agents work together for optimal results"""
        # Generate initial spec
        spec = self.agents['prompt'].run(prompt)
        
        # Get evaluation feedback
        evaluation = self.agents['evaluator'].run(spec, prompt)
        
        # If score < target, trigger collaborative improvement
        if evaluation.score < target_score:
            print(f"Score {evaluation.score} below target {target_score}, starting collaborative improvement...")
            
            # RL agent uses evaluator feedback
            improved_result = self.agents['rl'].run_with_feedback(
                prompt, evaluation.suggestions
            )
            
            # Re-evaluate improved result
            final_spec = improved_result.get("final_spec", spec.model_dump())
            final_evaluation = self.agents['evaluator'].run(
                DesignSpec(**final_spec), prompt
            )
            
            return {
                "initial_spec": spec.model_dump(),
                "initial_score": evaluation.score,
                "improved_spec": final_spec,
                "final_score": final_evaluation.score,
                "improvement": final_evaluation.score - evaluation.score,
                "iterations": improved_result.get("iterations", []),
                "collaborative": True
            }
            
        return {
            "spec": spec.model_dump(), 
            "evaluation": evaluation.model_dump(),
            "collaborative": False,
            "message": f"Initial score {evaluation.score} meets target"
        }
    
    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            try:
                # Test if agent is responsive
                if hasattr(agent, 'run'):
                    status[name] = "✅ Ready"
                else:
                    status[name] = "❌ No run method"
            except Exception as e:
                status[name] = f"❌ Error: {str(e)}"
        
        return status
    
    def optimize_spec_iteratively(self, prompt: str, max_iterations: int = 5) -> Dict[str, Any]:
        """Iteratively optimize specification until target score reached"""
        current_spec = self.agents['prompt'].run(prompt)
        iteration_history = []
        
        for i in range(max_iterations):
            # Evaluate current spec
            evaluation = self.agents['evaluator'].run(current_spec, prompt)
            
            iteration_data = {
                "iteration": i + 1,
                "spec": current_spec.model_dump(),
                "score": evaluation.score,
                "feedback": evaluation.feedback,
                "suggestions": evaluation.suggestions
            }
            iteration_history.append(iteration_data)
            
            # If score is good enough, stop
            if evaluation.score >= 90.0:
                break
            
            # Improve spec based on feedback
            if evaluation.suggestions:
                current_spec = self.agents['prompt'].improve_spec_with_feedback(
                    current_spec, evaluation.feedback, evaluation.suggestions
                )
        
        return {
            "final_spec": current_spec.model_dump(),
            "final_score": evaluation.score,
            "iterations": iteration_history,
            "total_iterations": len(iteration_history)
        }