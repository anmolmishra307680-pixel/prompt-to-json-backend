# Prompt to JSON Agent with Evaluator & RL System

A streamlined Python project for converting natural language prompts into structured JSON specifications with evaluation, scoring, and reinforcement learning feedback.

## Core Features

1. **Enhanced Extraction** - Pattern-based field extraction with improved accuracy (60-100% field detection)
2. **Evaluator Agent** - Rule-based critique with human-readable feedback  
3. **Data Scorer** - Quality rating system (0-10 scale)
4. **RL Loop** - Reward-based improvement tracking

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
├── demo_pipeline.py        # End-to-end demonstration
├── advanced_demo.py        # Complex prompt testing
├── utils.py                # Shared utilities
├── tests/                  # Test suite
├── spec_outputs/           # Generated specifications
├── evaluations/            # Evaluation results
├── rl_logs/               # RL training history
└── sample_outputs/        # Demo results
```

## Enhanced Capabilities

### Improved Extraction
- **Complex Types**: drone, library, throne, cabinet
- **Advanced Materials**: carbon fiber, concrete, stainless steel
- **Descriptive Dimensions**: lightweight, compact, massive, 2-floor
- **Contextual Purpose**: medical, industrial, aerial photography

### Performance Metrics
- **Average Extraction Rate**: 60-80% field completion
- **Quality Scores**: 6.2-8.0/10 average
- **Issue Detection**: Comprehensive validation with severity levels

## Sample Output

```json
{
  "prompt": "Design a lightweight carbon fiber drone frame",
  "spec": {
    "type": "drone",
    "material": "carbon fiber", 
    "color": "default",
    "dimensions": "lightweight",
    "purpose": "general"
  },
  "evaluation": {
    "critic_feedback": "Dimensions format unclear or missing units.",
    "issues": ["dimensions_unparseable"],
    "severity": "minor"
  },
  "scoring": {
    "format_score": 7.0,
    "completeness_score": 3,
    "material_realism_score": 3,
    "dimension_validity_score": 1,
    "type_match_score": 1
  },
  "reward": 0.14
}
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Test individual components
python src/extractor.py
python advanced_demo.py
```

## Dependencies

- `pydantic` - Data validation
- `numpy` - Numerical computations  
- `pytest` - Testing framework

## License

MIT License