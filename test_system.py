#!/usr/bin/env python3
"""Basic test suite for prompt-to-JSON system"""

import sys
from extractor import PromptExtractor
from main_agent import MainAgent
from evaluator_agent import EvaluatorAgent

def test_extractor():
    """Test prompt extraction functionality"""
    extractor = PromptExtractor()
    
    # Test building type extraction
    assert extractor.extract_building_type("office building") == "office"
    assert extractor.extract_building_type("residential complex") == "residential"
    assert extractor.extract_building_type("random text") == "general"
    assert extractor.extract_building_type("") == "general"
    
    # Test stories extraction
    assert extractor.extract_stories("5-story building") == 5
    assert extractor.extract_stories("two story house") == 2
    assert extractor.extract_stories("single level") == 1
    assert extractor.extract_stories("") == 1
    
    # Test materials extraction
    materials = extractor.extract_materials("steel and glass building")
    material_types = [m.type for m in materials]
    assert "steel" in material_types
    assert "glass" in material_types
    
    print("[PASS] Extractor tests passed")

def test_main_agent():
    """Test main agent functionality"""
    agent = MainAgent()
    
    # Test rule-based generation
    spec = agent.generate_spec("Modern office building with steel frame")
    assert spec.building_type == "office"
    assert len(spec.materials) > 0
    assert spec.stories >= 1
    
    # Test with different prompts
    spec2 = agent.generate_spec("Warehouse facility")
    assert spec2.building_type == "warehouse"
    assert len(spec2.materials) > 0
    
    print("[PASS] MainAgent tests passed")

def test_advanced_rl():
    """Test Advanced RL environment"""
    from advanced_rl import AdvancedRLEnvironment
    
    env = AdvancedRLEnvironment()
    result = env.train_episode("Test office building", max_steps=2)
    
    # Verify result structure
    assert "final_spec" in result
    assert "final_score" in result
    assert "total_reward" in result
    assert "steps" in result
    assert result["steps"] == 2
    
    # Verify final spec is valid
    final_spec = result["final_spec"]
    assert final_spec.building_type in ["office", "general"]
    assert final_spec.stories >= 1
    assert len(final_spec.materials) > 0
    
    print("[PASS] Advanced RL tests passed")
    


def test_evaluator():
    """Test evaluator functionality"""
    agent = MainAgent()
    evaluator = EvaluatorAgent()
    
    # Generate and evaluate a spec
    spec = agent.generate_spec("Perfect office building with steel and glass")
    evaluation = evaluator.evaluate_spec(spec, "Perfect office building")
    
    assert evaluation.score >= 0
    assert evaluation.score <= 100
    assert evaluation.completeness >= 0
    assert evaluation.format_validity >= 0
    
    print("[PASS] Evaluator tests passed")

def test_integration():
    """Test full system integration"""
    from rl_loop import RLLoop
    
    # Test single iteration
    rl_loop = RLLoop(max_iterations=1)
    results = rl_loop.run_training_loop("Test building")
    
    assert len(results["iterations"]) == 1
    assert "dashboard" in results["iterations"][0]
    assert results["final_spec"] is not None
    
    print("[PASS] Integration tests passed")

def test_universal_system():
    """Test universal system functionality"""
    from universal_agent import UniversalAgent
    from universal_evaluator import UniversalEvaluator
    
    agent = UniversalAgent()
    evaluator = UniversalEvaluator()
    
    # Test different prompt types
    test_prompts = [
        "Write an email to the team",
        "Create a task management system", 
        "Design a mobile app",
        "Build an office building"
    ]
    
    for prompt in test_prompts:
        spec = agent.generate_spec(prompt)
        evaluation = evaluator.evaluate_spec(spec, prompt)
        
        assert spec.prompt_type in ['email', 'task', 'software', 'building', 'product', 'general']
        assert len(spec.components) > 0
        assert evaluation.score >= 0
        assert evaluation.score <= 100
    
    print("[PASS] Universal system tests passed")

def run_all_tests():
    """Run all tests"""
    print("Running prompt-to-JSON system tests...\n")
    
    try:
        test_extractor()
        test_main_agent()
        test_advanced_rl()
        test_evaluator()
        test_universal_system()
        test_integration()
        
        print("\n[SUCCESS] All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)