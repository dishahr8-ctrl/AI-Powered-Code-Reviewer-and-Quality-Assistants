"""CLI for Evaluation Criteria"""
import argparse
from pathlib import Path
from core.evaluation_criteria import EvaluationCriteria, run_evaluation


def main():
    parser = argparse.ArgumentParser(description="Evaluation Criteria CLI")
    parser.add_argument("path", help="File or directory to evaluate")
    parser.add_argument("--coverage-report", help="Path to coverage report")
    parser.add_argument("--output", help="Save results to file")
    
    args = parser.parse_args()
    
    # Scan for files
    path_obj = Path(args.path)
    if path_obj.is_file():
        files = [path_obj]
    else:
        files = list(path_obj.rglob("*.py"))
    
    print(f"\n✅ Evaluating {len(files)} file(s)...")
    print("=" * 50)
    
    # Read code samples
    code_samples = []
    for file in files:
        try:
            code = file.read_text()
            code_samples.append(code)
        except Exception as e:
            print(f"❌ Error reading {file.name}: {e}")
    
    # Run evaluation
    result = run_evaluation(
        code_samples=code_samples,
        coverage_report_path=args.coverage_report
    )
    
    # Display results
    summary = result.get_summary()
    print(f"\n{summary}")
    
    # Save to file if requested
    if args.output:
        Path(args.output).write_text(summary)
        print(f"\n✅ Results saved to: {args.output}")
    
    # Exit with appropriate code
    exit(0 if result.meets_criteria else 1)


if __name__ == "__main__":
    main()
