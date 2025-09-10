# Prompt to JSON Agent with Evaluator & RL System

A comprehensive Python project for converting natural language prompts into structured JSON specifications with AI-powered evaluation, scoring, and reinforcement learning feedback loops.

## Core Features

1. **Enhanced Extraction** - Multi-material detection, improved dimension parsing (60-100% field detection)
2. **Evaluator Agent** - Rule-based critique with human-readable feedback  
3. **Data Scorer** - Quality rating system (0-10 scale)
4. **RL Loop** - Reward-based improvement tracking
5. **Optional LLM Integration** - Template for OpenAI/Anthropic/Local models
6. **RL Environment** - Gymnasium-style interface for spec refinement

## Quick Start

```bash
# Setup
git clone https://github.com/anmolmishra307680-pixel/prompt-to-json-backend.git
cd prompt-to-json-backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run full demo
python demo_pipeline.py

# Run advanced demo
python advanced_demo.py
```

## Usage

### Individual Components
```bash
# Test enhanced extraction
python src/extractor.py

# Generate and validate spec
python src/schema.py

# Evaluate existing spec
python evaluator_agent.py --prompt "Create a wooden table" --spec spec_outputs/sample.json

# Run RL training loop
python rl_loop.py --runs 5

# Test scoring system
python data_scorer.py

# Test RL environment
python rl_env.py

# Test multi-material extraction
python test_multi_material.py

# Demo LLM integration
python llm_integration.py
```

## Project Structure

```
prompt-to-json-backend/
├── src/
│   ├── extractor.py         # Enhanced pattern extraction
│   └── schema.py            # Pydantic validation
├── evaluator_agent.py       # Spec evaluation & critique
├── data_scorer.py          # Quality scoring (0-10)
├── rl_loop.py              # RL reward system
├── rl_env.py               # Optional RL environment
├── llm_integration.py      # LLM integration template
├── demo_pipeline.py        # End-to-end demonstration
├── advanced_demo.py        # Complex prompt testing
├── test_multi_material.py  # Multi-material testing
├── utils.py                # Smart fallback utilities
├── tests/                  # Test suite
├── spec_outputs/           # Generated specifications
├── evaluations/            # Evaluation results
├── rl_logs/               # RL training history
└── sample_outputs/        # Demo results
```

## Enhanced Capabilities

### Advanced Extraction
- **Multi-Material Support**: "glass, concrete", "wood, metal", "plastic, carbon fiber"
- **Complex Types**: drone, library, throne, cabinet
- **Smart Dimensions**: Prioritizes numeric over descriptive (6 feet > lightweight)
- **Context-Aware Purpose**: drone→aerial, throne→ceremonial, cabinet→storage
- **Smart Color Defaults**: wood→brown, metal→silver, throne→gold

### Performance Metrics
- **Multi-material detection**: 100% success on complex prompts
- **Average extraction**: 68-80% field completion
- **Quality scores**: 6.6-8.0/10 average
- **Purpose accuracy**: Fixed type-aware assignments

## Sample Output

```json
{
  "prompt": "Create a table with glass top and steel legs",
  "spec": {
    "type": "table",
    "material": "metal, glass", 
    "color": "silver",
    "dimensions": "standard",
    "purpose": "dining"
  },
  "evaluation": {
    "critic_feedback": "Dimensions are missing (provide specific measurements).",
    "issues": ["dimensions_missing"],
    "severity": "minor"
  },
  "scoring": {
    "format_score": 7.0,
    "completeness_score": 4,
    "material_realism_score": 3,
    "dimension_validity_score": 0,
    "type_match_score": 1
  },
  "reward": 0.14
}
```

## Optional Integrations

### LLM Enhancement
```python
from llm_integration import enhance_spec_with_llm

# Enhance extracted spec with LLM
enhanced_spec = enhance_spec_with_llm(extracted_spec, prompt)
```

### RL Environment
```python
from rl_env import SpecGenerationEnv

env = SpecGenerationEnv()
obs = env.reset("Create a wooden table")
obs, reward, done, info = env.step({"dimensions": "6x4 feet"})
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Test individual components
python src/extractor.py
python advanced_demo.py
python test_multi_material.py
```

## Dependencies

- `pydantic` - Data validation
- `numpy` - Numerical computations  
- `pytest` - Testing framework

Optional for LLM integration:
- `openai` - OpenAI API
- `anthropic` - Claude API
- `requests` - Local model APIs

## License

MIT License