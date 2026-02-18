# Usage Guide

## Installation

### From Source

```bash
git clone https://github.com/yourusername/ai-code-reviewer.git
cd ai-code-reviewer
pip install -e .
```

### As a Package

```bash
pip install ai-code-reviewer
```

## Quick Start

### Web Interface

```bash
streamlit run streamlit_review_ui.py
```

Then open http://localhost:8501 in your browser.

### Command Line

```bash
# Analyze a single file
python ai_code_reviewer.py myfile.py

# Analyze with specific options
python ai_code_reviewer.py myfile.py --detailed
```

## Web UI Features

### 1. Evaluation Criteria Display
- **Parser Accuracy**: Shows ≥95% success rate requirement
- **Docstring Generation**: Tracks 100% generation for missing cases
- **Coverage Report**: Validates successful report generation
- **Overall Status**: Visual indicators for pass/fail

### 2. Code Input
- **Text Input**: Paste Python code directly
- **PDF Upload**: Extract code from PDF files automatically
- Supports multi-line input
- Syntax highlighting

### 2. Filters & Search
- **Severity Filter**: Filter by CRITICAL, WARNING, INFO
- **Category Filter**: Filter by naming, documentation, formatting, etc.
- **Search**: Find specific issues by keyword
- **Quality Threshold**: Show only files above quality score

### 3. Analysis Results
- Quality Score with letter grade (A-F)
- Maintainability Index
- Cyclomatic Complexity
- Documentation Coverage

### 4. Docstring Tools
- **Style Selection**: Choose Google, NumPy, or reST
- **Auto-Generation**: Generate missing docstrings
- **Validation**: Check completeness
- **pydocstyle**: Style compliance checks

### 5. Issue Management
- Paginated issue list (10 per page)
- Expandable issue details
- Auto-fix suggestions
- Line number references

## Configuration

### pyproject.toml

```toml
[tool.ai-code-reviewer]
min_quality_score = 60
max_complexity = 20
min_doc_coverage = 70
fail_on_severity = "CRITICAL"

# Evaluation criteria
parser_success_threshold = 95.0
docstring_generation_threshold = 100.0
require_coverage_report = true

[tool.pydocstyle]
convention = "google"

[tool.black]
line-length = 100
```

## Evaluation Criteria

The tool validates three key metrics:

### 1. Parser Accuracy ≥95%
- Extracts functions and classes without errors
- Handles complex Python syntax
- Tracks success rate

**Check**:
```bash
python -c "from core.evaluation_criteria import EvaluationCriteria; e = EvaluationCriteria(); e.evaluate_parser(code); print(e.get_evaluation_result())"
```

### 2. Docstring Generation 100%
- Generates baseline docstrings for all missing cases
- Supports Google, NumPy, reST styles
- Includes all sections (Args, Returns, Raises, Yields, Attributes)

**Check**:
```python
from core.docstring_generator import generate_docstring, DocstringStyle
docstring = generate_docstring(func_info, DocstringStyle.GOOGLE)
```

### 3. Coverage Report Generated
- Successfully generates coverage reports
- Tracks documentation percentage
- Validates completeness

**Check**:
```python
from core.docstring_validator import calculate_docstring_coverage
coverage = calculate_docstring_coverage(code)
print(f"Coverage: {coverage['coverage']}%")
```

## Pre-commit Integration

### Setup

```bash
pip install pre-commit
pre-commit install
```

### Configuration

Edit `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest
        entry: pytest
        language: system
        args: ['--cov=core', '--cov-fail-under=80']
```

### Usage

```bash
# Run on all files
pre-commit run --all-files

# Run on staged files
git commit  # Hooks run automatically
```

## CI/CD Integration

### GitHub Actions

The `.github/workflows/ci.yml` workflow:
- Tests on Python 3.8-3.11
- Enforces 80% coverage
- Runs linting and formatting
- Validates docstrings

### Customization

Edit `.github/workflows/ci.yml` to:
- Add more Python versions
- Change coverage threshold
- Add deployment steps

## Examples

### Example 1: Basic Analysis

```python
def calculate_sum(a, b):
    return a + b
```

Results:
- Quality Score: 64.2/100 (Grade: D)
- Issues: Missing docstring
- Suggestion: Add Google-style docstring

### Example 2: With Docstring

```python
def calculate_sum(a, b):
    """Calculate the sum of two numbers.
    
    Args:
        a (int): First number
        b (int): Second number
    
    Returns:
        int: Sum of a and b
    """
    return a + b
```

Results:
- Quality Score: 85.3/100 (Grade: B)
- Issues: None
- Documentation: 100%

### Example 3: Complex Function

```python
def process_data(data, threshold=10):
    """Process data with threshold.
    
    Args:
        data (list): Input data
        threshold (int): Processing threshold
    
    Returns:
        list: Processed data
    
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    result = []
    for item in data:
        if item > threshold:
            result.append(item * 2)
    return result
```

Results:
- Quality Score: 92.1/100 (Grade: A)
- Complexity: 3
- Documentation: 100%

## Tips & Best Practices

### 1. Documentation
- Always add docstrings to public functions
- Include all parameters and return values
- Document exceptions with Raises section

### 2. Code Quality
- Keep functions under 50 lines
- Limit parameters to 5 or fewer
- Avoid deep nesting (max 4 levels)

### 3. Testing
- Maintain 80%+ code coverage
- Test edge cases
- Use pytest fixtures

### 4. Pre-commit
- Run hooks before pushing
- Fix issues locally first
- Keep commits clean

## Troubleshooting

### Issue: Import errors
**Solution**: Install all dependencies
```bash
pip install -r requirements.txt
```

### Issue: Coverage too low
**Solution**: Add more tests
```bash
pytest --cov=core --cov-report=html
# Open htmlcov/index.html to see gaps
```

### Issue: Pre-commit fails
**Solution**: Run checks manually
```bash
black .
flake8 .
pytest
```

## Support

- GitHub Issues: https://github.com/yourusername/ai-code-reviewer/issues
- Documentation: https://github.com/yourusername/ai-code-reviewer#readme
