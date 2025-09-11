"""Email generator using rule-based extraction."""

import re
from typing import Dict, Any
from .base_generator import BaseGenerator

class EmailGenerator(BaseGenerator):
    """Generator for email specifications."""
    
    def generate_spec(self, prompt: str) -> Dict[str, Any]:
        """Generate email specification from prompt."""
        extracted = self._extract_email_fields(prompt)
        
        spec = {
            "type": "email",
            "to": extracted.get('to') or 'recipient@example.com',
            "subject": extracted.get('subject') or 'Subject',
            "body": extracted.get('body') or self._generate_body(prompt, extracted),
            "tone": extracted.get('tone') or 'professional'
        }
        
        return {
            "spec": spec,
            "llm_output": f"Generated email to {spec['to']} about {spec['subject']}",
            "method": "rules"
        }
    
    def _extract_email_fields(self, prompt: str) -> Dict[str, Any]:
        """Extract email fields using patterns."""
        result = {}
        
        # Extract recipient
        to_patterns = [
            r'to\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'send\s+(?:to\s+)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'email\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'to\s+([\w\s]+?)(?:\s+about|\s+regarding|$)',
        ]
        
        for pattern in to_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                result['to'] = match.group(1).strip()
                break
        
        # Extract subject
        subject_patterns = [
            r'about\s+([^.!?]+)',
            r'regarding\s+([^.!?]+)',
            r'subject[:\s]+([^.!?]+)',
            r'concerning\s+([^.!?]+)'
        ]
        
        for pattern in subject_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                result['subject'] = match.group(1).strip()
                break
        
        # Extract tone
        tone_patterns = {
            'formal': ['formal', 'professional', 'business'],
            'casual': ['casual', 'informal', 'friendly'],
            'urgent': ['urgent', 'asap', 'immediately'],
            'polite': ['polite', 'courteous', 'respectful']
        }
        
        for tone, keywords in tone_patterns.items():
            if any(keyword in prompt.lower() for keyword in keywords):
                result['tone'] = tone
                break
        
        return result
    
    def _generate_body(self, prompt: str, extracted: Dict[str, Any]) -> str:
        """Generate email body based on prompt and extracted info."""
        subject = extracted.get('subject', 'update')
        tone = extracted.get('tone', 'professional')
        
        if tone == 'formal':
            greeting = "Dear recipient,"
            closing = "Best regards"
        elif tone == 'casual':
            greeting = "Hi there!"
            closing = "Thanks"
        else:
            greeting = "Hello,"
            closing = "Best regards"
        
        # Generate simple body based on subject
        if 'meeting' in subject.lower():
            body_content = f"I wanted to reach out regarding the {subject.lower()}. Please let me know your availability."
        elif 'project' in subject.lower():
            body_content = f"I'm writing to update you on the {subject.lower()}. We're making good progress."
        elif 'launch' in subject.lower():
            body_content = f"We are excited to announce the {subject.lower()}. Please prepare the necessary materials."
        else:
            body_content = f"I wanted to inform you about {subject.lower()}. Please review and let me know if you have any questions."
        
        return f"{greeting}\\n\\n{body_content}\\n\\n{closing}"