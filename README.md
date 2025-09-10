# Prompt to JSON Agent with Evaluator & RL System

A comprehensive Python project for converting natural language prompts into structured JSON specifications with AI-powered evaluation, scoring, and reinforcement learning feedback loops.

## Project Overview

This system combines rule-based extraction, AI model integration, and reinforcement learning to create, evaluate, and improve furniture/object design specifications from natural language prompts.

### Key Components

1. **Spec Generation** - Extract structured data from prompts
2. **Evaluator Agent** - Critique generated specs with human-like feedback
3. **Data Scorer** - Rate completeness, realism, and format (0-10 scale)
4. **RL Loop** - Reward system for continuous improvement

## Installation

1. Clone the repository:
```bash
git clone https://github.com/anmolmishra307680-pixel/prompt-to-json-backend.git
cd prompt-to-json-backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Spec Generation
```bash
python src/extractor.py
```

### Full Pipeline Demo
```bash
python demo_pipeline.py
```

### Individual Components

**Generate Spec:**
```bash
python src/schema.py
```

**Evaluate Spec:**
```bash
python evaluator_agent.py --prompt "Create a wooden table" --spec spec_outputs/sample.json
```

**Run RL Loop:**
```bash
python rl_loop.py --runs 5
```

**Score Spec:**
```bash
python data_scorer.py
```

## Agent Flow

```
Prompt → Extractor → Schema Validator → Evaluator Agent → Data Scorer → RL Loop
   ↓         ↓              ↓               ↓             ↓          ↓
"Create   Extract      Validate &      Critique &    Score 0-10   Compute
 table"   fields       save JSON       feedback      & explain     reward
```

## Sample Output

### Complete Pipeline Result
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

## Project Structure

```
prompt-to-json-backend/
├── src/                     # Core generation modules
│   ├── extractor.py         # Pattern-based field extraction
│   ├── schema.py            # Pydantic validation models
│   ├── llama_prompt.py      # AI model integration
│   └── logger.py            # Logging system
├── evaluator_agent.py       # Critic agent with feedback
├── data_scorer.py           # Quality scoring (0-10)
├── rl_loop.py              # Reinforcement learning loop
├── demo_pipeline.py        # End-to-end demonstrations
├── envs/                   # RL environments
│   └── simple_spec_env.py  # Gymnasium-style environment
├── spec_outputs/           # Generated JSON specifications
├── evaluations/            # Critic feedback results
├── rl_logs/               # RL training history
├── sample_outputs/        # Full pipeline demonstrations
├── tests/                 # Unit tests
└── requirements.txt       # Dependencies
```

## Features

### 🔍 **Evaluator Agent**
- Human-like feedback on generated specs
- Issue detection (missing fields, invalid materials, etc.)
- Severity classification (none/minor/major)
- Saves detailed evaluation reports

### 📊 **Data Scorer**
- **Completeness Score** (0-4): Checks required fields
- **Material Realism** (0-3): Validates against known materials
- **Dimension Validity** (0-2): Parses and validates measurements
- **Type Match** (0-1): Matches spec type with prompt context
- **Format Score** (0-10): Aggregated quality rating

### 🔄 **RL Loop**
- Reward calculation based on evaluation and scoring
- History tracking for training data
- Integration with gymnasium-style environments
- Continuous improvement feedback

### 🎯 **Demo Examples**
- **Architectural**: "Design a 2-floor eco-friendly library"
- **Mechanical**: "Create a lightweight drone body"
- **Props**: "Build a medieval wooden throne"
- **Scene**: "Design a modern glass coffee table"
- **Medical**: "Create a surgical instrument cabinet"

## Scoring System

| Component | Max Score | Description |
|-----------|-----------|-------------|
| Completeness | 4 | All required fields present |
| Material Realism | 3 | Known materials, consistency |
| Dimension Validity | 2 | Parseable, reasonable ranges |
| Type Match | 1 | Spec matches prompt context |
| **Total** | **10** | **Overall quality score** |

## Reward System

- **Perfect Spec** (no issues): +1.0 reward
- **Minor Issues** (1-2 issues): +0.2 reward  
- **Major Issues** (3+ issues): -1.0 reward
- **Scaled by Score**: reward × (spec_score/10)

## Testing

Run all tests:
```bash
python -m pytest tests/ -v
```

Individual test suites:
```bash
python -m pytest tests/test_evaluator.py -v
python -m pytest tests/test_data_scorer.py -v
```

## Dependencies

- `openai` - AI model integration
- `transformers` - HuggingFace model pipeline
- `langchain` - Language model framework
- `pydantic` - Data validation and settings
- `numpy` - Numerical computations for RL environment

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for AI-powered design specification generation**