# Prompt-to-JSON Agent Backend

A comprehensive system that converts natural language prompts into structured JSON design specifications using rule-based extraction, evaluation, and reinforcement learning feedback loops.

## Features

- **Prompt Interpretation**: Extract building specifications from natural language
- **Multi-mode Generation**: Rule-based and LLM-based (stub) generation
- **Comprehensive Evaluation**: Scoring based on completeness, format validity, and feasibility
- **Reinforcement Learning**: Iterative improvement through feedback loops
- **Detailed Reporting**: JSON reports and summaries
- **CLI Interface**: Easy-to-use command-line interface

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd prompt-to-json-backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Generate a single specification:
```bash
python main.py --prompt "Design a two-story steel building with glass facade"
```

### Advanced Usage

Run reinforcement learning training:
```bash
python main.py --prompt "Modern office building" --mode rl --iterations 5
```

Compare rule-based vs LLM approaches:
```bash
python main.py --prompt "Residential complex" --mode compare
```

Use LLM generation (stub):
```bash
python main.py --prompt "Luxury hotel" --use-llm
```

## Examples

### Example 1: Basic Building
```bash
python main.py --prompt "Design a two-story steel building with glass facade"
```

**Expected Output:**
- Building type: general
- Stories: 2
- Materials: steel, glass
- Features: facade
- Dimensions: 20m x 15m x 7m

### Example 2: Commercial Building
```bash
python main.py --prompt "Modern 5-story commercial office building with parking and elevator"
```

**Expected Output:**
- Building type: commercial
- Stories: 5
- Materials: steel
- Features: parking, elevator
- Dimensions: 30m x 25m x 17.5m

### Example 3: Residential Complex
```bash
python main.py --prompt "Luxury residential complex with 3 floors, concrete structure, balconies and garden"
```

**Expected Output:**
- Building type: residential
- Stories: 3
- Materials: concrete
- Features: balcony, garden
- Enhanced features: parking (auto-added)

### Example 4: Industrial Warehouse
```bash
python main.py --prompt "Large industrial warehouse with steel frame and 40m x 60m dimensions"
```

**Expected Output:**
- Building type: industrial
- Stories: 1
- Materials: steel
- Dimensions: 40m x 60m (extracted from prompt)
- Features: parking (auto-added)

### Example 5: RL Training
```bash
python main.py --prompt "Design a sustainable office building" --mode rl --iterations 3
```

**Expected Behavior:**
- Iteration 1: Basic specification generation
- Iteration 2: Improvement based on evaluation feedback
- Iteration 3: Further refinement
- Shows score progression and learning insights

## Project Structure

```
prompt-to-json-backend/
├── main.py                # CLI orchestrator
├── main_agent.py          # Main generation agent
├── evaluator_agent.py     # Evaluation agent
├── rl_loop.py             # Reinforcement learning loop
├── extractor.py           # Rule-based field extraction
├── schema.py              # Pydantic data models
├── evaluator/
│   ├── criteria.py        # Evaluation criteria and scoring
│   ├── report.py          # Report generation
│   └── feedback.py        # Feedback loop management
├── logs/                  # Training and feedback logs
├── spec_outputs/          # Generated specifications
├── reports/               # Evaluation reports
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Output Files

### Specifications
- **Location**: `spec_outputs/`
- **Format**: `design_spec_YYYYMMDD_HHMMSS.json`
- **Content**: Complete design specification with metadata

### Reports
- **Location**: `reports/`
- **Format**: `evaluation_report_YYYYMMDD_HHMMSS.json`
- **Content**: Detailed evaluation results and scoring

### Logs
- **Feedback Log**: `logs/feedback_log.json` - RL iteration-by-iteration feedback
- **Training Results**: `logs/rl_training_*.json` - Complete training sessions

## Evaluation Criteria

### Completeness (40% weight)
- Building type specification
- Number of stories
- Materials specification
- Dimensions
- Special features

### Format Validity (30% weight)
- Schema validation
- Data type correctness
- Required field presence

### Feasibility (30% weight)
- Structural feasibility
- Material compatibility
- Dimensional reasonableness

## Scoring System

- **A (90-100)**: Excellent specification
- **B (80-89)**: Good specification with minor issues
- **C (70-79)**: Acceptable with improvements needed
- **D (60-69)**: Poor specification requiring major changes
- **F (<60)**: Inadequate specification

## Development Notes

### Current Implementation
- Rule-based extraction using regex and keyword matching
- Stub LLM implementation (ready for HuggingFace integration)
- Comprehensive evaluation framework
- Basic reinforcement learning loop

### Future Enhancements
- Integration with actual LLM models (LLaMA, GPT, etc.)
- Advanced NLP techniques for better extraction
- More sophisticated reward functions
- Web interface
- Database integration

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **File Permissions**: Check write permissions for output directories
3. **Invalid Prompts**: Prompts must be 10-1000 characters long

### Debug Mode
Add `--verbose` flag for detailed logging (feature can be added)

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

MIT License - see LICENSE file for details