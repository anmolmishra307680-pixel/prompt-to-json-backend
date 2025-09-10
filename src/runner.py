#!/usr/bin/env python3
"""
CLI runner for the Prompt-to-JSON Agent
Usage: python src/runner.py --prompt "Design a red gearbox" --save
"""

import argparse
import json
from src.extractor import extract_basic_fields
from src.llama_prompt import refine_with_llm
from src.schema import save_spec

def main():
    parser = argparse.ArgumentParser(description='Prompt-to-JSON Agent CLI')
    parser.add_argument('--prompt', required=True, help='Input prompt to process')
    parser.add_argument('--save', action='store_true', help='Save output to spec_outputs/')
    parser.add_argument('--llm', action='store_true', help='Use LLM refinement')
    parser.add_argument('--output', help='Custom output filename')
    
    args = parser.parse_args()
    
    print(f"Processing prompt: {args.prompt}")
    
    if args.llm:
        # Use LLM pipeline
        result = refine_with_llm(args.prompt)
        extracted = result['extractor_output']
        print(f"LLM processing completed. Log entry created.")
    else:
        # Use extractor only
        extracted = extract_basic_fields(args.prompt)
    
    print(f"Extracted fields: {json.dumps(extracted, indent=2)}")
    
    if args.save:
        # Add fallbacks for missing required fields
        if extracted['type'] is None:
            extracted['type'] = 'unspecified'
        if not extracted['material']:
            extracted['material'] = ['unspecified']
        
        filename = save_spec(extracted, args.output)
        print(f"Specification saved to: {filename}")
    
    return extracted

if __name__ == "__main__":
    main()