#!/usr/bin/env python3
"""
Streamlit web app for prompt-to-JSON agent demo.
Provides interactive interface for testing the pipeline.
"""

import streamlit as st
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.main import run_pipeline
    from src.extractor import extract_basic_fields
    from utils import apply_fallbacks
    from data_scorer import score_spec
    from evaluator_agent import evaluate_spec
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

def main():
    st.set_page_config(
        page_title="Prompt-to-JSON Agent",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 Prompt-to-JSON Agent Demo")
    st.markdown("Convert natural language prompts into structured JSON specifications")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    save_report = st.sidebar.checkbox("Save evaluation report", value=False)
    run_rl = st.sidebar.checkbox("Compute RL reward", value=True)
    
    # Main input
    st.header("Input Prompt")
    prompt = st.text_area(
        "Enter your design prompt:",
        placeholder="Create a wooden dining table with glass top and steel legs",
        height=100
    )
    
    # Example prompts
    st.subheader("Example Prompts")
    examples = [
        "Create a wooden dining table with glass top",
        "Design a modern steel office chair with wheels",
        "Build a 3-floor concrete library with reading rooms",
        "Make a red leather sofa for the living room",
        "Design an eco-friendly bamboo bookshelf"
    ]
    
    col1, col2, col3 = st.columns(3)
    for i, example in enumerate(examples):
        col = [col1, col2, col3][i % 3]
        if col.button(f"Example {i+1}", key=f"ex_{i}"):
            prompt = example
            st.rerun()
    
    # Process button
    if st.button("🚀 Run Pipeline", type="primary", disabled=not prompt.strip()):
        if not prompt.strip():
            st.error("Please enter a prompt")
            return
        
        with st.spinner("Processing prompt through pipeline..."):
            try:
                # Run the pipeline
                result = run_pipeline(prompt, save_report=save_report, run_rl=run_rl)
                
                # Display results
                st.success("Pipeline completed successfully!")
                
                # Create tabs for different outputs
                tab1, tab2, tab3, tab4 = st.tabs(["📋 Specification", "🔍 Evaluation", "📊 Scores", "🎯 Summary"])
                
                with tab1:
                    st.subheader("Generated JSON Specification")
                    st.json(result["spec_data"])
                    
                    # Download button
                    spec_json = json.dumps(result["spec_data"], indent=2)
                    st.download_button(
                        label="📥 Download Spec JSON",
                        data=spec_json,
                        file_name=f"spec_{prompt[:20].replace(' ', '_')}.json",
                        mime="application/json"
                    )
                
                with tab2:
                    st.subheader("Evaluation Results")
                    eval_data = result["evaluation"]
                    
                    # Severity indicator
                    severity = eval_data["severity"]
                    if severity == "none":
                        st.success(f"✅ Severity: {severity.upper()}")
                    elif severity == "minor":
                        st.warning(f"⚠️ Severity: {severity.upper()}")
                    else:
                        st.error(f"❌ Severity: {severity.upper()}")
                    
                    # Feedback
                    st.write("**Critic Feedback:**")
                    st.write(eval_data["critic_feedback"])
                    
                    # Issues
                    if eval_data["issues"]:
                        st.write("**Issues Found:**")
                        for issue in eval_data["issues"]:
                            st.write(f"• {issue.replace('_', ' ').title()}")
                    else:
                        st.success("No issues found!")
                
                with tab3:
                    st.subheader("Quality Scores")
                    scores = result["scores"]
                    
                    # Score metrics
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Overall Quality", f"{scores['format_score']}/10")
                        st.metric("Completeness", f"{scores['completeness_score']}/4")
                    
                    with col2:
                        st.metric("Material Realism", f"{scores['material_realism_score']}/3")
                        st.metric("Dimension Validity", f"{scores['dimension_validity_score']}/2")
                        st.metric("Type Match", f"{scores['type_match_score']}/1")
                    
                    # Score breakdown
                    st.write("**Score Breakdown:**")
                    score_data = {
                        "Completeness": scores['completeness_score'],
                        "Material Realism": scores['material_realism_score'],
                        "Dimension Validity": scores['dimension_validity_score'],
                        "Type Match": scores['type_match_score']
                    }
                    st.bar_chart(score_data)
                
                with tab4:
                    st.subheader("Pipeline Summary")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Input:**")
                        st.write(f"Prompt: {prompt}")
                        st.write(f"Validation: {'✅ Passed' if result['validated'] else '❌ Failed'}")
                    
                    with col2:
                        st.write("**Output:**")
                        st.write(f"Issues: {len(result['evaluation']['issues'])}")
                        st.write(f"Quality: {result['scores']['format_score']}/10")
                        if run_rl:
                            st.write(f"RL Reward: {result['reward']:.3f}")
                    
                    # File paths
                    st.write("**Generated Files:**")
                    st.code(f"Spec: {result['spec_path']}")
                    st.code(f"Evaluation: {result['eval_path']}")
                
            except Exception as e:
                st.error(f"Pipeline failed: {str(e)}")
                st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit • Prompt-to-JSON Agent v1.0")

if __name__ == "__main__":
    main()