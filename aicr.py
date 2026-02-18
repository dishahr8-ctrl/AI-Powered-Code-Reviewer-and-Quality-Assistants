"""Unified CLI for AI Code Reviewer"""
import argparse
import sys
from pathlib import Path
from core.parser import parse_python
from core.quality_metrics import calculate_quality_score
from core.ai_engine_enhanced import generate_enhanced_review
from core.report_exporter import export_html_report, export_csv_report, export_json_report


def scan_files(path, pattern="*.py"):
    """Scan for Python files"""
    path_obj = Path(path)
    if path_obj.is_file():
        return [path_obj]
    return list(path_obj.rglob(pattern))


def review_files(files, severity="WARNING"):
    """Review files and display results"""
    print(f"\n🔍 Reviewing {len(files)} file(s)...\n")
    
    for file in files:
        code = file.read_text()
        metrics = calculate_quality_score(code, str(file))
        parsed = parse_python(code)
        reviews = generate_enhanced_review(code, parsed)
        
        # Filter by severity
        severity_order = {"CRITICAL": 3, "WARNING": 2, "INFO": 1}
        min_level = severity_order.get(severity, 2)
        filtered = [r for r in reviews if severity_order.get(r.get('severity', 'INFO'), 1) >= min_level]
        
        critical = sum(1 for r in filtered if r.get('severity') == 'CRITICAL')
        warning = sum(1 for r in filtered if r.get('severity') == 'WARNING')
        info = sum(1 for r in filtered if r.get('severity') == 'INFO')
        
        status = "✅" if critical == 0 else "❌"
        print(f"{status} {file.name}")
        print(f"   Quality: {metrics.quality_score:.1f}/100 | Complexity: {metrics.cyclomatic_complexity} | Issues: {critical}🔴 {warning}🟡 {info}🔵")
        
        if critical > 0:
            for r in [r for r in filtered if r.get('severity') == 'CRITICAL']:
                print(f"      🔴 {r.get('message', '')}")
    
    print(f"\n📊 SUMMARY")
    print(f"Files Analyzed: {len(files)}")


def apply_fixes(files, dry_run=False):
    """Apply auto-fixes to files"""
    from core.auto_fixer import apply_auto_fixes
    
    print(f"\n🔧 {'Previewing' if dry_run else 'Applying'} auto-fixes to {len(files)} file(s)...\n")
    
    total_fixes = 0
    for file in files:
        code = file.read_text()
        parsed = parse_python(code)
        reviews = generate_enhanced_review(code, parsed, enable_autofix=True)
        
        fixable = [r for r in reviews if r.get('auto_fix')]
        if fixable:
            fixed_code, applied = apply_auto_fixes(code, fixable)
            total_fixes += len(applied)
            
            print(f"✅ {file.name}: {len(applied)} fix(es)")
            
            if not dry_run:
                file.write_text(fixed_code)
        else:
            print(f"ℹ️  {file.name}: No auto-fixable issues")
    
    print(f"\n{'Would apply' if dry_run else 'Applied'} {total_fixes} fix(es) total")


def generate_report(files, format="html", project_name="AI Code Review"):
    """Generate quality reports"""
    print(f"\n📊 Generating {format} report for {len(files)} file(s)...\n")
    
    metrics_list = []
    for file in files:
        code = file.read_text()
        metrics = calculate_quality_score(code, str(file))
        metrics_list.append(metrics)
    
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    
    if format in ["html", "all"]:
        html_file = output_dir / "quality_report.html"
        export_html_report(metrics_list, str(html_file), project_name)
        print(f"✅ HTML report: {html_file}")
    
    if format in ["csv", "all"]:
        csv_file = output_dir / "quality_report.csv"
        export_csv_report(metrics_list, str(csv_file))
        print(f"✅ CSV report: {csv_file}")
    
    if format in ["json", "all"]:
        json_file = output_dir / "quality_report.json"
        export_json_report(metrics_list, str(json_file))
        print(f"✅ JSON report: {json_file}")


def main():
    parser = argparse.ArgumentParser(description="AI Code Reviewer - Unified CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for files")
    scan_parser.add_argument("path", help="Path to scan")
    scan_parser.add_argument("--pattern", default="*.py", help="File pattern")
    
    # Review command
    review_parser = subparsers.add_parser("review", help="Review code")
    review_parser.add_argument("path", help="Path to review")
    review_parser.add_argument("--severity", choices=["CRITICAL", "WARNING", "INFO"], default="WARNING")
    
    # Apply command
    apply_parser = subparsers.add_parser("apply", help="Apply auto-fixes")
    apply_parser.add_argument("path", help="Path to fix")
    apply_parser.add_argument("--dry-run", action="store_true", help="Preview fixes")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate reports")
    report_parser.add_argument("path", help="Path to analyze")
    report_parser.add_argument("--format", choices=["html", "csv", "json", "all"], default="html")
    report_parser.add_argument("--project-name", default="AI Code Review")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "scan":
        files = scan_files(args.path, args.pattern)
        print(f"\n🔍 Found {len(files)} file(s):")
        for f in files:
            print(f"   📄 {f}")
    
    elif args.command == "review":
        files = scan_files(args.path)
        review_files(files, args.severity)
    
    elif args.command == "apply":
        files = scan_files(args.path)
        apply_fixes(files, args.dry_run)
    
    elif args.command == "report":
        files = scan_files(args.path)
        generate_report(files, args.format, args.project_name)


if __name__ == "__main__":
    main()
