"""Test Severity Detection - Shows how errors are ranked"""
from core.parser import parse_python
from core.ai_engine_enhanced import generate_enhanced_review

# Test code with various issues
test_code = """
# CRITICAL: Syntax error
def broken_function()  # Missing colon
    return "error"

# WARNING: Bad naming
def MyFunction():
    pass

# WARNING: Missing docstring
def calculate(x, y):
    return x + y

# WARNING: High complexity
def complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    return a + b + c + d
    return 0

# INFO: Formatting issue
def format_issue(x,y):
    return x+y
"""

print("🔍 SEVERITY DETECTION TEST")
print("=" * 60)

try:
    # Parse and review
    parsed = parse_python(test_code)
    reviews = generate_enhanced_review(test_code, parsed, enable_autofix=True)
    
    # Count by severity
    critical = [r for r in reviews if r.get('severity') == 'CRITICAL']
    warning = [r for r in reviews if r.get('severity') == 'WARNING']
    info = [r for r in reviews if r.get('severity') == 'INFO']
    
    print(f"\n📊 FOUND {len(reviews)} ISSUE(S):")
    print(f"   🔴 CRITICAL: {len(critical)}")
    print(f"   🟡 WARNING: {len(warning)}")
    print(f"   🔵 INFO: {len(info)}")
    
    # Display by severity
    if critical:
        print("\n🔴 CRITICAL ISSUES (Must fix immediately):")
        print("-" * 60)
        for i, issue in enumerate(critical, 1):
            print(f"{i}. {issue.get('message')}")
            if issue.get('suggestion'):
                print(f"   💡 {issue.get('suggestion')}")
            print()
    
    if warning:
        print("\n🟡 WARNING ISSUES (Should fix before merging):")
        print("-" * 60)
        for i, issue in enumerate(warning, 1):
            print(f"{i}. [{issue.get('category')}] {issue.get('message')}")
            if issue.get('suggestion'):
                print(f"   💡 {issue.get('suggestion')}")
            if issue.get('auto_fix'):
                print(f"   🔧 Auto-fix available")
            print()
    
    if info:
        print("\n🔵 INFO ISSUES (Optional improvements):")
        print("-" * 60)
        for i, issue in enumerate(info, 1):
            print(f"{i}. [{issue.get('category')}] {issue.get('message')}")
            if issue.get('suggestion'):
                print(f"   💡 {issue.get('suggestion')}")
            print()

except SyntaxError as e:
    print(f"\n🔴 CRITICAL: Syntax Error Detected!")
    print(f"   {str(e)}")
    print(f"\n   This is a CRITICAL issue that prevents the code from running.")
    print(f"   Fix this before analyzing other issues.")

except Exception as e:
    print(f"\n❌ Error during analysis: {str(e)}")

print("\n" + "=" * 60)
print("✨ Test complete!")
