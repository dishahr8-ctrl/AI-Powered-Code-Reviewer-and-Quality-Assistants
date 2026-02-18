# AI Review Engine

## Overview

The AI Review Engine uses LLM-based prompt templates to generate human-like code feedback, automatically ranks findings by severity, and can optionally auto-fix simple issues.

## Features

### 1. LLM-Based Prompt Templates

The engine uses sophisticated prompt templates to generate contextual, human-like feedback.

#### System Prompt

Defines the AI reviewer persona:

```
You are an expert code reviewer with deep knowledge of software engineering best practices.
Your role is to provide constructive, actionable feedback on code quality.

Focus on:
- Code clarity and maintainability
- Potential bugs and edge cases
- Performance considerations
- Security vulnerabilities
- Best practices and design patterns

Provide specific, actionable suggestions with examples when possible.
```

#### Review Prompts

**General Review:**
```python
from core.llm_prompts import generate_review_prompt

prompt = generate_review_prompt(code, parsed_data)
# Generates context-aware review prompt with code analysis
```

**Focused Reviews:**
- **Naming**: PEP 8 naming conventions
- **Documentation**: Docstring quality
- **Complexity**: Code complexity analysis
- **Security**: Vulnerability detection
- **Performance**: Optimization opportunities

#### Example Usage

```python
from core.llm_prompts import generate_review_prompt, SYSTEM_PROMPT
from core.parser import parse_python

code = """
def CalculateTotal(items):
    total = 0
    for item in items:
        total += item
    return total
"""

parsed = parse_python(code)
prompt = generate_review_prompt(code, parsed, focus="naming")

print(SYSTEM_PROMPT)
print(prompt)
```

### 2. Severity Ranking

Issues are automatically ranked by severity to help prioritize fixes.

#### Severity Levels

**🔴 CRITICAL** - Prevents code from running
- Syntax errors
- Import errors
- Blocking issues
- Security vulnerabilities

**Example:**
```python
def broken_function()  # Missing colon
    return "error"
```

**🟡 WARNING** - Affects maintainability
- Naming convention violations
- Missing documentation
- High complexity (>10)
- Code smells
- Potential bugs

**Example:**
```python
def MyFunction():  # Should be snake_case
    pass

def complex_function(a, b, c, d, e, f):  # Too many parameters
    if a > 0:
        if b > 0:
            if c > 0:  # Deep nesting
                return a + b + c
```

**🔵 INFO** - Minor improvements
- Style suggestions
- Formatting issues
- Optional optimizations
- Best practice recommendations

**Example:**
```python
def calculate(x,y):  # Missing spaces after commas
    return x+y  # Missing spaces around operator
```

#### Severity Assignment Logic

```python
def assign_severity(issue_type, details):
    if issue_type == "syntax_error":
        return "CRITICAL"
    elif issue_type == "naming_violation":
        return "WARNING"
    elif issue_type == "formatting":
        return "INFO"
    # ... more logic
```

#### Filtering by Severity

```bash
# CLI: Show only critical issues
python cli_ai_review.py myfile.py --severity CRITICAL

# CLI: Show warnings and above
python cli_ai_review.py myfile.py --severity WARNING
```

### 3. Auto-Fix Capabilities

Automatically fixes simple, safe issues without changing logic.

#### Fixable Issue Categories

**1. Naming Conventions**

Converts to proper naming style:

```python
# Before
def MyFunction():
    pass

class user_account:
    pass

# After auto-fix
def my_function():
    pass

class UserAccount:
    pass
```

**2. Docstrings**

Generates basic docstring templates:

```python
# Before
def calculate_sum(a, b):
    return a + b

# After auto-fix
def calculate_sum(a, b):
    """
    TODO: Add description for calculate_sum.
    
    Args:
        a: TODO: Add description
        b: TODO: Add description
        
    Returns:
        TODO: Add return description
    """
    return a + b
```

**3. Spacing and Formatting**

Fixes whitespace issues:

```python
# Before
def calculate(x,y):
    return x+y

# After auto-fix
def calculate(x, y):
    return x + y
```

#### Using Auto-Fix

**CLI:**
```bash
# Preview fixes
python cli_ai_review.py myfile.py --preview

# Apply fixes
python cli_ai_review.py myfile.py --autofix

# Save to different file
python cli_ai_review.py myfile.py --autofix --output fixed.py
```

**Python API:**
```python
from core.auto_fixer import apply_auto_fixes, generate_fix_report
from core.ai_engine_enhanced import generate_enhanced_review
from core.parser import parse_python

code = """
def BadName():
    pass
"""

parsed = parse_python(code)
reviews = generate_enhanced_review(code, parsed, enable_autofix=True)

# Apply fixes
fixed_code, applied_fixes = apply_auto_fixes(code, reviews)

# Generate report
report = generate_fix_report(applied_fixes)
print(report)
```

#### Auto-Fix Report

```
Applied 3 fix(es):
✓ Renamed 'MyFunction' to 'my_function' (naming)
✓ Added docstring to 'calculate' (documentation)
✓ Removed trailing whitespace (formatting)
```

#### Safety Features

- **Preview Mode**: See changes before applying
- **Backup**: Original code preserved
- **Selective**: Choose which categories to fix
- **Reversible**: Changes can be undone

## Analysis Categories

### 1. Naming Conventions

**Checks:**
- Function names (snake_case)
- Class names (PascalCase)
- Variable names (snake_case)
- Constants (UPPER_CASE)

**Example Issues:**
```python
# Bad
def MyFunction():  # Should be my_function
    pass

class my_class:  # Should be MyClass
    pass

MY_VARIABLE = 1  # Should be my_variable (not a constant)
```

### 2. Documentation

**Checks:**
- Missing docstrings
- Incomplete docstrings
- Docstring quality
- Parameter documentation

**Example Issues:**
```python
# Missing docstring
def calculate(x, y):
    return x + y

# Incomplete docstring
def process(data, threshold):
    """Process data."""  # Missing Args and Returns
    return [x for x in data if x > threshold]
```

### 3. Complexity

**Checks:**
- Cyclomatic complexity
- Function length
- Nesting depth
- Number of parameters

**Example Issues:**
```python
# High complexity (6)
def complex_function(a, b, c, d, e):  # Too many parameters
    if a > 0:
        if b > 0:
            if c > 0:  # Deep nesting
                if d > 0:
                    return a + b + c + d
```

### 4. Formatting

**Checks:**
- Trailing whitespace
- Line length
- Blank lines
- Spacing around operators

**Example Issues:**
```python
# Bad formatting
def calculate(x,y):  # Missing spaces
    result=x+y  # Missing spaces
    return result   # Trailing whitespace
```

### 5. Best Practices

**Checks:**
- Error handling
- Resource management
- Type hints
- Design patterns

**Example Issues:**
```python
# Missing error handling
def divide(a, b):
    return a / b  # What if b is 0?

# Missing type hints
def calculate(x, y):  # Should specify types
    return x + y
```

## Integration Examples

### CLI Integration

```bash
# Basic review
python cli_ai_review.py myfile.py

# With auto-fix
python cli_ai_review.py myfile.py --autofix

# Filter by severity
python cli_ai_review.py myfile.py --severity WARNING

# Filter by category
python cli_ai_review.py myfile.py --category naming

# Show LLM prompt
python cli_ai_review.py myfile.py --prompt
```

### Python API Integration

```python
from core.ai_engine_enhanced import generate_enhanced_review
from core.parser import parse_python
from core.auto_fixer import apply_auto_fixes

# Analyze code
code = open('myfile.py').read()
parsed = parse_python(code)
reviews = generate_enhanced_review(code, parsed, enable_autofix=True)

# Filter by severity
critical = [r for r in reviews if r['severity'] == 'CRITICAL']
warnings = [r for r in reviews if r['severity'] == 'WARNING']

# Apply auto-fixes
fixable = [r for r in reviews if r.get('auto_fix')]
if fixable:
    fixed_code, applied = apply_auto_fixes(code, fixable)
    print(f"Applied {len(applied)} fixes")
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ai-review
        name: AI Code Review
        entry: python cli_ai_review.py
        language: system
        types: [python]
        args: ['--severity', 'CRITICAL']
```

### CI/CD Pipeline

```yaml
# .github/workflows/code-review.yml
- name: AI Code Review
  run: |
    python cli_ai_review.py src/*.py --severity WARNING
    if [ $? -ne 0 ]; then
      echo "Code review found issues!"
      exit 1
    fi
```

## Review Output Format

Each review item contains:

```python
{
    "severity": "WARNING",           # CRITICAL, WARNING, or INFO
    "category": "naming",            # naming, documentation, etc.
    "message": "Function 'MyFunc' should use snake_case",
    "line_number": 10,               # Optional: line number
    "suggestion": "Rename to 'my_func'",
    "auto_fix": "def my_func():"     # Optional: auto-fix code
}
```

## Best Practices

### 1. Review Workflow

```bash
# 1. Run basic review
python cli_ai_review.py myfile.py

# 2. Preview fixes
python cli_ai_review.py myfile.py --preview

# 3. Apply fixes
python cli_ai_review.py myfile.py --autofix

# 4. Review changes
git diff myfile.py

# 5. Commit
git commit -m "Applied AI review fixes"
```

### 2. Severity Handling

- Always fix CRITICAL issues first
- Address WARNING issues before merging
- INFO issues are optional improvements

### 3. Auto-Fix Safety

- Always preview fixes before applying
- Review auto-generated docstrings
- Test code after auto-fixes
- Use version control

### 4. Custom Configuration

```toml
# pyproject.toml
[tool.ai-code-reviewer]
# Severity thresholds
fail_on_severity = "CRITICAL"
severity_levels = ["CRITICAL", "WARNING", "INFO"]

# Auto-fix settings
autofix_enabled = true
autofix_categories = ["naming", "formatting", "documentation"]

# Complexity thresholds
max_complexity = 10
max_parameters = 5
max_nesting_depth = 4
```

## Limitations

### Current Auto-Fix Limitations

- Cannot fix complex logic errors
- Docstrings are templates (need manual completion)
- Some naming fixes may need manual review
- Cannot refactor complex code

### Future Enhancements

- Integration with actual LLM APIs (GPT-4, Claude, etc.)
- More sophisticated auto-fixes
- Context-aware docstring generation
- Automated refactoring suggestions
- Security vulnerability detection
- Performance profiling integration

## Demo

Run the demo to see the AI Review Engine in action:

```bash
python demo_ai_review.py
```

Output:
```
🤖 AI CODE REVIEW DEMO
============================================================

1️⃣  Parsing code...
✅ Found 1 functions and 1 classes

2️⃣  Generating AI review...

📊 Found 10 issue(s):
   🔴 CRITICAL: 0
   🟡 WARNING: 9
   🔵 INFO: 1

📋 Issues:

1. 🟡 [WARNING] naming
   Message: Function 'CalculateTotal' should use snake_case
   💡 Suggestion: Rename to 'calculate_total'
   🔧 Auto-fix available

3️⃣  Applying auto-fixes...

✅ Applied 6 fix(es):
✓ Renamed 'CalculateTotal' to 'calculate_total'
✓ Renamed 'user_account' to 'UserAccount'
✓ Added docstring to 'calculate_total'

✨ Demo complete!
```

## Summary

The AI Review Engine provides:

✅ **Human-like feedback** using LLM-based prompts
✅ **Severity ranking** (CRITICAL, WARNING, INFO)
✅ **Auto-fix capabilities** for simple issues
✅ **Multiple analysis categories**
✅ **Safe, reversible changes**
✅ **CLI and API integration**
✅ **CI/CD ready**

Use it to maintain high code quality and catch issues early!
