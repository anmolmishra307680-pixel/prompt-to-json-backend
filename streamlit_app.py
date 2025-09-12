import streamlit as st
import json
from main_agent import MainAgent
from evaluator_agent import EvaluatorAgent
from rl_loop import RLLoop

st.title("Prompt-to-JSON Agent")
st.write("Convert natural language prompts into structured building specifications")

# Initialize agents
@st.cache_resource
def get_agents():
    return MainAgent(), EvaluatorAgent(), RLLoop()

main_agent, evaluator_agent, rl_loop = get_agents()

# Input
prompt = st.text_area("Enter building description:", placeholder="Modern office building with glass facade")
mode = st.selectbox("Mode:", ["Single Generation", "RL Training", "Advanced RL", "Compare"])

if mode in ["RL Training", "Advanced RL"]:
    iterations = st.slider("Iterations:", 1, 5, 3)
    if mode == "RL Training":
        binary_rewards = st.checkbox("Binary Rewards")
    use_db = st.checkbox("Use Database Storage")

if st.button("Generate"):
    if prompt:
        try:
            if mode == "Single Generation":
                spec = main_agent.generate_spec(prompt)
                evaluation = evaluator_agent.evaluate_spec(spec, prompt)
                
                st.success(f"Score: {evaluation.score}/100")
                st.json(spec.model_dump())
                
            elif mode == "RL Training":
                rl_loop_instance = RLLoop(max_iterations=iterations, binary_rewards=binary_rewards)
                results = rl_loop_instance.run_training_loop(prompt)
                
                st.success(f"Training completed: {len(results['iterations'])} iterations")
                for i, iteration in enumerate(results['iterations']):
                    st.write(f"**Iteration {i+1}**: Score {iteration['evaluation']['score']}")
                    
            elif mode == "Advanced RL":
                from advanced_rl import AdvancedRLEnvironment
                env = AdvancedRLEnvironment()
                result = env.train_episode(prompt, max_steps=iterations)
                
                st.success(f"Advanced RL completed: {result['steps']} steps")
                st.write(f"**Final Score**: {result['final_score']}")
                st.write(f"**Total Reward**: {result['total_reward']:.3f}")
                st.json(result['final_spec'].model_dump())
                

                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a prompt")