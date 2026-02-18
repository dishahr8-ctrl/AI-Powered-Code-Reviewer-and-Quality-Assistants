"""Demo: AI Code Review with Auto-Fix"""
from core.parser import parse_python
from core.ai_engine_enhanced import generate_enhanced_review
from core.auto_fixer import apply_auto_fixes, generate_fix_report

# Sample code with issues
sample_code = """
def CalculateTotal(items):
    total = 0
    for item in items:
        total += item
    return total

class user_account:
    def __init__(self, name):
        self.userName = name
    
    def GetBalance(self):
        return 0
"""

print("🤖 AI CODE REVIEW DEMO")
print("=" * 60)

# Parse and review
print("\n1️⃣  Parsing code...")
parsed = parse_python(sample_code)
print(f"✅ Found {len(parsed.get('functions', []))} functions and {len(parsed.get('classes', []))} classes")

# Generate review
print("\n2️⃣  Generating AI review...")
reviews = generate_enhanced_review(sample_code, parsed, enable_autofix=True)

# Display issues by severity
critical = [r for r in reviews if r.get('severity') == 'CRITICAL']
warning = [r for r in reviews if r.get('severity') == 'WARNING']
info = [r for r in reviews if r.get('severity') == 'INFO']

print(f"\n📊 Found {len(reviews)} issue(s):")
print(f"   🔴 CRITICAL: {len(critical)}")
print(f"   🟡 WARNING: {len(warning)}")
print(f"   🔵 INFO: {len(info)}")

print("\n📋 Issues:")
for i, review in enumerate(reviews[:10], 1):
    severity_icon = {'CRITICAL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(review.get('severity'), '🔵')
    print(f"\n{i}. {severity_icon} [{review.get('severity')}] {review.get('category', 'general')}")
    print(f"   Message: {review.get('message', '')}")
    if review.get('suggestion'):
        print(f"   💡 Suggestion: {review.get('suggestion')}")
    if review.get('auto_fix'):
        print(f"   🔧 Auto-fix available")

# Apply auto-fixes
print("\n3️⃣  Applying auto-fixes...")
fixable = [r for r in reviews if r.get('auto_fix')]
if fixable:
    fixed_code, applied_fixes = apply_auto_fixes(sample_code, fixable)
    
    print(f"\n✅ Applied {len(applied_fixes)} fix(es):")
    print(generate_fix_report(applied_fixes))
    
    print("\n📝 Fixed Code:")
    print("-" * 60)
    print(fixed_code)
    print("-" * 60)
else:
    print("\nℹ️  No auto-fixable issues found")

print("\n✨ Demo complete!")
