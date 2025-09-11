#!/usr/bin/env python3
"""
Streamlit web app for prompt-to-JSON agent demo.
Type-aware interface with classification and examples.
"""

import streamlit as st
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.classifier import classify_prompt
    from src.schema_registry import get_schema_for_type, get_available_types
    from src.generators import DesignGenerator, EmailGenerator
    from src.evaluators.evaluation_runner import run_evaluation
    from src.data_scorer import score_spec
    from src.schema_registry import validate_spec, save_valid_spec
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

def main():
    st.set_page_config(
        page_title="Prompt-to-JSON Agent",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Prompt-to-JSON Agent")
    st.markdown("**Type-aware** prompt processing with automatic classification and validation")
    
    # Initialize session state
    if 'detected_type' not in st.session_state:
        st.session_state.detected_type = None
    if 'classification_result' not in st.session_state:
        st.session_state.classification_result = None
    
    # Main input
    st.header("📝 Input Prompt")
    prompt = st.text_area(
        "Enter your prompt:",
        placeholder="Write an email to marketing team about project launch OR Create a wooden dining table",
        height=100,
        key="prompt_input"
    )
    
    # Auto-classify on input change
    if prompt.strip() and (not st.session_state.classification_result or 
                          st.session_state.classification_result.get('prompt') != prompt):
        with st.spinner("Classifying prompt type..."):
            classification = classify_prompt(prompt)
            st.session_state.classification_result = {**classification, 'prompt': prompt}
            st.session_state.detected_type = classification['type']
    
    # Type detection and override
    if st.session_state.classification_result:
        st.header("🎯 Prompt Classification")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            classification = st.session_state.classification_result
            confidence_color = "🟢" if classification['confidence'] > 0.8 else "🟡" if classification['confidence'] > 0.5 else "🔴"
            st.write(f"**Detected Type:** {classification['type'].title()} {confidence_color}")
            st.write(f"**Confidence:** {classification['confidence']:.1%}")
            st.write(f"**Reason:** {classification['reason']}")
        
        with col2:
            # Type override dropdown
            available_types = get_available_types()
            override_type = st.selectbox(
                "Override type:",
                options=available_types,
                index=available_types.index(st.session_state.detected_type),
                key="type_override"
            )
            if override_type != st.session_state.detected_type:
                st.session_state.detected_type = override_type
                st.info(f"Type overridden to: {override_type}")
    
    # Show schema info and examples for selected type
    if st.session_state.detected_type:
        schema_info = get_schema_for_type(st.session_state.detected_type)
        
        st.header(f"📋 {st.session_state.detected_type.title()} Specification")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("**Help:**")
            st.info(schema_info['help'])
            
            # Email-specific quick fill
            if st.session_state.detected_type == 'email':
                st.write("**Quick Fill (Optional):**")
                quick_to = st.text_input("To:", placeholder="recipient@example.com")
                quick_subject = st.text_input("Subject:", placeholder="Meeting reminder")
        
        with col2:
            st.write("**Example Prompts:**")
            for i, example in enumerate(schema_info['examples']):
                if st.button(f"📝 {example}", key=f"example_{i}"):
                    st.session_state.prompt_input = example
                    st.rerun()
    
    # Action buttons
    if prompt.strip() and st.session_state.detected_type:
        col1, col2 = st.columns(2)
        
        with col1:
            run_pipeline_btn = st.button("🚀 Run Pipeline", type="primary")
        
        with col2:
            auto_correct_btn = st.button("🔧 Auto-Correct & Retry")
        
        if run_pipeline_btn or auto_correct_btn:
            with st.spinner("Processing prompt..."):
                try:
                    # Generate specification
                    if st.session_state.detected_type == 'email':
                        generator = EmailGenerator()
                    else:
                        generator = DesignGenerator()
                    
                    gen_result = generator.generate_spec(prompt)
                    spec = gen_result['spec']
                    
                    # Validate specification
                    validation = validate_spec(spec, st.session_state.detected_type)
                    
                    # Save if valid
                    if validation['valid']:
                        spec_path = save_valid_spec(spec, st.session_state.detected_type)
                    else:
                        spec_path = "validation_failed"
                    
                    # Run evaluation
                    eval_path = run_evaluation(prompt, spec, spec_path, st.session_state.detected_type)
                    
                    # Calculate scores
                    scores = score_spec(spec, prompt, st.session_state.detected_type)
                    
                    # Store results in session state
                    st.session_state.results = {
                        'spec': spec,
                        'validation': validation,
                        'spec_path': spec_path,
                        'eval_path': eval_path,
                        'scores': scores,
                        'generation': gen_result
                    }
                    
                    st.success("✅ Pipeline completed successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Pipeline failed: {str(e)}")
                    st.exception(e)
    
    # Display results if available
    if 'results' in st.session_state:
        results = st.session_state.results
        
        st.header("📊 Results")
        
        # Create tabs for different outputs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Specification", "🔍 Evaluation", "📊 Scores", "🎯 Summary"])
        
        with tab1:
            st.subheader(f"{st.session_state.detected_type.title()} Specification")
            
            # Validation status
            if results['validation']['valid']:
                st.success("✅ Specification is valid")
            else:
                st.error("❌ Specification validation failed")
                for error in results['validation']['errors']:
                    st.write(f"• {error}")
            
            # Display spec based on type
            if st.session_state.detected_type == 'email':
                spec = results['spec']
                st.write(f"**To:** {spec.get('to', 'N/A')}")
                st.write(f"**Subject:** {spec.get('subject', 'N/A')}")
                st.write(f"**Tone:** {spec.get('tone', 'N/A')}")
                st.write("**Body:**")
                st.text_area("Email body:", value=spec.get('body', ''), height=150, disabled=True)
            else:
                st.json(results['spec'])
            
            # Download button
            spec_json = json.dumps(results['spec'], indent=2)
            st.download_button(
                label="📥 Download Specification",
                data=spec_json,
                file_name=f"{st.session_state.detected_type}_spec.json",
                mime="application/json"
            )
        
        with tab2:
            st.subheader("Evaluation Results")
            
            # Load evaluation from file
            try:
                with open(results['eval_path'], 'r') as f:
                    eval_data = json.load(f)
                
                # Severity indicator
                severity = eval_data["severity"]
                severity_icons = {"none": "✅", "minor": "⚠️", "moderate": "🔶", "major": "❌"}
                st.write(f"**Severity:** {severity_icons.get(severity, '❓')} {severity.upper()}")
                
                # Feedback
                st.write("**Critic Feedback:**")
                st.info(eval_data["critic_feedback"])
                
                # Issues
                if eval_data["issues"]:
                    st.write("**Issues Found:**")
                    for issue in eval_data["issues"]:
                        st.write(f"• {issue}")
                else:
                    st.success("No issues found!")
                
            except Exception as e:
                st.error(f"Could not load evaluation: {e}")
        
        with tab3:
            st.subheader("Quality Scores")
            scores = results['scores']
            
            # Type-specific score display
            if st.session_state.detected_type == 'email':
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Overall Quality", f"{scores.get('format_score', 0):.1f}/10")
                    st.metric("Subject Score", f"{scores.get('subject_score', 0):.1f}/2.5")
                with col2:
                    st.metric("Body Score", f"{scores.get('body_score', 0):.1f}/2.5")
                    st.metric("Recipient Score", f"{scores.get('recipient_score', 0):.1f}/2.5")
                    st.metric("Tone Score", f"{scores.get('tone_score', 0):.1f}/2.5")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Overall Quality", f"{scores.get('format_score', 0):.1f}/10")
                    st.metric("Completeness", f"{scores.get('completeness_score', 0)}/4")
                with col2:
                    st.metric("Material Realism", f"{scores.get('material_realism_score', 0)}/3")
                    st.metric("Dimension Validity", f"{scores.get('dimension_validity_score', 0)}/2")
            
            # Score visualization
            score_keys = [k for k in scores.keys() if k.endswith('_score') and k != 'format_score']
            if score_keys:
                chart_data = {k.replace('_score', '').title(): scores[k] for k in score_keys}
                st.bar_chart(chart_data)
        
        with tab4:
            st.subheader("Pipeline Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Input:**")
                st.write(f"**Prompt:** {prompt}")
                st.write(f"**Detected Type:** {st.session_state.detected_type}")
                st.write(f"**Method:** {results['generation']['method']}")
            
            with col2:
                st.write("**Output:**")
                st.write(f"**Validation:** {'✅ Passed' if results['validation']['valid'] else '❌ Failed'}")
                st.write(f"**Quality Score:** {results['scores'].get('format_score', 0):.1f}/10")
                st.write(f"**Files Generated:** 2")
            
            # File paths
            st.write("**Generated Files:**")
            st.code(f"Specification: {results['spec_path']}")
            st.code(f"Evaluation: {results['eval_path']}")
    
    # Footer
    st.markdown("---")
    st.markdown("🤖 **Prompt-to-JSON Agent v2.0** • Type-aware processing with auto-classification")

if __name__ == "__main__":
    main()