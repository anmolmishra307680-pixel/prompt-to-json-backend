# Prompt-to-JSON Agent Backend

A comprehensive system that converts natural language prompts into structured JSON design specifications using rule-based extraction, evaluation, and reinforcement learning feedback loops.

## Features

- **Prompt Interpretation**: Extract building specifications from natural language
- **Multi-mode Generation**: Rule-based generation with advanced RL training
- **Comprehensive Evaluation**: Scoring based on completeness, format validity, and feasibility
- **Reinforcement Learning**: Iterative improvement through feedback loops
- **Detailed Reporting**: JSON reports and summaries
- **CLI Interface**: Easy-to-use command-line interface
- **Web Interface**: Streamlit-based web application
- **Database Integration**: SQLite storage for persistent data
- **Advanced RL**: Policy gradient training with REINFORCE
- **Deep Validation**: Comprehensive JSON input sanitization

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

Compare different approaches:
```bash
python main.py --prompt "Residential complex" --mode compare
```

Launch web interface:
```bash
python main.py --mode web
```

Use database storage:
```bash
python main.py --prompt "Office building" --mode single --use-db
```

Advanced RL training:
```bash
python main.py --prompt "Smart building" --mode advanced-rl --iterations 3
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

### Example 6: Web Interface
```bash
python main.py --mode web
```

**Expected Behavior:**
- Launches Streamlit web application
- Interactive prompt input interface
- Real-time specification generation
- Multiple modes available in web UI

### Example 7: Database Integration
```bash
python main.py --prompt "Hospital complex" --mode rl --iterations 2 --use-db
```

**Expected Behavior:**
- Saves all specifications to SQLite database
- Persistent storage across runs
- Query with: `python db_query.py`

### Example 8: Advanced RL Training
```bash
python main.py --prompt "Smart office" --mode advanced-rl --iterations 3
```

**Expected Behavior:**
- Policy gradient learning with REINFORCE
- State-action-reward optimization
- Advanced training logs generated

## Project Structure

```
prompt-to-json-backend/
├── main.py                # CLI orchestrator
├── main_agent.py          # Main generation agent
├── evaluator_agent.py     # Evaluation agent
├── rl_loop.py             # Reinforcement learning loop
├── advanced_rl.py         # Advanced RL with policy gradient
├── extractor.py           # Rule-based field extraction
├── schema.py              # Pydantic data models
├── streamlit_app.py       # Web interface
├── database_integration.py # Database storage
├── json_validator.py      # Input validation
├── db_query.py            # Database query tool
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
- **Advanced RL**: `logs/advanced_rl_training_*.json` - Policy gradient training
- **General Logs**: `logs/logs.json` - All prompt-result pairs

### Database
- **Location**: `prompt_to_json.db` (SQLite)
- **Tables**: specifications, evaluations
- **Query Tool**: `python db_query.py`

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

### ✅ Complete Task 3 Implementation
- ✅ **Streamlit Web Interface**: Full web deployment ready
  - Interactive prompt input and real-time results
  - Multiple modes: Single, RL Training, Compare
  - Launch with: `python main.py --mode web`
- ✅ **Advanced RL Environment**: Policy gradient implementation
  - REINFORCE algorithm with policy updates
  - State-action-reward learning loop
  - Run with: `python main.py --mode advanced-rl`
- ✅ **Database Integration**: SQLite implementation ready
  - Persistent storage for specifications and evaluations
  - Query interface for historical data
  - Enable with: `--use-db` flag
- ✅ **Deep JSON Validation**: Comprehensive input sanitization
  - Security validation and XSS prevention
  - Schema validation and type checking
  - Enable with: `--validate-json` flag

### Future Enhancements (Optional)
- **LLM Integration**: GPT-4/LLaMA integration for advanced generation
- **Advanced Databases**: PostgreSQL/MongoDB for enterprise scale
- **Authentication**: User management and access control

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **File Permissions**: Check write permissions for output directories
3. **Invalid Prompts**: Prompts must be 10-1000 characters long

### Debug Mode
Add `--verbose` flag for detailed logging (feature can be added)

## CLI Tools

### Database Query
```bash
# View database contents
python db_query.py
```

### Web Interface
```bash
# Launch Streamlit app
python main.py --mode web
# Or directly:
streamlit run streamlit_app.py
```

### Input Validation
```bash
# Enable deep JSON validation
python main.py --prompt "Building" --validate-json
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
- Basic authentication (no user management)
- SQLite only (no PostgreSQL/MongoDB yet)

### 🚀 Deployment Ready
The system is production-ready for the core prompt-to-JSON conversion task with RL feedback loops. All essential features are implemented and tested.

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

MIT License - see LICENSE file for details