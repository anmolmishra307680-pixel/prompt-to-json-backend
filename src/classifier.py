"""Prompt type classifier with rule-based detection and LLM fallback."""

import re
from typing import Dict, List, Tuple
import json

# Rule-based classification patterns
CLASSIFICATION_RULES = {
    "email": {
        "keywords": ["email", "send", "write", "compose", "message", "subject", "recipient", "cc", "bcc"],
        "patterns": [
            r"\bemail\b",
            r"\bsend\b.*\bto\b",
            r"\bwrite\b.*\bemail\b",
            r"\bcompose\b.*\bmessage\b",
            r"\bsubject\b.*\bline\b"
        ],
        "phrases": ["write an email", "send a message", "compose email", "email to"]
    },
    "design": {
        "keywords": ["create", "design", "build", "make", "construct", "table", "chair", "sofa", "desk", "cabinet", "shelf"],
        "patterns": [
            r"\b(create|design|build|make)\b.*\b(table|chair|sofa|desk|cabinet|shelf|furniture)\b",
            r"\b(wooden|steel|metal|glass|leather|fabric)\b.*\b(table|chair|sofa|desk)\b",
            r"\b(dining|office|living|bedroom)\b.*\b(table|chair|sofa|desk)\b"
        ],
        "phrases": ["create a", "design a", "build a", "make a"]
    },
    "code": {
        "keywords": ["code", "function", "class", "variable", "python", "javascript", "programming", "script"],
        "patterns": [
            r"\bwrite\b.*\b(code|function|script)\b",
            r"\b(python|javascript|java|c\+\+)\b.*\b(code|function)\b",
            r"\bdef\b|\bclass\b|\bfunction\b"
        ],
        "phrases": ["write code", "create function", "implement class"]
    },
    "document": {
        "keywords": ["document", "report", "letter", "memo", "proposal", "summary", "article"],
        "patterns": [
            r"\bwrite\b.*\b(document|report|letter|memo)\b",
            r"\bcreate\b.*\b(document|report|summary)\b"
        ],
        "phrases": ["write a document", "create report", "draft letter"]
    }
}

def classify_prompt_rules(prompt: str) -> Tuple[str, float, str]:
    """Rule-based prompt classification."""
    prompt_lower = prompt.lower()
    scores = {}
    reasons = {}
    
    for prompt_type, rules in CLASSIFICATION_RULES.items():
        score = 0
        matched_items = []
        
        # Check keywords
        for keyword in rules["keywords"]:
            if keyword in prompt_lower:
                score += 1
                matched_items.append(f"keyword '{keyword}'")
        
        # Check regex patterns
        for pattern in rules["patterns"]:
            if re.search(pattern, prompt_lower):
                score += 2  # Patterns are more specific
                matched_items.append(f"pattern match")
        
        # Check phrases
        for phrase in rules["phrases"]:
            if phrase in prompt_lower:
                score += 1.5
                matched_items.append(f"phrase '{phrase}'")
        
        if score > 0:
            scores[prompt_type] = score
            reasons[prompt_type] = f"matched: {', '.join(matched_items[:3])}"
    
    if not scores:
        return "unknown", 0.0, "no rule matches"
    
    # Get best match
    best_type = max(scores.keys(), key=lambda k: scores[k])
    max_score = scores[best_type]
    
    # Normalize confidence (rough heuristic)
    confidence = min(max_score / 5.0, 1.0)  # Scale to 0-1
    
    return best_type, confidence, reasons[best_type]

def classify_prompt_llm(prompt: str) -> Tuple[str, float, str]:
    """LLM-based prompt classification fallback."""
    try:
        from src.llama_prompt import generate_raw_response
        
        classification_prompt = f"""Classify this prompt into one of these categories:
- email: writing emails, messages, communications
- design: creating furniture, objects, physical items
- code: programming, writing code, functions
- document: reports, letters, articles, documents
- unknown: anything else

Prompt: "{prompt}"

Respond with only: category_name"""
        
        response = generate_raw_response(classification_prompt, max_length=20)
        response_clean = response.strip().lower()
        
        # Extract classification from response
        valid_types = ["email", "design", "code", "document", "unknown"]
        for valid_type in valid_types:
            if valid_type in response_clean:
                return valid_type, 0.7, f"LLM classified as {valid_type}"
        
        return "unknown", 0.3, "LLM response unclear"
        
    except Exception as e:
        return "unknown", 0.0, f"LLM fallback failed: {str(e)}"

def classify_prompt(prompt: str) -> Dict[str, any]:
    """
    Classify prompt type with rule-based detection and LLM fallback.
    
    Args:
        prompt: Input prompt string
        
    Returns:
        Dict with type, confidence, and reason
    """
    if not prompt or not prompt.strip():
        return {
            "type": "unknown",
            "confidence": 0.0,
            "reason": "empty prompt"
        }
    
    # Try rule-based classification first
    rule_type, rule_confidence, rule_reason = classify_prompt_rules(prompt)
    
    # If rule confidence is high enough, use it
    if rule_confidence >= 0.6:
        return {
            "type": rule_type,
            "confidence": rule_confidence,
            "reason": rule_reason
        }
    
    # If rule confidence is low, try LLM fallback
    llm_type, llm_confidence, llm_reason = classify_prompt_llm(prompt)
    
    # Choose best result
    if llm_confidence > rule_confidence:
        return {
            "type": llm_type,
            "confidence": llm_confidence,
            "reason": llm_reason
        }
    else:
        return {
            "type": rule_type,
            "confidence": rule_confidence,
            "reason": rule_reason
        }

def get_classification_suggestions(prompt_type: str) -> List[str]:
    """Get suggestions based on classified prompt type."""
    suggestions = {
        "email": [
            "This appears to be an email request. This system is designed for furniture/design specifications.",
            "Try prompts like: 'Create a wooden dining table' or 'Design a steel chair'"
        ],
        "design": [
            "Great! This looks like a design/furniture prompt.",
            "The system will extract materials, dimensions, colors, and purpose."
        ],
        "code": [
            "This appears to be a coding request. This system is for furniture design.",
            "Try prompts like: 'Build a glass desk' or 'Make a leather sofa'"
        ],
        "document": [
            "This looks like a document writing request. This system creates furniture specifications.",
            "Try prompts like: 'Design a modern chair' or 'Create a wooden table'"
        ],
        "unknown": [
            "Prompt type unclear. This system works best with furniture/design prompts.",
            "Try: 'Create a [material] [furniture_type]' like 'Create a wooden table'"
        ]
    }
    
    return suggestions.get(prompt_type, suggestions["unknown"])

# Demo function for testing
def demo_classifier():
    """Demo the classifier with various prompts."""
    test_prompts = [
        "Please write a short professional email to the marketing team",
        "Create a wooden dining table with glass top",
        "Write a Python function to sort a list",
        "Design a modern steel chair with wheels",
        "Compose a business letter to the client",
        "Build a 3-floor concrete library",
        "Hello world"
    ]
    
    print("=== Prompt Classifier Demo ===")
    for prompt in test_prompts:
        result = classify_prompt(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Type: {result['type']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Reason: {result['reason']}")

if __name__ == "__main__":
    demo_classifier()