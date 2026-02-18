"""CLI for Docstring Tools"""
import argparse
from pathlib import Path
from core.docstring_validator import calculate_docstring_coverage, validate_docstring_completeness, run_pydocstyle_check
from core.docstring_generator import generate_docstring, DocstringStyle, extract_function_info
from core.docstring_parser import detect_docstring_style
import ast


def main():
    parser = argparse.ArgumentParser(description="Docstring Tools CLI")
    parser.add_argument("file", help="Python file to analyze")
    parser.add_argument("--validate", action="store_true", help="Validate docstrings")
    parser.add_argument("--generate", action="store_true", help="Generate missing docstrings")
    parser.add_argument("--style", choices=["google", "numpy", "rest"], default="google", help="Docstring style")
    
    args = parser.parse_args()
    
    # Read file
    code = Path(args.file).read_text()
    
    if args.validate:
        print(f"\n🔍 Validating docstrings in {args.file}")
        print("=" * 50)
        
        # Calculate coverage
        coverage = calculate_docstring_coverage(code)
        print(f"\n📊 Docstring Coverage: {coverage['coverage']:.1f}%")
        print(f"   Total items: {coverage['total']}")
        print(f"   Documented: {coverage['documented']}")
        print(f"   Missing: {coverage['missing']}")
        
        # Validate completeness
        try:
            tree = ast.parse(code)
            issues = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    docstring = ast.get_docstring(node)
                    node_issues = validate_docstring_completeness(node, docstring)
                    issues.extend(node_issues)
            
            if issues:
                print(f"\n⚠️  Found {len(issues)} issue(s):\n")
                for severity, message in issues:
                    icon = "🟡" if severity == "WARNING" else "🔵"
                    print(f"{icon} [{severity}] {message}")
            else:
                print("\n✅ All docstrings are complete!")
        except Exception as e:
            print(f"\n❌ Error validating: {e}")
        
        # Run pydocstyle
        print(f"\n🔧 Running pydocstyle checks...")
        try:
            pydoc_issues = run_pydocstyle_check(args.file)
            if pydoc_issues:
                print(f"\n📋 pydocstyle found {len(pydoc_issues)} issue(s):\n")
                for issue in pydoc_issues[:10]:
                    print(f"   {issue}")
            else:
                print("\n✅ No pydocstyle issues found!")
        except Exception as e:
            print(f"\n⚠️  pydocstyle not available: {e}")
    
    elif args.generate:
        print(f"\n✨ Generating {args.style} style docstrings for {args.file}")
        print("=" * 50)
        
        style_map = {
            "google": DocstringStyle.GOOGLE,
            "numpy": DocstringStyle.NUMPY,
            "rest": DocstringStyle.REST
        }
        
        try:
            tree = ast.parse(code)
            generated_count = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
                    func_info = extract_function_info(node)
                    docstring = generate_docstring(func_info, style_map[args.style])
                    
                    print(f"\n📝 Function: {node.name}")
                    print('"""')
                    print(docstring)
                    print('"""')
                    generated_count += 1
            
            if generated_count > 0:
                print(f"\n✅ Generated {generated_count} docstring(s)")
            else:
                print("\n✅ All functions already have docstrings!")
        
        except Exception as e:
            print(f"\n❌ Error generating: {e}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
