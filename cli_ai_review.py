"""CLI for AI Code Review"""
import argparse
from pathlib import Path
from core.parser import parse_python
from core.ai_engine_enhanced import generate_enhanced_review
from core.auto_fixer import apply_auto_fixes, generate_fix_report
from core.llm_prompts import generate_review_prompt


def main():
    parser = argparse.ArgumentParser(description="AI Code Review CLI")
    parser.add_argument("file", help="Python file to review")
    parser.add_argument("--autofix", action="store_true", help="Apply auto-fixes")
    parser.add_argument("--preview", action="store_true", help="Preview fixes without applying")
    parser.add_argument("--output", help="Output file for fixed code")
    parser.add_argument("--severity", choices=["CRITICAL", "WARNING", "INFO"], help="Filter by severity")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--prompt", action="store_true", help="Show LLM prompt")
    
    args = parser.parse_args()
    
    # Read file
    code = Path(args.file).read_text()
    
    # Parse and review
    parsed = parse_python(code)
    reviews = generate_enhanced_review(code, parsed, enable_autofix=True)
    
    # Show LLM prompt if requested
    if args.prompt:
        print("\n🤖 LLM PROMPT")
        print("=" * 50)
        prompt = generate_review_prompt(code, parsed)
        print(prompt)
        print("=" * 50)
        return
    
    # Filter reviews
    if args.severity:
        reviews = [r for r in reviews if r.get('severity') == args.severity]
    if args.category:
        reviews = [r for r in reviews if r.get('category') == args.category]
    
    # Count by severity
    critical = sum(1 for r in reviews if r.get('severity') == 'CRITICAL')
    warning = sum(1 for r in reviews if r.get('severity') == 'WARNING')
    info = sum(1 for r in reviews if r.get('severity') == 'INFO')
    
    print(f"\n🔍 AI CODE REVIEW: {args.file}")
    print("=" * 50)
    print(f"Found {len(reviews)} issue(s):")
    print(f"  🔴 CRITICAL: {critical}")
    print(f"  🟡 WARNING: {warning}")
    print(f"  🔵 INFO: {info}")
    print()
    
    # Display issues
    for i, review in enumerate(reviews, 1):
        severity_icon = {'CRITICAL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(review.get('severity'), '🔵')
        print(f"{i}. {severity_icon} [{review.get('severity')}] {review.get('category', 'general')}")
        print(f"   {review.get('message', '')}")
        if review.get('suggestion'):
            print(f"   💡 {review.get('suggestion')}")
        if review.get('auto_fix'):
            print(f"   🔧 Auto-fix available")
        print()
    
    # Apply auto-fixes
    if args.autofix or args.preview:
        fixable = [r for r in reviews if r.get('auto_fix')]
        if fixable:
            fixed_code, applied_fixes = apply_auto_fixes(code, fixable)
            
            print(f"\n🔧 AUTO-FIX {'PREVIEW' if args.preview else 'APPLIED'}")
            print("=" * 50)
            print(generate_fix_report(applied_fixes))
            
            if not args.preview:
                output_file = args.output or args.file
                Path(output_file).write_text(fixed_code)
                print(f"\n✅ Fixed code saved to: {output_file}")
        else:
            print("\nℹ️  No auto-fixable issues found")


if __name__ == "__main__":
    main()
