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

### Current Implementation (Production Ready)
- ✅ Rule-based extraction using regex and keyword matching
- ✅ Comprehensive evaluation framework with scoring
- ✅ Complete reinforcement learning loop with feedback
- ✅ Binary and continuous reward systems
- ✅ Dashboard integration and detailed logging
- ✅ Enhanced error handling and recovery mechanisms

### Explicitly Missing Features (Future Enhancements)
- ❌ **LLM Integration**: Currently disabled. For production LLM use, integrate with:
  - GPT-4 API for advanced text understanding
  - Local models like LLaMA, Mistral for on-premise deployment
  - HuggingFace transformers for custom model integration
- ❌ **Advanced RL Environment**: Gymnasium integration removed for simplicity
  - For sophisticated RL training, implement custom environment
  - Consider policy gradient methods or actor-critic architectures
- ❌ **Web Interface**: Command-line only currently
  - Streamlit/FastAPI integration planned for web deployment
- ❌ **Database Integration**: File-based storage only
  - PostgreSQL/MongoDB integration for production scale

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **File Permissions**: Check write permissions for output directories
3. **Invalid Prompts**: Prompts must be 10-1000 characters long

### Debug Mode
Add `--verbose` flag for detailed logging (feature can be added)

## CLI Tools

### Prompt History
```bash
# Show last 5 prompts
python cli_tools.py history --last 5

# Show all prompts
python cli_tools.py history

# Show system statistics
python cli_tools.py stats
```

### System Statistics
```bash
python cli_tools.py stats
```

## Sample Outputs

The `sample_outputs/` directory contains example files:
- `sample_spec_1.json` - Perfect office building specification
- `sample_evaluation_1.json` - Complete evaluation report
- `sample_rl_training.json` - RL training with 2 iterations

## Logging System

### Traditional Logs
- **Location**: `logs/logs.json`
- **Content**: All prompt-result pairs with timestamps
- **Usage**: Retrievable via CLI tools

### Testing
- **Location**: `test_system.py`
- **Content**: Automated tests for all core functionality
- **Usage**: `python test_system.py`

## Production Readiness

### ✅ Complete Features (Tasks 1-3)
- **Task 1**: Prompt parsing and specification generation
- **Task 2**: Evaluation system with comprehensive scoring
- **Task 3**: RL loop with iterative feedback and improvement

### ✅ Production Quality
- Enhanced error handling with fallback mechanisms
- Comprehensive logging and status reporting
- Modular architecture with clear separation of concerns
- Robust file handling with validation
- Complete test coverage for core functionality

### ⚠️ Known Limitations
- LLM integration is disabled (rule-based generation only)
- No web interface (CLI only)
- File-based storage (no database integration)
- Basic RL implementation (no advanced policy methods)

### 🚀 Deployment Ready
The system is production-ready for the core prompt-to-JSON conversion task with RL feedback loops. All essential features are implemented and tested.

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

MIT License - see LICENSE file for details