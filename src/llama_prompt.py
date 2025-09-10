"""LLaMA/HuggingFace integration for spec generation using lightweight models."""

import json
import os
import re
from datetime import datetime
from typing import Dict, Optional

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

try:
    from extractor import extract_basic_fields
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from extractor import extract_basic_fields

# Global model cache
_model_cache = None
_tokenizer_cache = None

def get_model():
    """Load and cache the lightweight model."""
    global _model_cache, _tokenizer_cache
    
    if not HF_AVAILABLE:
        raise ImportError("transformers not available. Install with: pip install transformers torch")
    
    if _model_cache is None:
        model_name = "distilgpt2"  # Lightweight model
        print(f"Loading model: {model_name}")
        
        _tokenizer_cache = AutoTokenizer.from_pretrained(model_name)
        _model_cache = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Add pad token if missing
        if _tokenizer_cache.pad_token is None:
            _tokenizer_cache.pad_token = _tokenizer_cache.eos_token
    
    return _model_cache, _tokenizer_cache

def generate_raw_response(prompt: str) -> str:
    """Generate raw LLM response from prompt."""
    try:
        model, tokenizer = get_model()
        
        # Create structured prompt for spec generation
        structured_prompt = f"""Generate a JSON specification for: {prompt}

Format:
{{
  "type": "object_type",
  "material": ["material1", "material2"],
  "color": "color_name",
  "dimensions": {{"raw": "dimensions"}},
  "purpose": "intended_use"
}}

JSON:"""
        
        # Generate response
        inputs = tokenizer.encode(structured_prompt, return_tensors="pt", max_length=200, truncation=True)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 100,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part
        generated_text = response[len(structured_prompt):].strip()
        
        # Log the interaction
        log_llm_interaction(prompt, generated_text)
        
        return generated_text
        
    except Exception as e:
        print(f"LLM generation failed: {e}")
        return f"Error: {str(e)}"

def generate_spec_with_llm(prompt: str) -> dict:
    """Generate spec using LLM with fallback to rule-based extraction."""
    
    # Try LLM generation first
    try:
        llm_output = generate_raw_response(prompt)
        
        # Try to parse JSON from LLM output
        parsed_spec = parse_json_from_text(llm_output)
        
        if parsed_spec and validate_spec_structure(parsed_spec):
            print(f"[SUCCESS] LLM generated valid spec")
            return parsed_spec
        else:
            print(f"[FALLBACK] LLM output invalid, falling back to rule-based")
            
    except Exception as e:
        print(f"[ERROR] LLM failed ({e}), falling back to rule-based")
    
    # Fallback to rule-based extraction
    fallback_spec = extract_basic_fields(prompt)
    
    # Convert to expected format
    return {
        "type": fallback_spec.get('type'),
        "material": fallback_spec.get('material', []),
        "color": fallback_spec.get('color', 'none'),
        "dimensions": fallback_spec.get('dimensions', {}),
        "purpose": fallback_spec.get('purpose'),
        "source": "fallback"
    }

def parse_json_from_text(text: str) -> Optional[Dict]:
    """Extract JSON from LLM text output."""
    try:
        # Look for JSON-like blocks
        json_patterns = [
            r'\{[^{}]*\}',  # Simple JSON block
            r'\{.*?\}',     # Any content between braces
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    # Clean up the match
                    cleaned = match.strip()
                    parsed = json.loads(cleaned)
                    if isinstance(parsed, dict):
                        return parsed
                except json.JSONDecodeError:
                    continue
        
        return None
        
    except Exception:
        return None

def validate_spec_structure(spec: dict) -> bool:
    """Validate that spec has required structure."""
    required_fields = ['type', 'material', 'color', 'purpose']
    return all(field in spec for field in required_fields)

def log_llm_interaction(prompt: str, llm_output: str):
    """Log LLM interactions to JSONL file."""
    try:
        from logger import log_prompt
        # Use centralized logger
        log_prompt(
            prompt=prompt,
            llm_output=llm_output,
            model="distilgpt2",
            source="llm_generation"
        )
    except ImportError:
        # Fallback to original logging
        os.makedirs("logs", exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "llm_output": llm_output,
            "model": "distilgpt2"
        }
        
        with open("logs/llm_logs.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

def save_sample_spec(spec: dict, filename: str):
    """Save spec to spec_outputs directory."""
    os.makedirs("spec_outputs", exist_ok=True)
    
    output_spec = {
        **spec,
        "timestamp": datetime.now().isoformat(),
        "generated_by": "llm" if spec.get("source") != "fallback" else "fallback"
    }
    
    filepath = f"spec_outputs/{filename}"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output_spec, f, indent=2)
    
    return filepath

# Demo function
def run_demo():
    """Run demo with sample prompts."""
    demo_prompts = [
        "Design a red gearbox with steel gears",
        "Create a wooden dining table with glass top",
        "Build a concrete library with 3 floors"
    ]
    
    print("=== LLM Integration Demo ===")
    
    for i, prompt in enumerate(demo_prompts, 1):
        print(f"\nDemo {i}: {prompt}")
        
        try:
            spec = generate_spec_with_llm(prompt)
            print(f"Generated spec: {spec}")
            
            # Save sample
            filename = f"llm_sample_{i:02d}.json"
            filepath = save_sample_spec(spec, filename)
            print(f"Saved to: {filepath}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_demo()