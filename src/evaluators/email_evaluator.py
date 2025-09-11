"""Email evaluator for email specifications."""

import re
from typing import Dict, Any, List
from .base_evaluator import BaseEvaluator

class EmailEvaluator(BaseEvaluator):
    """Evaluator for email specifications."""
    
    def evaluate(self, prompt: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate email specification."""
        issues = []
        feedback_parts = []
        scores = {}
        
        # Check subject
        subject_score = self._check_subject(spec, issues, feedback_parts)
        scores["subject_score"] = subject_score
        
        # Check body content
        body_score = self._check_body(prompt, spec, issues, feedback_parts)
        scores["body_score"] = body_score
        
        # Check tone consistency
        tone_score = self._check_tone(prompt, spec, issues, feedback_parts)
        scores["tone_score"] = tone_score
        
        # Check recipient
        recipient_score = self._check_recipient(spec, issues, feedback_parts)
        scores["recipient_score"] = recipient_score
        
        # Overall scores
        scores["format_score"] = (subject_score + recipient_score) / 2 * 10
        scores["completeness_score"] = min(4, len([s for s in scores.values() if s > 0.7]))
        
        # Determine severity
        severity = self._determine_severity(issues)
        
        # Generate feedback
        if not feedback_parts:
            feedback_parts.append("Email specification looks complete")
        
        critic_feedback = "; ".join(feedback_parts) + "."
        
        return {
            "critic_feedback": critic_feedback,
            "issues": issues,
            "severity": severity,
            "scores": scores
        }
    
    def _check_subject(self, spec: Dict[str, Any], issues: List[str], feedback: List[str]) -> float:
        """Check subject line quality."""
        subject = spec.get("subject", "")
        
        if not subject:
            issues.append("Missing email subject")
            return 0.0
        
        if len(subject) < 3:
            issues.append("Subject too short")
            feedback.append("subject very brief")
            return 0.3
        
        if len(subject) > 100:
            issues.append("Subject too long")
            feedback.append("subject quite long")
            return 0.7
        
        feedback.append("subject concise")
        return 1.0
    
    def _check_body(self, prompt: str, spec: Dict[str, Any], issues: List[str], feedback: List[str]) -> float:
        """Check body content quality."""
        body = spec.get("body", "")
        
        if not body:
            issues.append("Missing email body")
            return 0.0
        
        if len(body) < 10:
            issues.append("Body too short")
            return 0.3
        
        # Check for dates mentioned in prompt
        date_patterns = [
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}',
            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2}',
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'oct\s*1', r'october\s*1'
        ]
        
        prompt_has_date = any(re.search(pattern, prompt.lower()) for pattern in date_patterns)
        body_has_date = any(re.search(pattern, body.lower()) for pattern in date_patterns)
        
        if prompt_has_date and body_has_date:
            feedback.append("body includes relevant date")
            return 1.0
        elif prompt_has_date and not body_has_date:
            issues.append("Body missing date mentioned in prompt")
            return 0.6
        
        feedback.append("body content appropriate")
        return 0.8
    
    def _check_tone(self, prompt: str, spec: Dict[str, Any], issues: List[str], feedback: List[str]) -> float:
        """Check tone consistency."""
        tone = spec.get("tone", "").lower()
        prompt_lower = prompt.lower()
        
        # Detect expected tone from prompt
        if any(word in prompt_lower for word in ["formal", "professional", "business"]):
            expected_tone = "formal"
        elif any(word in prompt_lower for word in ["casual", "friendly", "informal"]):
            expected_tone = "casual"
        elif any(word in prompt_lower for word in ["urgent", "asap", "immediately"]):
            expected_tone = "urgent"
        else:
            expected_tone = "professional"  # default
        
        if not tone:
            issues.append("Missing tone specification")
            return 0.5
        
        if tone == expected_tone or (expected_tone == "professional" and tone == "formal"):
            feedback.append("tone consistent with prompt")
            return 1.0
        
        issues.append(f"Tone mismatch: expected {expected_tone}, got {tone}")
        return 0.4
    
    def _check_recipient(self, spec: Dict[str, Any], issues: List[str], feedback: List[str]) -> float:
        """Check recipient field."""
        to = spec.get("to", "")
        
        if not to:
            issues.append("Missing recipient")
            return 0.0
        
        # Check if it's a valid email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, to):
            feedback.append("recipient email valid")
            return 1.0
        
        # Check if it's a reasonable recipient description
        if len(to) > 3:
            feedback.append("recipient specified")
            return 0.8
        
        issues.append("Invalid recipient format")
        return 0.3
    
    def _determine_severity(self, issues: List[str]) -> str:
        """Determine overall severity based on issues."""
        if not issues:
            return "none"
        
        critical_keywords = ["missing", "invalid", "mismatch"]
        minor_keywords = ["short", "long", "brief"]
        
        has_critical = any(any(keyword in issue.lower() for keyword in critical_keywords) for issue in issues)
        has_minor = any(any(keyword in issue.lower() for keyword in minor_keywords) for issue in issues)
        
        if has_critical:
            return "major"
        elif has_minor:
            return "minor"
        
        return "moderate"