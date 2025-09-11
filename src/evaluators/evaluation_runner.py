"""Evaluation runner for generating evaluation reports."""

import json
import os
from datetime import datetime
from typing import Dict, Any
from .email_evaluator import EmailEvaluator
from .design_evaluator import DesignEvaluator

def run_evaluation(prompt: str, spec: Dict[str, Any], spec_path: str, spec_type: str) -> str:
    """Run evaluation and save report."""
    
    # Select evaluator based on type
    if spec_type == 'email':
        evaluator = EmailEvaluator()
    else:
        evaluator = DesignEvaluator()
    
    # Run evaluation
    evaluation = evaluator.evaluate(prompt, spec)
    
    # Create evaluation report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "prompt": prompt,
        "spec_path": spec_path,
        "critic_feedback": evaluation["critic_feedback"],
        "issues": evaluation["issues"],
        "severity": evaluation["severity"],
        "scores": evaluation["scores"],
        "timestamp": datetime.now().isoformat()
    }
    
    # Save evaluation report
    os.makedirs("evaluations", exist_ok=True)
    eval_filename = f"{spec_type}_eval_{timestamp}.json"
    eval_path = os.path.join("evaluations", eval_filename)
    
    with open(eval_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    return eval_path