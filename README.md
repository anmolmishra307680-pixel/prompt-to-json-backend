# Prompt to JSON Agent

A Python project for converting natural language prompts into structured JSON specifications for furniture design using AI models and pattern matching.

## Project Purpose

This tool extracts structured information from furniture design prompts and converts them into validated JSON specifications. It combines rule-based extraction with AI model integration for comprehensive prompt processing.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prompt-to-json-agent.git
cd prompt-to-json-agent
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage Examples

### Basic Field Extraction
```python
from src.extractor import extract_basic_fields

prompt = "Create a wooden dining table that is 6 feet long and brown in color"
result = extract_basic_fields(prompt)
print(result)
# Output: {'type': 'table', 'material': 'wood', 'color': 'brown', 'dimensions': '6 feet', 'purpose': 'dining'}
```

### Schema Validation
```python
from src.schema import validate_and_save

raw_data = {
    "type": "chair",
    "material": "metal", 
    "color": "black",
    "purpose": "office"
}
spec = validate_and_save(raw_data, "office_chair.json")
```

### AI Model Integration
```python
from src.llama_prompt import load_model, generate_response

generator = load_model()
response = generate_response("Design a modern sofa", generator)
print(response)
```

### Logging System
```python
from src.logger import append_log, get_last_prompts

append_log("Create a desk", "Generated desk specification")
last_entries = get_last_prompts(3)
```

## Sample Output

### JSON Specification Example
```json
{
  "type": "table",
  "material": "wood",
  "color": "brown",
  "dimensions": "6 feet",
  "purpose": "dining"
}
```

### Log Entry Example
```json
{
  "timestamp": "2025-09-10T11:50:26.672850",
  "prompt": "Create a wooden dining table",
  "output": "Generated spec: {'type': 'table', 'material': 'wood', 'color': 'brown'}"
}
```

## Project Structure

```
prompt-to-json-agent/
├── src/
│   ├── extractor.py      # Pattern-based field extraction
│   ├── schema.py         # Pydantic validation models
│   ├── llama_prompt.py   # AI model integration
│   ├── logger.py         # Logging system
│   └── test_prompts.py   # Testing framework
├── spec_outputs/         # Generated JSON specifications
├── logs.json            # Processing logs
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Features

- **Pattern Matching**: Extract furniture type, material, color, dimensions, and purpose
- **AI Integration**: Use DistilGPT2 for enhanced text generation
- **Schema Validation**: Pydantic-based JSON validation with fallback values
- **Logging System**: Timestamped logging with retrieval functionality
- **Edge Case Handling**: Robust fallback mechanisms for incomplete prompts

## Dependencies

- `openai` - AI model integration
- `transformers` - HuggingFace model pipeline
- `langchain` - Language model framework
- `pydantic` - Data validation and settings management