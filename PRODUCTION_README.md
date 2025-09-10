# Production Deployment Guide

## Core Production Files

### Essential Files (Required)
```
├── src/
│   ├── extractor.py         # Core extraction logic
│   └── schema.py            # Pydantic validation
├── evaluator_agent.py       # Spec evaluation
├── data_scorer.py          # Quality scoring
├── rl_loop.py              # RL reward system
├── demo_pipeline.py        # Main pipeline
├── utils.py                # Utilities
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

### Optional Files (Development/Testing)
```
├── advanced_demo.py        # Advanced testing (dev only)
├── test_multi_material.py  # Multi-material tests (dev only)
├── rl_env.py              # RL environment (optional)
├── llm_integration.py     # LLM template (optional)
└── tests/                 # Unit tests (dev only)
```

## Minimal Production Setup

```bash
# Essential files only
pip install pydantic numpy

# Core functionality
python demo_pipeline.py
python rl_loop.py --runs 3
```

## Full Development Setup

```bash
# All features including tests
pip install -r requirements.txt
python -m pytest tests/ -v
python advanced_demo.py
```

## Performance Optimizations

1. **Smart Defaults**: Reduces "standard" dimension issues
2. **Type-Aware Purpose**: Eliminates mismatched assignments
3. **Multi-Material Support**: Handles complex material specs
4. **Numeric Dimension Priority**: Prefers "6 feet" over "lightweight"

## Integration Points

- **LLM Integration**: Use `llm_integration.py` as template
- **RL Environment**: Optional `rl_env.py` for training
- **Custom Evaluation**: Extend `evaluator_agent.py` rules
- **Scoring Logic**: Modify `data_scorer.py` weights