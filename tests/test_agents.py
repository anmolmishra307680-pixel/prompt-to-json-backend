import pytest
from prompt_agent import MainAgent
from evaluator import EvaluatorAgent
from rl_agent import RLLoop
from schema import DesignSpec

class TestMainAgent:
    @pytest.fixture
    def agent(self):
        return MainAgent()
    
    def test_generate_spec_office_building(self, agent):
        spec = agent.run("10-story office building")
        assert spec.building_type == "office"
        assert spec.stories == 10
        assert len(spec.materials) > 0
        
    def test_generate_spec_residential(self, agent):
        spec = agent.run("Modern residential apartment")
        assert spec.building_type == "residential"
        # Check that features are populated (balcony may not always be present)
        assert len(spec.features) > 0
        
    def test_error_handling_empty_prompt(self, agent):
        with pytest.raises(ValueError, match="Prompt must be"):
            agent.generate_spec("")
            
    def test_spec_validation(self, agent):
        spec = agent.run("Hospital building")
        assert spec.dimensions.area > 0
        assert spec.timestamp is not None

class TestEvaluatorAgent:
    @pytest.fixture
    def evaluator(self):
        return EvaluatorAgent()
    
    @pytest.fixture
    def sample_spec(self):
        return DesignSpec(
            building_type="office",
            stories=5,
            materials=[{"type": "steel"}],
            dimensions={"length": 30, "width": 25, "height": 17.5, "area": 750},
            features=["elevator", "parking"],
            requirements=["Modern office building"]
        )
    
    def test_evaluate_complete_spec(self, evaluator, sample_spec):
        evaluation = evaluator.run(sample_spec, "Modern office building")
        assert evaluation.score > 0
        assert evaluation.completeness > 0
        assert evaluation.format_validity > 0
        
    def test_evaluate_incomplete_spec(self, evaluator):
        incomplete_spec = DesignSpec(
            building_type="office",
            stories=1,
            materials=[],
            dimensions={"length": 0, "width": 0, "height": 0, "area": 0},
            features=[],
            requirements=[]
        )
        evaluation = evaluator.run(incomplete_spec, "Office")
        assert evaluation.score < 80  # Should score lower for incomplete spec

class TestRLLoop:
    @pytest.fixture
    def rl_agent(self):
        return RLLoop()
    
    def test_rl_training_basic(self, rl_agent):
        result = rl_agent.run("Smart building", 2)
        assert "session_id" in result
        assert "iterations" in result
        assert len(result["iterations"]) == 2
        
    def test_rl_improvement(self, rl_agent):
        result = rl_agent.run("Office building", 3)
        iterations = result["iterations"]
        
        # Check that iterations show improvement
        first_score = iterations[0]["score_after"]
        last_score = iterations[-1]["score_after"]
        assert last_score >= first_score  # Should improve or stay same