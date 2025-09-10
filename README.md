# Prompt-to-JSON Agent

A Python agent that converts natural language prompts into structured JSON outputs using AI models.

## Development Plan

### Day 1 — Setup & repo skeleton (6–8 hrs)
- [x] Create GitHub repo and clone
- [x] Create virtual environment
- [x] Install core dependencies
- [x] Create folder structure
- [x] Initialize basic files

## Project Structure

```
prompt-to-json-agent/
├── src/                 # Source code
├── data/               # Data files
│   ├── logs.json      # Application logs
│   └── spec_outputs/  # Generated specifications
├── tests/             # Test files
├── docs/              # Documentation
├── venv/              # Virtual environment
└── requirements.txt   # Python dependencies
```

## Setup

1. Clone the repository
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

## Testing

Run tests with pytest:
```bash
python -m pytest tests/ -v
```