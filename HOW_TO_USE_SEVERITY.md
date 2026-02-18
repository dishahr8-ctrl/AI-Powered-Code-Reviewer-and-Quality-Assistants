# How to Use Severity Detection

## What is Severity Ranking?

The AI Code Reviewer automatically ranks all issues by severity to help you prioritize fixes:

- 🔴 **CRITICAL**: Must fix immediately (prevents code from running)
- 🟡 **WARNING**: Should fix before merging (affects quality)
- 🔵 **INFO**: Optional improvements (nice to have)

## Quick Start

### 1. Analyze Your Code

**Web UI:**
```
1. Open http://localhost:8501
2. Paste your code or upload PDF
3. Click "Analyze Code"
4. See issues ranked by severity
```

**CLI:**
```bash
python cli_ai_review.py your_file.py
```

### 2. Understanding the Output

```
🔍 AI CODE REVIEW: your_file.py
==================================================
Found 10 issue(s):
  🔴 CRITICAL: 1    ← Fix these first!
  🟡 WARNING: 7     ← Fix before merging
  🔵 INFO: 2        ← Optional improvements
```

## Severity Levels Explained

### 🔴 CRITICAL (Fix Immediately)

**What it means:** Your code won't run or has serious bugs

**Examples:**
```python
# Syntax error - missing colon
def my_function()
    return "error"

# Undefined variable
def calculate():
    return undefined_var + 1

# Division by zero
def divide():
    return 10 / 0
```

**What to do:**
1. Fix these FIRST before anything else
2. Your code won't work until these are fixed
3. Run the code again after fixing

### 🟡 WARNING (Fix Before Merging)

**What it means:** Code works but has quality issues

**Examples:**
```python
# Bad naming
def MyFunction():  # Should be my_function
    pass

# Missing documentation
def calculate(x, y):  # No docstring
    return x + y

# Too complex
def complex(a, b, c, d, e):  # Too many parameters
    if a > 0:
        if b > 0:
            if c > 0:  # Too much nesting
                return a + b + c
```

**What to do:**
1. Fix these before committing code
2. They affect code maintainability
3. Use auto-fix for simple issues

### 🔵 INFO (Optional Improvements)

**What it means:** Minor style issues

**Examples:**
```python
# Spacing issues
def calculate(x,y):  # Missing spaces
    return x+y

# Trailing whitespace
def test():
    x = 1   # Extra spaces
    return x
```

**What to do:**
1. Fix when you have time
2. Use auto-fix to clean up
3. Not urgent

## Using in Web UI

### Step 1: Upload/Paste Code

```python
# Example code with issues
def CalculateTotal(items):  # WARNING: Bad naming
    total = 0
    for item in items:
        total += item
    return total
```

### Step 2: View Results

The UI shows:
- **Evaluation Criteria** (top)
- **Quality Metrics** (scores)
- **Issues by Severity** (with counts)
- **Detailed Issue List** (expandable)

### Step 3: Filter by Severity

Use the sidebar filter:
- Select "CRITICAL" to see only critical issues
- Select "WARNING" to see warnings
- Select "INFO" to see minor issues

### Step 4: Export Report

Select export format (CSV/HTML/JSON) to save results

## Using in CLI

### Show All Issues

```bash
python cli_ai_review.py myfile.py
```

### Show Only Critical

```bash
python cli_ai_review.py myfile.py --severity CRITICAL
```

### Show Warnings and Above

```bash
python cli_ai_review.py myfile.py --severity WARNING
```

### Apply Auto-Fix

```bash
# Preview fixes
python cli_ai_review.py myfile.py --preview

# Apply fixes
python cli_ai_review.py myfile.py --autofix
```

## Real Example

### Input Code

```python
def CalculateTotal(items):
    total = 0
    for item in items:
        total += item
    return total

class user_account:
    def GetBalance(self):
        return 0
```

### Output

```
🔍 AI CODE REVIEW
==================================================
Found 6 issue(s):
  🔴 CRITICAL: 0
  🟡 WARNING: 6
  🔵 INFO: 0

🟡 WARNING Issues:

1. [naming] Function 'CalculateTotal' should use snake_case
   💡 Rename to 'calculate_total'
   🔧 Auto-fix available

2. [naming] Class 'user_account' should use PascalCase
   💡 Rename to 'UserAccount'
   🔧 Auto-fix available

3. [naming] Function 'GetBalance' should use snake_case
   💡 Rename to 'get_balance'
   🔧 Auto-fix available

4. [documentation] Function 'CalculateTotal' missing docstring
   💡 Add docstring
   🔧 Auto-fix available

5. [documentation] Function '__init__' missing docstring
   💡 Add docstring
   🔧 Auto-fix available

6. [documentation] Function 'GetBalance' missing docstring
   💡 Add docstring
   🔧 Auto-fix available
```

## Priority Guide

### 1. Fix CRITICAL First

```bash
# Show only critical issues
python cli_ai_review.py myfile.py --severity CRITICAL

# Fix them manually
# Run again to verify
```

### 2. Then Fix WARNINGS

```bash
# Show warnings
python cli_ai_review.py myfile.py --severity WARNING

# Use auto-fix for simple issues
python cli_ai_review.py myfile.py --autofix
```

### 3. Finally Fix INFO

```bash
# Show all issues
python cli_ai_review.py myfile.py

# Clean up formatting
python cli_ai_review.py myfile.py --autofix
```

## Tips

### ✅ DO:
- Fix CRITICAL issues immediately
- Address WARNINGS before committing
- Use auto-fix for simple issues
- Review auto-fixes before applying

### ❌ DON'T:
- Ignore CRITICAL issues
- Commit code with many WARNINGS
- Apply auto-fix without reviewing
- Skip testing after fixes

## Testing Your Code

### Test File

Create `example_code_with_issues.py`:

```python
# WARNING: Bad naming
def MyFunction():
    pass

# WARNING: Missing docstring
def calculate(x, y):
    return x + y

# INFO: Formatting
def format_issue(x,y):
    return x+y
```

### Run Analysis

```bash
python cli_ai_review.py example_code_with_issues.py
```

### See Results

You'll see issues ranked by severity with suggestions!

## Summary

The severity ranking helps you:
- ✅ Prioritize fixes (CRITICAL → WARNING → INFO)
- ✅ Understand issue importance
- ✅ Focus on what matters most
- ✅ Improve code quality systematically

Start with CRITICAL, move to WARNING, then INFO! 🎯
