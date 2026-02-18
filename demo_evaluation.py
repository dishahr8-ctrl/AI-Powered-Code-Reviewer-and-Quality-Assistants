"""Demo: Evaluation Criteria"""
from core.evaluation_criteria import EvaluationCriteria, run_evaluation

print("✅ EVALUATION CRITERIA DEMO")
print("=" * 60)

# Sample code
sample_code = """
def calculate_sum(a, b):
    '''Calculate sum of two numbers'''
    return a + b

def multiply(x, y):
    return x * y

class Calculator:
    '''Simple calculator class'''
    def add(self, a, b):
        return a + b
"""

print("\n1️⃣  Parser Accuracy Evaluation")
print("-" * 60)

evaluator = EvaluationCriteria()
success, details = evaluator.evaluate_parser(sample_code)

print(f"Parser Success: {success}")
print(f"Items Parsed: {details['total_items']}")
print(f"Successfully Parsed: {details['successfully_parsed']}")
print(f"Errors: {details['parsing_errors']}")
print(f"Success Rate: {details['success_rate']:.1f}%")

print("\n2️⃣  Docstring Generation Evaluation")
print("-" * 60)

# Simulate docstring generation
evaluator.track_docstring_generation(success=True, count=1)  # multiply function
print(f"Missing Docstrings: 1")
print(f"Generated: 1")
print(f"Generation Rate: 100.0%")

print("\n3️⃣  Coverage Report Evaluation")
print("-" * 60)

evaluator.evaluate_coverage_report(coverage_data={'coverage': 66.7})
print(f"Coverage Report: Generated ✅")
print(f"Coverage: 66.7%")

print("\n4️⃣  Overall Evaluation Result")
print("-" * 60)

result = evaluator.get_evaluation_result()
print(result.get_summary())

print("\n5️⃣  Complete Evaluation")
print("-" * 60)

# Run complete evaluation
complete_result = run_evaluation(
    code_samples=[sample_code],
    coverage_report_path=None
)

print(f"\nMeets Criteria: {complete_result.meets_criteria}")
print(f"Parser Accuracy: {complete_result.parser_success_rate:.1f}% (Target: ≥95%)")
print(f"Docstring Generation: {complete_result.docstring_generation_rate:.1f}% (Target: 100%)")
print(f"Coverage Report: {'Generated' if complete_result.coverage_report_generated else 'Not Generated'}")

print("\n✨ Demo complete!")
