# AI Code Reviewer

Comprehensive Python code analysis tool with AI-powered review, quality metrics, and advanced docstring management.

## Features

### Evaluation Criteria

The tool validates three key performance indicators:

1. **Parser Accuracy ≥95%**
   - Extracts functions and classes without errors
   - Handles complex Python syntax
   - Tracks parsing success rate

2. **Docstring Generation 100%**
   - Generates baseline docstrings for all missing cases
   - Supports Google, NumPy, and reST styles
   - Includes Args, Returns, Raises, Yields, Attributes

3. **Coverage Report Generated**
   - Successfully generates coverage reports
   - Tracks documentation coverage percentage
   - Validates completeness

### Code Analysis
- AI-powered code review with severity ranking
- Quality metrics (Maintainability Index, Complexity, etc.)
- Auto-fix capabilities
- Multi-format reports (HTML, CSV, JSON)

### Docstring Synthesis & Validation
- **Multi-style support**: Google, NumPy, and reST formats
- **Auto-generation**: Generate missing docstrings with proper structure
- **Advanced sections**: Raises, Yields, and Attributes support
- **Validation**: Check completeness and style compliance
- **pydocstyle integration**: Automated style checking
- **Coverage reporting**: Track documentation progress

### Validation & Metrics
- **Quality Scores**: Per-file and overall code quality evaluation (0-100)
- **Maintainability Index**: Industry-standard MI metric with ratings
- **Complexity Metrics**: Cyclomatic, Cognitive, Halstead metrics
- **Coverage Tracking**: Documentation and test coverage hints
- **Code Health**: Code smells and technical debt estimation
- **Export Reports**: CSV, HTML, and JSON formats
- **Trend Analysis**: Track quality over time

### Workflow & CI Integration
- **Pre-commit hooks**: Automatic code quality checks before commits
- **CI/CD workflows**: GitHub Actions with coverage enforcement
- **Configuration**: Centralized settings via `pyproject.toml`
- **Streamlit UI**: Interactive web interface for code review

### AI Review Engine
- **LLM-based prompts**: Human-like code feedback generation
- **Severity ranking**: Issues categorized as CRITICAL, WARNING, INFO
- **Auto-fix capabilities**: Automatically fix naming, docstrings, spacing
- **Smart suggestions**: Context-aware improvement recommendations

### Interface
- Modern web UI (Streamlit)
- Command-line tools
- CI/CD integration ready

## Quick Start

### Installation

#### From PyPI (when published)
```bash
pip install ai-code-reviewer
```

#### From Source
```bash
git clone https://github.com/yourusername/ai-code-reviewer.git
cd ai-code-reviewer
pip install -e .
```

### Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks
pip install pre-commit
pre-commit install

# Run web UI
streamlit run streamlit_review_ui.py

# Or use CLI
python ai_code_reviewer.py <file.py>
```

### Web UI Features

- **Multi-Language Support**: Python, Java, C++, JavaScript, Go, Rust
- **PDF Upload**: Extract and analyze code from PDF files
- **Text Input**: Paste code directly into the editor
- **Quality Metrics Dashboard**: Real-time quality scores and grades
- **Maintainability Index**: Industry-standard MI with ratings
- **Complexity Tracking**: Cyclomatic, Cognitive, Halstead metrics
- **Advanced Filters**: Filter by severity, category, and quality score
- **Search**: Find specific issues by keyword
- **Pagination**: Navigate through large issue lists
- **Tooltips**: Helpful hints on all controls
- **Auto-fix Preview**: View and download fixed code
- **Line Numbers**: Jump to specific issues in code
- **LLM Prompts**: View AI prompt templates
- **Severity Ranking**: Visual indicators for CRITICAL, WARNING, INFO
- **Export Reports**: Download CSV, HTML, or JSON reports
- **Download Fixed Code**: One-click download of auto-fixed code

## Docstring Features

### Supported Styles

**Google Style:**
```python
def function(arg1, arg2):
    """Brief description.
    
    Args:
        arg1 (type): Description
        arg2 (type): Description
    
    Returns:
        type: Description
    
    Raises:
        ValueError: Description
    """
```

**NumPy Style:**
```python
def function(arg1, arg2):
    """Brief description.
    
    Parameters
    ----------
    arg1 : type
        Description
    arg2 : type
        Description
    
    Returns
    -------
    type
        Description
    
    Raises
    ------
    ValueError
        Description
    """
```

**reST Style:**
```python
def function(arg1, arg2):
    """Brief description.
    
    :param arg1: Description
    :type arg1: type
    :param arg2: Description
    :type arg2: type
    :return: Description
    :rtype: type
    :raises ValueError: Description
    """
```

### Web UI Features

1. **Style Selection**: Choose your preferred docstring format
2. **Auto-Detection**: Identifies existing docstring style
3. **Generation**: One-click generation of missing docstrings
4. **Validation**: Real-time completeness checking
5. **pydocstyle**: Integrated style compliance checks
6. **Coverage Tracking**: Monitor documentation progress

## Configuration

### pyproject.toml

All settings are centralized in `pyproject.toml`:

```toml
[tool.ai-code-reviewer]
# Quality thresholds
min_quality_score = 60
max_complexity = 20
min_doc_coverage = 70

# CI/CD settings
fail_on_severity = "CRITICAL"
severity_levels = ["CRITICAL", "WARNING", "INFO"]

# Auto-fix settings
autofix_enabled = true
autofix_categories = ["naming", "formatting", "documentation"]

# Code smell detection
detect_code_smells = true
max_function_length = 50
max_parameters = 5
max_nesting_depth = 4

[tool.pytest.ini_options]
addopts = [
    "--cov=core",
    "--cov-fail-under=80",
]

[tool.pydocstyle]
convention = "google"  # or "numpy"

[tool.black]
line-length = 100
```

### Pre-commit Hooks

Install and configure:

```bash
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

Hooks include:
- Black (code formatting)
- Flake8 (linting)
- pydocstyle (docstring style)
- pytest (tests with 80% coverage)
- mypy (type checking)

### CI/CD Workflow

GitHub Actions workflow automatically:
- Tests on Python 3.8, 3.9, 3.10, 3.11
- Enforces 80% code coverage
- Runs linting and formatting checks
- Validates docstring style
- Uploads coverage to Codecov

## Requirements

```bash
pip install -r requirements.txt
```

## Documentation

- [Usage Guide](USAGE.md) - Detailed usage instructions
- [How to Use Severity Detection](HOW_TO_USE_SEVERITY.md) - Understand error ranking
- [AI Review Engine](AI_REVIEW_ENGINE.md) - LLM-based code review features
- [Validation & Metrics](VALIDATION_METRICS.md) - Complete metrics guide
- [Quick Start](QUICK_START.md) - Get started quickly
- [API Documentation](docs/API.md) - API reference (coming soon)
- [Contributing](CONTRIBUTING.md) - Contribution guidelines (coming soon)

## Publishing

### Build Package

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Check distribution
twine check dist/*
```

### Publish to PyPI

```bash
# Test PyPI
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

## Testing

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=core --cov-report=html

# Specific test file
pytest tests/test_parser.py
```

### Edge Cases Covered

- Empty files
- Syntax errors
- Missing docstrings
- Complex nested functions
- Generator functions (Yields)
- Class methods and properties (Attributes)
- Multiple inheritance
- Async functions
- Exception handling (Raises)

### Evaluation Criteria Tests

```bash
# Run evaluation tests
pytest tests/test_evaluation_criteria.py -v

# Check parser accuracy
python -c "from core.evaluation_criteria import EvaluationCriteria; e = EvaluationCriteria(); print(e.get_evaluation_result())"
```

## Evaluation Criteria Details

### 1. Parser Accuracy (≥95%)

**Objective**: Extract functions and classes with at least 95% success rate

**Metrics**:
- Total items parsed
- Successfully parsed items
- Parsing errors
- Success rate calculation

**Example**:
```python
from core.evaluation_criteria import EvaluationCriteria

evaluator = EvaluationCriteria()
evaluator.evaluate_parser(code)
result = evaluator.get_evaluation_result()
print(f"Parser accuracy: {result.parser_success_rate}%")
```

### 2. Docstring Generation (100%)

**Objective**: Generate baseline docstrings for all missing documentation

**Metrics**:
- Missing docstrings identified
- Docstrings successfully generated
- Generation failures
- Generation rate

**Example**:
```python
from core.docstring_generator import generate_docstring, DocstringStyle

func_info = extract_function_info(node)
docstring = generate_docstring(func_info, DocstringStyle.GOOGLE)
```

### 3. Coverage Report

**Objective**: Successfully generate code coverage reports

**Metrics**:
- Report generation success
- Coverage percentage
- Documented vs undocumented items

**Example**:
```python
from core.docstring_validator import calculate_docstring_coverage

coverage = calculate_docstring_coverage(code)
print(f"Coverage: {coverage['coverage']}%")
```

## AI Review Engine

### LLM-Based Prompts

The tool uses sophisticated prompt templates to generate human-like feedback:

```python
from core.llm_prompts import generate_review_prompt, SYSTEM_PROMPT

# System prompt defines the AI reviewer persona
print(SYSTEM_PROMPT)

# Generate context-aware review prompt
prompt = generate_review_prompt(code, parsed_data, focus="naming")
```

**Available Prompt Types**:
- General review
- Naming conventions
- Documentation quality
- Complexity analysis
- Security review
- Performance optimization

### Severity Ranking

Issues are automatically ranked by severity:

**🔴 CRITICAL**: Prevents code from running
- Syntax errors
- Import errors
- Blocking issues

**🟡 WARNING**: Affects maintainability
- Naming convention violations
- Missing documentation
- High complexity
- Code smells

**🔵 INFO**: Minor improvements
- Style suggestions
- Formatting issues
- Optional optimizations

### Auto-Fix Capabilities

Automatically fixes simple issues:

**Fixable Categories**:
- **Naming**: Convert to snake_case/PascalCase
- **Documentation**: Generate docstring templates
- **Formatting**: Fix spacing and whitespace

**Example**:
```python
from core.auto_fixer import apply_auto_fixes

fixed_code, applied_fixes = apply_auto_fixes(code, reviews)
print(f"Applied {len(applied_fixes)} fixes")
```

**Auto-Fix Report**:
```
Applied 3 fix(es):
✓ Renamed 'MyFunction' to 'my_function'
✓ Added docstring to 'calculate'
✓ Removed trailing whitespace
```

## License

MIT
