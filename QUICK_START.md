# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Run Web UI

```bash
streamlit run streamlit_review_ui.py
```

Open http://localhost:8501 in your browser.

## CLI Usage

### Unified CLI (aicr.py)

```bash
# Scan files
python aicr.py scan src/

# Review code
python aicr.py review src/

# Apply auto-fixes
python aicr.py apply src/ --dry-run

# Generate reports
python aicr.py report src/ --format html
```

### Specialized CLIs

```bash
# AI Review
python cli_ai_review.py myfile.py --autofix

# Docstring Tools
python cli_docstring.py myfile.py --validate
python cli_docstring.py myfile.py --generate --style google

# Quality Metrics
python cli_metrics.py src/ --export-html report.html

# Evaluation Criteria
python cli_evaluation.py src/
```

## Run Demos

```bash
# AI Review Demo
python demo_ai_review.py

# Docstring Demo
python demo_docstring.py

# Metrics Demo
python demo_metrics.py

# Evaluation Demo
python demo_evaluation.py
```

## Configuration

Edit `pyproject.toml`:

```toml
[tool.ai-code-reviewer]
min_quality_score = 60
max_complexity = 20
min_doc_coverage = 70
```

## Pre-commit Hooks

```bash
# Run manually
pre-commit run --all-files

# Hooks run automatically on commit
git commit -m "Your message"
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=core --cov-report=html
```

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed usage
- Check [README.md](README.md) for features
- Explore the web UI at http://localhost:8501
