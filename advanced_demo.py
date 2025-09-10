"""Advanced demo showcasing improved extraction and evaluation capabilities."""

from src.extractor import extract_basic_fields
from evaluator_agent import evaluate_spec
from data_scorer import score_spec
from utils import apply_fallbacks

def test_complex_prompts():
    """Test extraction on challenging prompts that previously failed."""
    
    complex_prompts = [
        "Design a lightweight 2-meter carbon fiber drone frame for professional aerial cinematography",
        "Create a sustainable 3-floor library building with solar panels and recycled materials", 
        "Build a compact stainless steel surgical instrument sterilization cabinet for operating rooms",
        "Construct a massive concrete foundation platform 50x30 meters for industrial equipment",
        "Design a medieval oak throne chair with intricate gold leaf decorative patterns"
    ]
    
    print("=== Advanced Extraction & Evaluation Demo ===\n")
    
    total_score = 0
    total_fields = 0
    
    for i, prompt in enumerate(complex_prompts, 1):
        print(f"Test {i}: {prompt}")
        print("-" * 80)
        
        # Extract fields
        extracted = extract_basic_fields(prompt)
        print(f"Raw extraction: {extracted}")
        
        # Apply fallbacks
        spec_data = apply_fallbacks(extracted)
        print(f"With fallbacks: {spec_data}")
        
        # Evaluate
        evaluation = evaluate_spec(prompt, spec_data)
        print(f"Evaluation: {evaluation['severity']} - {len(evaluation['issues'])} issues")
        print(f"Feedback: {evaluation['critic_feedback']}")
        
        # Score
        scoring = score_spec(spec_data, prompt)
        print(f"Score: {scoring['format_score']}/10")
        
        # Calculate metrics
        extracted_fields = sum(1 for v in extracted.values() if v is not None)
        total_fields += extracted_fields
        total_score += scoring['format_score']
        
        print(f"Extraction success: {extracted_fields}/5 fields ({extracted_fields*20}%)")
        print("=" * 80)
        print()
    
    # Summary
    avg_extraction = total_fields / (len(complex_prompts) * 5) * 100
    avg_score = total_score / len(complex_prompts)
    
    print("=== SUMMARY ===")
    print(f"Average extraction rate: {avg_extraction:.1f}%")
    print(f"Average quality score: {avg_score:.1f}/10")
    print(f"Tests completed: {len(complex_prompts)}")

if __name__ == "__main__":
    test_complex_prompts()