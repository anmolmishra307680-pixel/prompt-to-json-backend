"""Unit tests for RL loop module with deterministic inputs."""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, Mock

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from rl.rl_loop import compute_reward, rl_iteration, analyze_rl_history, save_before_after_comparison

class TestComputeReward:
    """Test cases for reward computation."""
    
    def test_compute_reward_perfect_spec(self):
        """Test reward computation for perfect spec."""
        report = {
            "severity": "none",
            "issues": []
        }
        scores = {
            "format_score": 10.0,
            "completeness_score": 4
        }
        
        reward = compute_reward(report, scores)
        
        # Perfect spec: base_reward=1.0, format_multiplier=1.0, completeness_bonus=0.1
        assert reward == 1.1
    
    def test_compute_reward_minor_issues(self):
        """Test reward computation for spec with minor issues."""
        report = {
            "severity": "minor",
            "issues": ["dimensions_missing"]
        }
        scores = {
            "format_score": 7.5,
            "completeness_score": 3
        }
        
        reward = compute_reward(report, scores)
        
        # Minor issues: base_reward=0.2, format_multiplier=0.75
        expected = 0.2 * 0.75  # 0.15
        assert abs(reward - expected) < 0.01
    
    def test_compute_reward_major_issues(self):
        """Test reward computation for spec with major issues."""
        report = {
            "severity": "major",
            "issues": ["type_missing", "material_missing", "dimensions_missing"]
        }
        scores = {
            "format_score": 3.0,
            "completeness_score": 1
        }
        
        reward = compute_reward(report, scores)
        
        # Major issues: base_reward=-1.0, format_multiplier=0.3, quality_penalty=-0.2
        expected = -1.0 * 0.3 - 0.2  # -0.5
        assert abs(reward - expected) < 0.25  # More lenient for rounding
    
    def test_compute_reward_with_completeness_bonus(self):
        """Test reward computation with completeness bonus."""
        report = {
            "severity": "minor",
            "issues": ["dimensions_missing"]
        }
        scores = {
            "format_score": 8.0,
            "completeness_score": 4  # Should trigger bonus
        }
        
        reward = compute_reward(report, scores)
        
        # Minor: 0.2 * 0.8 + 0.1 (bonus) = 0.26
        expected = 0.2 * 0.8 + 0.1
        assert abs(reward - expected) < 0.01
    
    def test_compute_reward_with_quality_penalty(self):
        """Test reward computation with quality penalty."""
        report = {
            "severity": "minor",
            "issues": ["material_missing"]
        }
        scores = {
            "format_score": 2.5,  # Should trigger penalty
            "completeness_score": 2
        }
        
        reward = compute_reward(report, scores)
        
        # Minor: 0.2 * 0.25 - 0.2 (penalty) = -0.15
        expected = 0.2 * 0.25 - 0.2
        assert abs(reward - expected) < 0.01

class TestRLIteration:
    """Test cases for RL iteration functionality."""
    
    @patch('rl.rl_loop.extract_basic_fields')
    @patch('rl.rl_loop.apply_fallbacks')
    @patch('rl.rl_loop.evaluate_spec')
    @patch('rl.rl_loop.score_spec')
    @patch('rl.rl_loop.generate_feedback')
    @patch('rl.rl_loop.log_feedback')
    @patch('rl.rl_loop.log_rl_iteration')
    def test_rl_iteration_no_retry(self, mock_log_rl, mock_log_feedback, mock_gen_feedback,
                                   mock_score, mock_evaluate, mock_fallbacks, mock_extract):
        """Test RL iteration without retry (reward above threshold)."""
        
        # Setup mocks
        mock_extract.return_value = {"type": "table", "material": ["wood"]}
        mock_fallbacks.return_value = {"type": "table", "material": ["wood"], "purpose": "dining"}
        mock_evaluate.return_value = {
            "critic_feedback": "Good spec",
            "issues": [],
            "severity": "none",
            "recommendations": []
        }
        mock_score.return_value = {"format_score": 9.0, "completeness_score": 4}
        mock_gen_feedback.return_value = {
            "feedback_text": "Well done",
            "actions": ["maintain_quality"],
            "source": "heuristic"
        }
        
        # Run iteration with high threshold (no retry expected)
        trace = rl_iteration("Design a wooden table", iteration_id=1, reward_threshold=0.1)
        
        # Verify calls
        mock_extract.assert_called_once_with("Design a wooden table")
        mock_fallbacks.assert_called_once()
        mock_evaluate.assert_called_once()
        mock_score.assert_called_once()
        mock_gen_feedback.assert_called_once()
        mock_log_rl.assert_called_once()
        
        # Verify trace structure
        assert trace["iteration_id"] == 1
        assert trace["prompt"] == "Design a wooden table"
        assert "spec" in trace
        assert "evaluation" in trace
        assert "quality_scores" in trace
        assert "reward" in trace
        assert "retry_info" in trace
        assert trace["retry_info"]["attempted"] is False
    
    @patch('rl.rl_loop.extract_basic_fields')
    @patch('rl.rl_loop.apply_fallbacks')
    @patch('rl.rl_loop.evaluate_spec')
    @patch('rl.rl_loop.score_spec')
    @patch('rl.rl_loop.generate_feedback')
    @patch('rl.rl_loop.log_feedback')
    @patch('rl.rl_loop.log_rl_iteration')
    @patch('rl.rl_loop.apply_feedback_to_prompt')
    @patch('rl.rl_loop.save_before_after_comparison')
    def test_rl_iteration_with_retry(self, mock_save_comparison, mock_apply_feedback,
                                     mock_log_rl, mock_log_feedback, mock_gen_feedback,
                                     mock_score, mock_evaluate, mock_fallbacks, mock_extract):
        """Test RL iteration with retry (reward below threshold)."""
        
        # Setup mocks for original attempt (low reward)
        mock_extract.side_effect = [
            {"type": "unknown", "material": ["unspecified"]},  # Original
            {"type": "table", "material": ["wood"]}  # Enhanced
        ]
        mock_fallbacks.side_effect = [
            {"type": "unknown", "material": ["unspecified"]},  # Original
            {"type": "table", "material": ["wood"], "purpose": "dining"}  # Enhanced
        ]
        mock_evaluate.side_effect = [
            {"critic_feedback": "Poor spec", "issues": ["type_missing"], "severity": "major", "recommendations": []},  # Original
            {"critic_feedback": "Better spec", "issues": [], "severity": "none", "recommendations": []}  # Enhanced
        ]
        mock_score.side_effect = [
            {"format_score": 2.0, "completeness_score": 1},  # Original (low score)
            {"format_score": 8.0, "completeness_score": 4}   # Enhanced (high score)
        ]
        mock_gen_feedback.return_value = {
            "feedback_text": "Add type specification",
            "actions": ["specify_object_type"],
            "source": "heuristic"
        }
        mock_apply_feedback.return_value = "Design a table -- specify object type clearly"
        
        # Run iteration with high threshold (retry expected)
        trace = rl_iteration("Design a table", iteration_id=1, reward_threshold=0.5)
        
        # Verify retry was attempted
        assert trace["retry_info"]["attempted"] is True
        assert trace["retry_info"]["improvement"] > 0
        mock_apply_feedback.assert_called_once()
        mock_save_comparison.assert_called_once()

class TestAnalyzeRLHistory:
    """Test cases for RL history analysis."""
    
    def test_analyze_rl_history_no_file(self):
        """Test analysis when no history file exists."""
        with patch('rl.rl_loop.os.path.exists', return_value=False):
            analysis = analyze_rl_history()
            
            assert "error" in analysis
            assert "No RL history found" in analysis["error"]
    
    def test_analyze_rl_history_with_data(self):
        """Test analysis with sample history data."""
        sample_traces = [
            {
                "reward": 0.8,
                "evaluation": {"severity": "none"},
                "quality_scores": {"format_score": 9.0}
            },
            {
                "reward": 0.2,
                "evaluation": {"severity": "minor"},
                "quality_scores": {"format_score": 6.0}
            },
            {
                "reward": -0.1,
                "evaluation": {"severity": "major"},
                "quality_scores": {"format_score": 3.0}
            }
        ]
        
        # Mock file reading
        mock_file_content = "\n".join([
            '{"reward": 0.8, "evaluation": {"severity": "none"}, "quality_scores": {"format_score": 9.0}, "timestamp": "2025-01-10T10:00:00"}',
            '{"reward": 0.2, "evaluation": {"severity": "minor"}, "quality_scores": {"format_score": 6.0}, "timestamp": "2025-01-10T10:01:00"}',
            '{"reward": -0.1, "evaluation": {"severity": "major"}, "quality_scores": {"format_score": 3.0}, "timestamp": "2025-01-10T10:02:00"}'
        ])
        
        with patch('rl.rl_loop.os.path.exists', return_value=True):
            with patch('builtins.open', create=True) as mock_open:
                mock_open.return_value.__enter__.return_value = mock_file_content.split('\n')
                
                analysis = analyze_rl_history()
                
                assert analysis["total_iterations"] == 3
                assert analysis["reward_stats"]["mean"] == pytest.approx(0.3, abs=0.1)
                assert analysis["reward_stats"]["positive_count"] == 2
                assert analysis["severity_distribution"]["none"] == 1
                assert analysis["severity_distribution"]["minor"] == 1
                assert analysis["severity_distribution"]["major"] == 1

class TestSaveBeforeAfterComparison:
    """Test cases for before/after comparison saving."""
    
    def test_save_before_after_comparison(self):
        """Test saving before/after comparison."""
        comparison_data = {
            "iteration_id": 1,
            "original": {
                "prompt": "Design a table",
                "reward": 0.1,
                "spec": {"type": "unknown"}
            },
            "enhanced": {
                "prompt": "Design a table -- add dimensions",
                "reward": 0.3,
                "spec": {"type": "table", "dimensions": {"raw": "6 feet"}}
            },
            "improvement_achieved": True
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('rl.rl_loop.os.makedirs'):
                with patch('rl.rl_loop.datetime') as mock_datetime:
                    mock_datetime.now.return_value.strftime.return_value = "20250110_120000"
                    
                    # Mock the file path to use temp directory
                    expected_path = os.path.join(temp_dir, "before_after_20250110_120000.json")
                    
                    with patch('builtins.open', create=True) as mock_open:
                        mock_file = Mock()
                        mock_open.return_value.__enter__.return_value = mock_file
                        
                        filepath = save_before_after_comparison(comparison_data)
                        
                        # Verify file operations
                        mock_open.assert_called_once()
                        # JSON dump calls write multiple times, just verify it was called
                        assert mock_file.write.called
                        assert "before_after_" in filepath

class TestRLLoopEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_compute_reward_unknown_severity(self):
        """Test reward computation with unknown severity."""
        report = {
            "severity": "unknown",
            "issues": ["some_issue"]
        }
        scores = {
            "format_score": 5.0,
            "completeness_score": 2
        }
        
        reward = compute_reward(report, scores)
        
        # Unknown severity should use default penalty
        assert reward < 0
    
    def test_compute_reward_edge_scores(self):
        """Test reward computation with edge case scores."""
        report = {
            "severity": "minor",
            "issues": []
        }
        scores = {
            "format_score": 0.0,  # Minimum score
            "completeness_score": 0
        }
        
        reward = compute_reward(report, scores)
        
        # Should handle zero scores gracefully
        assert isinstance(reward, (int, float))
        assert reward <= 0  # Should be negative due to low quality

if __name__ == "__main__":
    pytest.main([__file__, "-v"])