# Demo Instructions

This document provides step-by-step instructions for running the Prompt-to-JSON Agent demo applications.

## Prerequisites

Ensure you have Python 3.8+ installed and the project dependencies:

```bash
pip install -r requirements.txt
```

## Command Line Interface (CLI)

### Basic Usage

Run the enhanced CLI with various options:

```bash
# Basic prompt processing
python src/main.py --prompt "Create a wooden dining table"

# Process prompt from file
echo "Design a modern steel chair" > prompt.txt
python src/main.py --prompt-file prompt.txt

# Generate evaluation report
python src/main.py --prompt "Build a glass desk" --save-report

# Run with RL reward computation
python src/main.py --prompt "Create a leather sofa" --run-rl

# Full pipeline with all features
python src/main.py --prompt "Design an eco-friendly bamboo bookshelf" --save-report --run-rl
```

### CLI Flags

- `--prompt`: Direct prompt string input
- `--prompt-file`: Read prompt from text file
- `--save-report`: Generate and save detailed evaluation report
- `--run-rl`: Compute reinforcement learning reward score

### Error Handling

The CLI now includes robust error handling for:
- Invalid JSON parsing
- Missing files
- Empty prompts
- Module import errors
- Keyboard interruption

## Streamlit Web Application

### Installation

Install Streamlit (if not already included):

```bash
pip install streamlit
```

### Running the Web App

Start the Streamlit demo:

```bash
streamlit run src/web_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Web App Features

#### Input Section
- **Text Area**: Enter custom design prompts
- **Example Buttons**: Quick-load common prompts
- **Configuration Sidebar**: Toggle report generation and RL computation

#### Output Tabs

1. **📋 Specification Tab**
   - Generated JSON specification
   - Download button for JSON file
   - Formatted display

2. **🔍 Evaluation Tab**
   - Severity indicator (None/Minor/Major)
   - Critic feedback text
   - List of identified issues

3. **📊 Scores Tab**
   - Overall quality score (0-10)
   - Component scores breakdown
   - Interactive bar chart

4. **🎯 Summary Tab**
   - Input/output summary
   - Validation status
   - Generated file paths
   - RL reward (if enabled)

### Example Prompts

The web app includes these built-in examples:
- "Create a wooden dining table with glass top"
- "Design a modern steel office chair with wheels"
- "Build a 3-floor concrete library with reading rooms"
- "Make a red leather sofa for the living room"
- "Design an eco-friendly bamboo bookshelf"

## Pipeline Components

Both interfaces run the complete pipeline:

1. **Field Extraction**: Parse prompt for basic attributes
2. **Fallback Application**: Fill missing fields with smart defaults
3. **Validation**: Ensure spec meets schema requirements
4. **Evaluation**: Generate critic feedback and identify issues
5. **Scoring**: Compute quality metrics (0-10 scale)
6. **Report Generation**: Create detailed evaluation report (optional)
7. **RL Reward**: Compute reinforcement learning reward (optional)
8. **Logging**: Record interaction for analysis

## Output Files

Generated files are saved to:
- `spec_outputs/`: JSON specifications
- `evaluations/`: Evaluation results
- `reports/`: Detailed evaluation reports (if enabled)
- `logs/`: Interaction logs

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **File Not Found**: Check file paths and permissions
3. **Empty Output**: Verify prompt is not empty
4. **Streamlit Issues**: Try `streamlit run --server.port 8502 src/web_app.py`

### Debug Mode

For detailed error information, run with Python's verbose mode:

```bash
python -v src/main.py --prompt "test prompt"
```

## Performance Notes

- **CLI**: Faster for batch processing and automation
- **Web App**: Better for interactive testing and visualization
- **Pipeline Time**: Typically 1-3 seconds per prompt
- **File Size**: JSON specs are usually < 1KB

## Integration Examples

### Batch Processing

```bash
# Process multiple prompts
for prompt in "table" "chair" "desk"; do
    python src/main.py --prompt "Create a wooden $prompt" --save-report
done
```

### API Integration

The pipeline can be imported and used programmatically:

```python
from src.main import run_pipeline

result = run_pipeline("Create a steel table", save_report=True, run_rl=True)
print(f"Quality score: {result['scores']['format_score']}")
```

## Next Steps

- Explore the generated specifications in `spec_outputs/`
- Review evaluation reports in `reports/`
- Experiment with different prompt styles
- Integrate with your own applications using the pipeline functions