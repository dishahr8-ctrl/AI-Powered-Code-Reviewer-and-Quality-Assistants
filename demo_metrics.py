"""Demo: Quality Metrics"""
from core.quality_metrics import calculate_quality_score

print("📊 QUALITY METRICS DEMO")
print("=" * 60)

# Sample codes with different quality levels
excellent_code = """
def calculate_average(numbers: list) -> float:
    '''
    Calculate the average of a list of numbers.
    
    Args:
        numbers (list): List of numeric values
        
    Returns:
        float: The arithmetic mean
        
    Raises:
        ValueError: If list is empty
    '''
    if not numbers:
        raise ValueError("Empty list")
    return sum(numbers) / len(numbers)
"""

poor_code = """
def calc(x,y,z,a,b,c):
    if x>0:
        if y>0:
            if z>0:
                if a>0:
                    if b>0:
                        return x+y+z+a+b+c
    return 0
"""

# Analyze excellent code
print("\n1️⃣  Excellent Code Example")
print("-" * 60)
metrics1 = calculate_quality_score(excellent_code, "excellent.py")
print(f"Quality Score: {metrics1.quality_score:.1f}/100 (Grade: {metrics1.grade})")
print(f"Maintainability Index: {metrics1.maintainability_index:.1f}/100")
print(f"Cyclomatic Complexity: {metrics1.cyclomatic_complexity}")
print(f"Docstring Coverage: {metrics1.docstring_coverage:.1f}%")
print(f"Code Smells: {metrics1.code_smells}")
print(f"Technical Debt: {metrics1.technical_debt_minutes} minutes")

# Analyze poor code
print("\n2️⃣  Poor Code Example")
print("-" * 60)
metrics2 = calculate_quality_score(poor_code, "poor.py")
print(f"Quality Score: {metrics2.quality_score:.1f}/100 (Grade: {metrics2.grade})")
print(f"Maintainability Index: {metrics2.maintainability_index:.1f}/100")
print(f"Cyclomatic Complexity: {metrics2.cyclomatic_complexity}")
print(f"Docstring Coverage: {metrics2.docstring_coverage:.1f}%")
print(f"Code Smells: {metrics2.code_smells}")
print(f"Technical Debt: {metrics2.technical_debt_minutes} minutes")

# Detailed metrics
print("\n3️⃣  Detailed Metrics")
print("-" * 60)
print(f"\nSize Metrics:")
print(f"  Lines of Code: {metrics1.lines_of_code}")
print(f"  Source Lines: {metrics1.source_lines}")
print(f"  Comment Lines: {metrics1.comment_lines}")
print(f"  Functions: {metrics1.num_functions}")
print(f"  Classes: {metrics1.num_classes}")

print(f"\nComplexity Metrics:")
print(f"  Cyclomatic: {metrics1.cyclomatic_complexity}")
print(f"  Cognitive: {metrics1.cognitive_complexity}")
print(f"  Halstead Volume: {metrics1.halstead_volume:.2f}")
print(f"  Halstead Difficulty: {metrics1.halstead_difficulty:.2f}")

print(f"\nCode Health:")
print(f"  Comment Ratio: {metrics1.comment_ratio:.1%}")
print(f"  Code Smells: {metrics1.code_smells}")
print(f"  Technical Debt: {metrics1.technical_debt_minutes} min")

# Comparison
print("\n4️⃣  Comparison")
print("-" * 60)
improvement = metrics1.quality_score - metrics2.quality_score
print(f"Quality Score Difference: {improvement:+.1f} points")
print(f"Excellent code is {improvement:.1f} points better!")

print("\n✨ Demo complete!")
