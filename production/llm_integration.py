"""Optional LLM integration for enhanced spec generation."""

import json
from typing import Dict, Optional

def generate_with_llm(prompt: str, model_name: str = "gpt-3.5-turbo") -> Optional[Dict]:
    """
    Generate spec using LLM API (placeholder implementation).
    
    This is a template for integrating with OpenAI, Anthropic, or local models.
    Replace with actual API calls as needed.
    """
    
    # Template system prompt for spec generation
    system_prompt = """You are a furniture design specification generator. 
    Convert natural language prompts into structured JSON with these fields:
    - type: furniture type (table, chair, etc.)
    - material: primary material(s) 
    - color: color specification
    - dimensions: measurements with units
    - purpose: intended use/context
    
    Return only valid JSON."""
    
    # Placeholder for actual LLM integration
    # Example integrations:
    
    # OpenAI API:
    # import openai
    # response = openai.ChatCompletion.create(
    #     model=model_name,
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return json.loads(response.choices[0].message.content)
    
    # Anthropic Claude:
    # import anthropic
    # client = anthropic.Anthropic(api_key="your-key")
    # response = client.messages.create(
    #     model="claude-3-sonnet-20240229",
    #     messages=[{"role": "user", "content": f"{system_prompt}\n\nPrompt: {prompt}"}]
    # )
    # return json.loads(response.content[0].text)
    
    # Local model (Ollama):
    # import requests
    # response = requests.post("http://localhost:11434/api/generate", json={
    #     "model": "llama2",
    #     "prompt": f"{system_prompt}\n\nPrompt: {prompt}",
    #     "stream": False
    # })
    # return json.loads(response.json()["response"])
    
    print(f"LLM integration placeholder - would process: {prompt}")
    return None

def enhance_spec_with_llm(extracted_spec: Dict, prompt: str) -> Dict:
    """Enhance extracted spec using LLM for missing fields."""
    
    # Check what fields are missing
    missing_fields = [k for k, v in extracted_spec.items() if not v or v in ['unknown', 'unspecified', 'default', 'standard']]
    
    if not missing_fields:
        return extracted_spec
    
    # Generate enhancement prompt
    enhancement_prompt = f"""
    Original prompt: {prompt}
    Current spec: {json.dumps(extracted_spec)}
    Missing/unclear fields: {missing_fields}
    
    Please provide better values for the missing fields based on the original prompt.
    Return only the enhanced spec as JSON.
    """
    
    # Placeholder for LLM enhancement
    enhanced = generate_with_llm(enhancement_prompt)
    
    if enhanced:
        # Merge enhanced fields back
        for field in missing_fields:
            if field in enhanced and enhanced[field]:
                extracted_spec[field] = enhanced[field]
    
    return extracted_spec

if __name__ == "__main__":
    # Demo of LLM integration points
    test_prompt = "Create a lightweight carbon fiber drone frame"
    
    print("=== LLM Integration Demo ===")
    print(f"Prompt: {test_prompt}")
    print("\n1. Direct LLM generation:")
    result = generate_with_llm(test_prompt)
    print(f"Result: {result}")
    
    print("\n2. Enhancement of extracted spec:")
    extracted = {
        "type": "drone",
        "material": "carbon fiber", 
        "color": "default",
        "dimensions": "standard",
        "purpose": "aerial"
    }
    enhanced = enhance_spec_with_llm(extracted, test_prompt)
    print(f"Enhanced: {enhanced}")
    
    print("\nTo enable LLM integration:")
    print("1. Install: pip install openai anthropic requests")
    print("2. Set API keys in environment variables")
    print("3. Uncomment desired integration in generate_with_llm()")
    print("4. Import and use in demo_pipeline.py or rl_loop.py")