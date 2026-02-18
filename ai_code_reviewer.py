"""
AI Code Reviewer - Unified CLI
Combines AI review, docstring tools, and quality metrics
"""
import sys
import argparse
from pathlib import Path
from core.parser import parse_python
from core.ai_engine_enhanced import generate_enhanced_review
from core.quality_metrics import calculate_quality_score
from core.report_exporter import print_metrics_summary, export_html_report
from core.auto_fixer import apply_auto_fixes, generate_fix_report
from core.docstring_validator import calculate_docstring_coverage


def comprehensive_review(file_path: str, args):
    """Perform comprehensive code review with all features"""
    
    print(f"\n{'='*70}")
    print(f"🤖 AI CODE REVIEWER - COMPREHENSIVE ANALYSIS")
    print(f"{'='*70}")
    print(f"File: {file_path}\n")
    
    # Read file
    try:
        code = Path(file_path).read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # 1. QUALITY METRICS
    if not args.skip_metrics:
        print("📊 STEP 1: QUALITY METRICS")
        print("-" * 70)
        metrics = calculate_quality_score(code, file_path)
        
        print(f"   Quality Score: {metrics.quality_score:.1f}/100 (Grade: {get_grade(metrics.quality_score)})")
        print(f"   Maintainability Index: {metrics.maintainability_index:.1f}/100")
        print(f"   Cyclomatic Complexity: {metrics.cyclomatic_complexity}")
        print(f"   Docstring Coverage: {metrics.docstring_coverage:.1f}%")
        print(f"   Code Smells: {metrics.code_smells}")
        print(f"   Technical Debt: {metrics.technical_debt_minutes} minutes")
        
        if args.detailed_metrics:
            print_metrics_summary(metrics)
    
    # 2. AI REVIEW
    if not args.skip_review:
        print(f"\n🔍 STEP 2: AI CODE REVIEW")
        print("-" * 70)
        parsed_data = parse_python(code)
        reviews = generate_enhanced_review(code, parsed_data, enable_autofix=True)
        
        # Group by severity
        critical = [r for r in reviews if r['severity'] == 'CRITICAL']
        warnings = [r for r in reviews if r['severity'] == 'WARNING']
        info = [r for r in reviews if r['severity'] == 'INFO']
        
        print(f"   Found: {len(critical)} critical, {len(warnings)} warnings, {len(info)} info\n")
        
        # Show top issues
        for review in reviews[:5]:
            icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵"}.get(review['severity'], "⚪")
            print(f"   {icon} [{review['severity']}] {review['message']}")
            if review.get('suggestion'):
                print(f"      💡 {review['suggestion']}")
    
    # 3. DOCSTRING ANALYSIS
    if not args.skip_docstrings:
        print(f"\n📚 STEP 3: DOCSTRING ANALYSIS")
        print("-" * 70)
        doc_coverage = calculate_docstring_coverage(code)
        
        print(f"   Coverage: {doc_coverage['coverage']:.1f}%")
        print(f"   Documented: {doc_coverage['documented']}/{doc_coverage['total']} items")
        
        if doc_coverage['coverage'] < 80:
            print(f"   ⚠️  Recommendation: Improve documentation coverage")
    
    # 4. AUTO-FIX
    if args.autofix:
        print(f"\n🔧 STEP 4: AUTO-FIX")
        print("-" * 70)
        
        fixed_code, applied_fixes = apply_auto_fixes(code, reviews)
        
        if applied_fixes:
            output_file = args.output or file_path
            Path(output_file).write_text(fixed_code, encoding='utf-8')
            print(f"   ✅ Applied {len(applied_fixes)} fixes")
            print(f"   📝 Saved to: {output_file}")
        else:
            print(f"   ℹ️  No auto-fixable issues found")
    
    # 5. SUMMARY & RECOMMENDATIONS
    print(f"\n📋 SUMMARY & RECOMMENDATIONS")
    print("-" * 70)
    
    if not args.skip_metrics:
        if metrics.quality_score >= 80:
            print(f"   ✅ Quality: Excellent ({metrics.quality_score:.1f}/100)")
        elif metrics.quality_score >= 60:
            print(f"   ⚠️  Quality: Needs improvement ({metrics.quality_score:.1f}/100)")
        else:
            print(f"   ❌ Quality: Critical ({metrics.quality_score:.1f}/100)")
    
    if not args.skip_review:
        if len(critical) > 0:
            print(f"   🔴 Action Required: Fix {len(critical)} critical issue(s)")
        elif len(warnings) > 0:
            print(f"   🟡 Recommended: Address {len(warnings)} warning(s)")
        else:
            print(f"   ✅ Code Review: No major issues")
    
    if not args.skip_docstrings:
        if doc_coverage['coverage'] < 70:
            print(f"   📚 Documentation: Add docstrings ({doc_coverage['coverage']:.1f}% coverage)")
        else:
            print(f"   ✅ Documentation: Good coverage ({doc_coverage['coverage']:.1f}%)")
    
    print(f"\n{'='*70}\n")
    
    # Return success/failure
    if not args.skip_metrics:
        return metrics.quality_score >= 60 and len(critical) == 0
    return len(critical) == 0 if not args.skip_review else True


def get_grade(score: float) -> str:
    """Get letter grade from score"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def main():
    parser = argparse.ArgumentParser(
        description="AI Code Reviewer - Comprehensive code analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full analysis
  python ai_code_reviewer.py myfile.py
  
  # With auto-fix
  python ai_code_reviewer.py myfile.py --autofix
  
  # Skip certain checks
  python ai_code_reviewer.py myfile.py --skip-metrics
  
  # Detailed metrics
  python ai_code_reviewer.py myfile.py --detailed-metrics
  
  # Generate report
  python ai_code_reviewer.py myfile.py --export-html report.html
        """
    )
    
    parser.add_argument("file", help="Python file to analyze")
    
    # Analysis options
    parser.add_argument("--skip-metrics", action="store_true", help="Skip quality metrics")
    parser.add_argument("--skip-review", action="store_true", help="Skip AI review")
    parser.add_argument("--skip-docstrings", action="store_true", help="Skip docstring analysis")
    
    # Output options
    parser.add_argument("--detailed-metrics", action="store_true", help="Show detailed metrics")
    parser.add_argument("--autofix", action="store_true", help="Apply auto-fixes")
    parser.add_argument("--output", "-o", help="Output file for fixed code")
    
    # Export options
    parser.add_argument("--export-html", help="Export HTML report")
    parser.add_argument("--export-csv", help="Export CSV report")
    parser.add_argument("--export-json", help="Export JSON report")
    
    args = parser.parse_args()
    
    # Validate file
    if not Path(args.file).exists():
        print(f"❌ File not found: {args.file}")
        sys.exit(1)
    
    # Run comprehensive review
    success = comprehensive_review(args.file, args)
    
    # Export reports if requested
    if args.export_html or args.export_csv or args.export_json:
        from core.report_exporter import export_csv_report, export_json_report
        
        code = Path(args.file).read_text(encoding='utf-8')
        metrics = calculate_quality_score(code, args.file)
        metrics_list = [metrics]
        
        if args.export_html:
            export_html_report(metrics_list, args.export_html, "Code Quality Report")
            print(f"✅ HTML report: {args.export_html}")
        
        if args.export_csv:
            export_csv_report(metrics_list, args.export_csv)
            print(f"✅ CSV report: {args.export_csv}")
        
        if args.export_json:
            export_json_report(metrics_list, args.export_json)
            print(f"✅ JSON report: {args.export_json}")
    
    # Exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
