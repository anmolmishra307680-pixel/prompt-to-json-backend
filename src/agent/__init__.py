"""Agent module for automated spec improvement and editing."""

from .editor import apply_feedback_to_prompt, apply_direct_spec_edits, generate_improvement_suggestions

__all__ = [
    'apply_feedback_to_prompt',
    'apply_direct_spec_edits', 
    'generate_improvement_suggestions'
]