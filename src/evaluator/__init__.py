"""Evaluator package for design specification analysis."""

from .criteria import KNOWN_MATERIALS, ALL_MATERIALS, TYPE_RULES
from .report import evaluate_spec, save_report, generate_human_report

__all__ = [
    'KNOWN_MATERIALS',
    'ALL_MATERIALS', 
    'TYPE_RULES',
    'evaluate_spec',
    'save_report',
    'generate_human_report'
]