# Prompt to JSON Agent with Evaluator & RL System

A streamlined Python project for converting natural language prompts into structured JSON specifications with evaluation, scoring, and reinforcement learning feedback.

## Core Features

1. **Enhanced Extraction** - Pattern-based field extraction with improved accuracy
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
```

## Usage

### Individual Components
```bash
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
├── utils.py                # Shared utilities
├── tests/                  # Test suite
├── spec_outputs/           # Generated specifications
├── evaluations/            # Evaluation results
├── rl_logs/               # RL training history
└── sample_outputs/        # Demo results
```

## Sample Output

```json
{
  "prompt": "Design a modern glass coffee table for living room",
  "spec": {
    "type": "table",
    "material": "glass", 
    "color": "default",
    "dimensions": "standard",
    "purpose": "living room"
  },
  "evaluation": {
    "critic_feedback": "Dimensions are missing (provide specific measurements).",
    "issues": ["dimensions_missing"],
    "severity": "minor"
  },
  "scoring": {
    "format_score": 7.0,
    "completeness_score": 3,
    "material_realism_score": 3,
    "dimension_validity_score": 0,
    "type_match_score": 1
  },
  "reward": 0.14
}
```

## Testing

```bash
python -m pytest tests/ -v
```

## Dependencies

- `pydantic` - Data validation
- `numpy` - Numerical computations

## License

MIT License