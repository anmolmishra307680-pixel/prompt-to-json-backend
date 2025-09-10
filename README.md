# Prompt-to-JSON Agent

A Python agent that converts natural language prompts into structured JSON design specifications using AI models. The system combines rule-based extraction with LLM refinement to produce validated JSON outputs.

## Features

- **Rule-based Extraction**: Keyword matching for materials, objects, colors, dimensions
- **LLM Integration**: Uses DistilGPT-2 for prompt refinement and enhancement
- **Schema Validation**: Pydantic models ensure consistent JSON structure
- **Comprehensive Logging**: All prompt-response pairs logged with timestamps
- **Robust Testing**: 26+ tests covering edge cases and integration scenarios

## Project Structure

```
prompt-to-json-backend/
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── extractor.py         # Rule-based field extraction
│   ├── llama_prompt.py      # LLM integration + orchestration
│   ├── schema.py            # Pydantic DesignSpec + validation
│   └── logger.py            # Logging functionality
│
├── data/
│   ├── logs.json            # Application logs (JSON array)
│   └── spec_outputs/        # Generated JSON specifications
│       ├── house.json
│       ├── drone.json
│       ├── chest.json
│       ├── robotic_hand.json
│       └── scene.json
│
├── tests/
│   ├── test_extractor.py    # Extractor unit tests
│   ├── test_schema.py       # Schema validation tests
│   ├── test_integration.py  # End-to-end pipeline tests
│   ├── test_edge_cases.py   # Edge case handling tests
│   └── test_llama_prompt.py # LLM integration tests
│
└── examples/
    ├── sample_prompts.txt
    └── sample_outputs.json
```

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anmolmishra307680-pixel/prompt-to-json-backend.git
   cd prompt-to-json-backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests to verify setup**:
   ```bash
   python -m pytest tests/ -v
   ```

## Usage

### Basic Extraction

Extract structured fields from natural language prompts:

```python
from src.extractor import extract_basic_fields

# Extract fields from prompt
result = extract_basic_fields("Create a red gearbox with steel gears for automotive use.")
print(result)
```

**Output**:
```json
{
  "type": "gearbox",
  "material": ["steel"],
  "color": "red",
  "dimensions": null,
  "purpose": "automotive use",
  "extras": null
}
```

### LLM Integration

Use LLM to refine extracted fields and log results:

```python
from src.llama_prompt import refine_with_llm

# Process with LLM and log
result = refine_with_llm("Design a 2-floor building using glass and concrete.")
print(result['extractor_output'])
```

### Schema Validation & Export

Validate and save structured specifications:

```python
from src.schema import save_spec

# Save validated JSON spec
raw_data = {
    "type": "gearbox",
    "material": ["steel"],
    "color": "red",
    "purpose": "automotive use"
}

filename = save_spec(raw_data, "data/spec_outputs/my_gearbox.json")
print(f"Saved to: {filename}")
```

## Example Commands

### Run Extractor Only
```bash
python -c "from src.extractor import extract_basic_fields; print(extract_basic_fields('Create a red gearbox with steel gears.'))"
```

### Run Full LLM Pipeline
```bash
python -m src.llama_prompt
```

### CLI Runner (Command Line Interface)

Process prompts directly from command line:

```bash
# Basic extraction and save
python -m src.runner --prompt "Create a red gearbox with steel gears" --save

# With LLM refinement
python -m src.runner --prompt "Design a modern building" --llm --save

# Custom output filename
python -m src.runner --prompt "Build a drone" --save --output "data/spec_outputs/my_drone.json"
```

### Generate Sample Specifications
```python
from src.extractor import extract_basic_fields
from src.schema import save_spec

prompts = [
    "Design a 2-floor house using brick and wood.",
    "Create a lightweight drone body using carbon fiber.",
    "Build a treasure chest for a medieval game."
]

for prompt in prompts:
    extracted = extract_basic_fields(prompt)
    if extracted['type'] is None:
        extracted['type'] = 'unspecified'
    if not extracted['material']:
        extracted['material'] = ['unspecified']
    
    filename = save_spec(extracted)
    print(f"Generated: {filename}")
```

## Sample Output

**Input**: `"Create a red gearbox with steel gears for automotive use."`

**Generated JSON** (`data/spec_outputs/gearbox.json`):
```json
{
    "type": "gearbox",
    "material": [
        "steel"
    ],
    "color": "red",
    "dimensions": null,
    "purpose": "automotive use",
    "extras": null
}
```

**Log Entry** (`data/logs.json`):
```json
{
  "prompt": "Create a red gearbox with steel gears for automotive use.",
  "extractor_output": {
    "type": "gearbox",
    "material": ["steel"],
    "color": "red",
    "dimensions": null,
    "purpose": "automotive use",
    "extras": null
  },
  "llm_raw": "Prompt: Create a red gearbox with steel gears for automotive use.\nJSON: ...",
  "timestamp": "2025-09-10T09:00:00.123456"
}
```

## Testing

Run the complete test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test modules
python -m pytest tests/test_extractor.py -v
python -m pytest tests/test_schema.py -v
python -m pytest tests/test_integration.py -v

# Quick test run
python -m pytest -q
```

**Test Coverage**: 26+ tests covering:
- Rule-based extraction logic
- Schema validation and edge cases
- LLM integration functionality
- End-to-end pipeline integration
- Error handling and fallback scenarios

## Architecture

1. **Extractor** (`src/extractor.py`): Rule-based keyword matching for structured field extraction
2. **LLM Integration** (`src/llama_prompt.py`): DistilGPT-2 integration for prompt refinement
3. **Schema Validation** (`src/schema.py`): Pydantic models for JSON structure validation
4. **Logging** (`src/logger.py`): Comprehensive logging of all prompt-response pairs

## Dependencies

- **transformers**: Hugging Face transformers for LLM integration
- **pydantic**: Data validation and schema enforcement
- **pytest**: Testing framework
- **torch**: PyTorch backend for transformers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.