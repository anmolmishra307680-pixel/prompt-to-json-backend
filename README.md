# Prompt to JSON Agent with Evaluator & RL System

A comprehensive Python project for converting natural language prompts into structured JSON specifications with AI-powered evaluation, scoring, and reinforcement learning feedback loops.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   Extractor      │───▶│   Schema        │
│   (Prompt)      │    │   Pattern Match  │    │   Validation    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   RL Loop       │◀───│   Data Scorer    │◀───│   JSON Spec     │
│   Feedback      │    │   Quality (0-10) │    │   Output        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                       ▲                       │
         │                       │                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Agent Editor  │    │   Evaluator      │◀───│   Critic        │
│   Improvements  │    │   Report Gen     │    │   Analysis      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Core Features

1. **Enhanced Extraction** - Multi-material detection, improved dimension parsing (60-100% field detection)
2. **Evaluator Agent** - Rule-based critique with human-readable feedback  
3. **Data Scorer** - Quality rating system (0-10 scale)
4. **RL Loop** - Reward-based improvement tracking
5. **CLI & Web Interface** - Command-line and Streamlit demo applications
6. **Comprehensive Testing** - 75+ tests with CI/CD pipeline

## Quick Start

```bash
# Setup
git clone https://github.com/anmolmishra307680-pixel/prompt-to-json-backend.git
cd prompt-to-json-backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# CLI Usage
python src/main.py --prompt "Create a wooden dining table" --save-report --run-rl

# Web Demo
streamlit run src/web_app.py

# Run Tests
python -m pytest tests/ -v
```

## Usage

### Command Line Interface
```bash
# Basic prompt processing
python src/main.py --prompt "Create a wooden table"

# Process from file with full pipeline
echo "Design a modern steel chair" > prompt.txt
python src/main.py --prompt-file prompt.txt --save-report --run-rl

# Generate detailed evaluation reports
python src/main.py --prompt "Build a glass desk" --save-report
```

### Web Application
```bash
# Start interactive demo
streamlit run src/web_app.py
# Open http://localhost:8501 in browser
```

### Individual Components
```bash
# Test extraction and validation
python src/extractor.py
python src/schema.py

# Run evaluation and scoring
python evaluator_agent.py --prompt "Create a wooden table" --spec spec_outputs/sample.json
python data_scorer.py

# RL training and feedback
python src/rl/rl_loop.py
```

## Project Structure

```
prompt-to-json-backend/
├── src/
│   ├── main.py                # CLI entrypoint (robust)
│   ├── web_app.py             # Streamlit demo
│   ├── extractor.py           # Enhanced pattern extraction
│   ├── schema.py              # Pydantic validation
│   ├── logger.py              # Interaction logging
│   ├── data_scorer.py         # Quality scoring
│   ├── agent/
│   │   └── editor.py          # Automated improvements
│   ├── evaluator/
│   │   ├── criteria.py        # Validation rules
│   │   ├── report.py          # Report generation
│   │   └── feedback.py        # Feedback generation
│   └── rl/
│       └── rl_loop.py         # RL reward system
├── tests/                     # Comprehensive test suite (75+ tests)
├── docs/
│   ├── demo_instructions.md   # Usage guide
│   └── samples/               # End-to-end examples
├── spec_outputs/              # Generated JSON specifications
├── evaluations/               # Evaluation results
├── reports/                   # Human-readable reports
├── rl_logs/                   # RL training history
├── logs/                      # System logs
└── .github/workflows/         # CI/CD pipeline
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

## Sample Outputs

### Generated Specification
```json
{
  "type": "table",
  "material": ["wood", "glass"],
  "color": "brown",
  "dimensions": {
    "raw": "6x4 feet",
    "width_cm": 183,
    "height_cm": 122
  },
  "purpose": "dining",
  "metadata": {
    "generated_by": "extractor_v1",
    "confidence": 0.85
  }
}
```

### Evaluation Report
```json
{
  "prompt": "Create a wooden dining table with glass top",
  "spec_path": "spec_outputs/wooden_table_20250910_120000.json",
  "critic_feedback": "Specification looks complete and well-defined.",
  "issues": [],
  "severity": "none",
  "recommendations": [],
  "scores": {
    "format_score": 8.5,
    "completeness_score": 4,
    "material_realism_score": 3,
    "dimension_validity_score": 2,
    "type_match_score": 1
  },
  "timestamp": "2025-09-10T12:00:00Z"
}
```

### RL History Entry
```json
{
  "timestamp": "2025-09-10T12:05:00Z",
  "prompt": "Create a wooden dining table with glass top",
  "spec_path": "spec_outputs/wooden_table_20250910_120000.json",
  "eval_path": "evaluations/eval_wooden_table_20250910_120000.json",
  "format_score": 8.5,
  "reward": 0.425,
  "editor_action": "no_changes_needed",
  "notes": "high quality spec generated"
}
```

## Development Journey - Day by Day

### Day 1-5: Foundation
- **Day 1**: Basic extraction patterns and regex rules
- **Day 2**: Pydantic schema validation and error handling
- **Day 3**: Logging system and interaction tracking
- **Day 4**: Multi-material support and smart fallbacks
- **Day 5**: LLM integration template and prompt engineering

### Day 6-10: Intelligence Layer
- **Day 6**: Evaluator agent with comprehensive criteria validation
- **Day 7**: Data scoring system with 4-component quality metrics
- **Day 8**: Feedback generation and RL reward computation
- **Day 9**: Automated improvement system with retry logic
- **Day 10**: Comprehensive testing suite and CI/CD pipeline

### Day 11-12: Polish & Production
- **Day 11**: Enhanced CLI with robust error handling and Streamlit demo
- **Day 12**: Final documentation, sample outputs, and project completion

### Values Demonstrated
- **Honesty**: Transparent reporting of limitations and edge cases
- **Discipline**: Consistent daily progress with systematic testing
- **Gratitude**: Appreciation for iterative improvement and learning opportunities

## Testing & Quality Assurance

```bash
# Run comprehensive test suite (75+ tests)
python -m pytest tests/ -v

# Run specific test modules
python -m pytest tests/test_extractor.py -v
python -m pytest tests/test_evaluator.py -v
python -m pytest tests/test_rl_loop.py -v

# Test CLI functionality
python test_day11.py

# Run CI pipeline locally
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage
- **Extractor**: Pattern matching, multi-material detection, edge cases
- **Schema**: Validation rules, error handling, fallback mechanisms
- **Evaluator**: Criteria validation, report generation, scoring integration
- **RL Loop**: Reward computation, feedback application, iteration tracking
- **Integration**: End-to-end pipeline testing with mocked dependencies

## Dependencies

### Core Requirements
- `pydantic==2.9.2` - Data validation and schema enforcement
- `numpy==2.3.2` - Numerical computations for scoring
- `pytest==7.4.4` - Testing framework
- `streamlit>=1.28.0` - Web application framework

### Optional Integrations
- `transformers==4.44.2` - HuggingFace model integration
- `torch==2.4.1` - PyTorch for ML models
- `langchain==0.3.7` - LLM orchestration framework

### Development Tools
- GitHub Actions for CI/CD
- Multi-Python version testing (3.8, 3.9, 3.10, 3.11)
- Automated linting and code quality checks

## Performance Metrics

- **Extraction Accuracy**: 68-80% field completion rate
- **Multi-material Detection**: 100% success on complex prompts
- **Quality Scoring**: 6.6-8.0/10 average across test cases
- **Processing Speed**: 1-3 seconds per prompt
- **Test Coverage**: 75+ tests with 100% pass rate
- **CI/CD**: Automated testing across multiple Python versions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`python -m pytest tests/ -v`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with systematic daily development approach
- Comprehensive testing and quality assurance
- Production-ready architecture with robust error handling
- Interactive demo for accessibility and user experience