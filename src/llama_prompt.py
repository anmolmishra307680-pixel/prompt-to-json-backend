import json
import datetime
from transformers import pipeline
from src.extractor import extract_basic_fields
from src.logger import append_log

pipe = pipeline("text-generation", model="distilgpt2")

def refine_with_llm(prompt: str, max_new_tokens=50):
    base = extract_basic_fields(prompt)
    # build a short instruction for LLM to produce JSON-like clarification
    llm_prompt = f"Prompt: {prompt}\nJSON:"
    resp = pipe(llm_prompt, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7)[0]["generated_text"]
    # naive attempt: return base and raw llm text (we will parse in Day4)
    entry = {
        "prompt": prompt,
        "extractor_output": base,
        "llm_raw": resp,
        "timestamp": datetime.datetime.now().isoformat()
    }
    append_log(entry)
    return entry

if __name__ == "__main__":
    print(refine_with_llm("Design a 2-floor building using glass and concrete."))