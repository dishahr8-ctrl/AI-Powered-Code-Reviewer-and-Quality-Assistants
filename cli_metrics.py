"""CLI for Quality Metrics"""
import argparse
from pathlib import Path
from core.quality_metrics import calculate_quality_score
from core.report_exporter import export_html_report, export_csv_report, export_json_report, print_metrics_summary


def main():
    parser = argparse.ArgumentParser(description="Quality Metrics CLI")
    parser.add_argument("path", help="File or directory to analyze")
    parser.add_argument("--detailed", action="store_true", help="Show detailed metrics")
    parser.add_argument("--export-html", help="Export HTML report")
    parser.add_argument("--export-csv", help="Export CSV report")
    parser.add_argument("--export-json", help="Export JSON report")
    parser.add_argument("--min-quality", type=int, help="Minimum quality score filter")
    parser.add_argument("--max-complexity", type=int, help="Maximum complexity filter")
    parser.add_argument("--project-name", default="Code Quality Report", help="Project name for reports")
    
    args = parser.parse_args()
    
    # Scan for files
    path_obj = Path(args.path)
    if path_obj.is_file():
        files = [path_obj]
    else:
        files = list(path_obj.rglob("*.py"))
    
    print(f"\n📊 Analyzing {len(files)} file(s)...")
    print("=" * 50)
    
    # Calculate metrics
    metrics_list = []
    for file in files:
        try:
            code = file.read_text()
            metrics = calculate_quality_score(code, str(file))
            
            # Apply filters
            if args.min_quality and metrics.quality_score < args.min_quality:
                continue
            if args.max_complexity and metrics.cyclomatic_complexity > args.max_complexity:
                continue
            
            metrics_list.append(metrics)
            
            # Print summary
            print(f"\n📄 {file.name}")
            print(f"   Quality Score: {metrics.quality_score:.1f}/100 (Grade: {metrics.grade})")
            print(f"   Maintainability: {metrics.maintainability_index:.1f}/100")
            print(f"   Complexity: {metrics.cyclomatic_complexity}")
            print(f"   Doc Coverage: {metrics.docstring_coverage:.1f}%")
            
            if args.detailed:
                print(f"   Lines of Code: {metrics.lines_of_code}")
                print(f"   Functions: {metrics.num_functions}")
                print(f"   Classes: {metrics.num_classes}")
                print(f"   Code Smells: {metrics.code_smells}")
                print(f"   Technical Debt: {metrics.technical_debt_minutes} min")
        
        except Exception as e:
            print(f"\n❌ Error analyzing {file.name}: {e}")
    
    # Summary
    if metrics_list:
        avg_quality = sum(m.quality_score for m in metrics_list) / len(metrics_list)
        avg_complexity = sum(m.cyclomatic_complexity for m in metrics_list) / len(metrics_list)
        
        print(f"\n📈 SUMMARY")
        print("=" * 50)
        print(f"Files Analyzed: {len(metrics_list)}")
        print(f"Average Quality: {avg_quality:.1f}/100")
        print(f"Average Complexity: {avg_complexity:.1f}")
    
    # Export reports
    if args.export_html:
        export_html_report(metrics_list, args.export_html, args.project_name)
        print(f"\n✅ HTML report saved to: {args.export_html}")
    
    if args.export_csv:
        export_csv_report(metrics_list, args.export_csv)
        print(f"\n✅ CSV report saved to: {args.export_csv}")
    
    if args.export_json:
        export_json_report(metrics_list, args.export_json)
        print(f"\n✅ JSON report saved to: {args.export_json}")


if __name__ == "__main__":
    main()
