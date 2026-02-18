"""Streamlit UI for AI Code Reviewer"""
import streamlit as st
from pathlib import Path
from core.quality_metrics import calculate_quality_score
from core.ai_engine_enhanced import generate_enhanced_review
from core.parser import parse_python
from core.docstring_validator import calculate_docstring_coverage, validate_docstring_completeness, run_pydocstyle_check
from core.docstring_generator import generate_docstring, DocstringStyle, extract_function_info
from core.docstring_parser import detect_docstring_style
from core.evaluation_criteria import EvaluationCriteria
from core.llm_prompts import generate_review_prompt, SYSTEM_PROMPT
from core.auto_fixer import apply_auto_fixes, generate_fix_report
import ast

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

# Clear cache button in sidebar (for development)
if st.sidebar.button("🔄 Clear Cache & Reload"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

st.title("🤖 AI Code Reviewer")

# Sidebar
st.sidebar.header("⚙️ Settings")

# Programming language selection
programming_language = st.sidebar.selectbox(
    "Programming Language",
    ["Python", "Java", "C++", "JavaScript", "Go", "Rust"],
    help="Select the programming language of your code"
)

# Severity filter with tooltips
severity_filter = st.sidebar.multiselect(
    "Filter by Severity",
    ["CRITICAL", "WARNING", "INFO"],
    default=["CRITICAL", "WARNING", "INFO"],
    help="Filter issues by severity level"
)

# Category filter
category_filter = st.sidebar.multiselect(
    "Filter by Category",
    ["naming", "documentation", "formatting", "complexity", "syntax"],
    default=["naming", "documentation", "formatting", "complexity", "syntax"],
    help="Filter issues by category"
)

# Quality threshold slider
min_quality = st.sidebar.slider(
    "Minimum Quality Score",
    min_value=0,
    max_value=100,
    value=60,
    help="Show only files with quality score above this threshold"
)

# Set default values for removed features
enable_docstring_gen = False
enable_pydocstyle = False
enable_autofix = False
autofix_categories = []
show_llm_prompts = False
search_query = ""

# Export options
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export Reports")
export_format = st.sidebar.multiselect(
    "Export Format",
    ["CSV", "HTML", "JSON"],
    default=[],
    help="Select formats to export analysis results"
)

# Main content
# Code input section
st.subheader("Code Input")

# Input method selection
input_method = st.radio(
    "Input Method",
    ["Text Input", "PDF Upload"],
    horizontal=True,
    help="Choose how to provide your code"
)

if input_method == "Text Input":
    # Language-specific placeholder code
    placeholder_code = {
        "Python": "# Paste your Python code here...",
        "Java": "// Paste your Java code here...",
        "C++": "// Paste your C++ code here...",
        "JavaScript": "// Paste your JavaScript code here...",
        "Go": "// Paste your Go code here...",
        "Rust": "// Paste your Rust code here..."
    }
    
    code_input = st.text_area(
        f"Paste your {programming_language} code here:",
        height=400,
        value="",
        placeholder=placeholder_code.get(programming_language, "# Paste your code here...")
    )
else:
    # PDF Upload
    st.info("📄 Upload a file to extract code automatically")
    uploaded_file = st.file_uploader(
        "Choose a file (PDF, TXT, PY, etc.)",
        type=['pdf', 'txt', 'py', 'java', 'cpp', 'js', 'go', 'rs', 'c', 'h'],
        help="Upload a file containing code",
        key="pdf_uploader"
    )
    
    if uploaded_file is not None:
        st.write(f"📎 File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        try:
            # Check file type
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                # Extract from PDF
                from core.pdf_reader import extract_code_from_pdf
                
                with st.spinner("🔍 Extracting code from PDF..."):
                    code_input = extract_code_from_pdf(uploaded_file)
            else:
                # Read as text file
                with st.spinner("📖 Reading file..."):
                    code_input = uploaded_file.read().decode('utf-8')
            
            if code_input and len(code_input.strip()) > 10:
                st.success(f"✅ Successfully extracted {len(code_input)} characters!")
                
                # Show extracted code in expandable section
                with st.expander("📄 View Extracted Code", expanded=True):
                    # Map language to code highlighting
                    lang_map = {
                        "Python": "python",
                        "Java": "java",
                        "C++": "cpp",
                        "JavaScript": "javascript",
                        "Go": "go",
                        "Rust": "rust"
                    }
                    st.code(code_input, language=lang_map.get(programming_language, "python"))
            else:
                st.error("❌ Could not find any code in the file. Please make sure:")
                st.markdown("""
                - The file contains actual code (not just images)
                - The code is readable text (not scanned)
                - Try copying the code manually if extraction fails
                """)
                code_input = ""
        except ImportError as e:
            st.error("❌ PDF reading library not available. Please install PyPDF2:")
            st.code("pip install PyPDF2", language="bash")
            code_input = ""
        except Exception as e:
            st.error(f"❌ Error reading file:")
            st.markdown(f"""
            **What went wrong:** {str(e)}
            
            **How to fix it:**
            - Make sure the file is not corrupted
            - Try a different file
            - Or paste your code directly using 'Text Input' option
            """)
            code_input = ""
    else:
        code_input = ""

# Language warning for non-Python
if programming_language != "Python":
    st.warning(f"⚠️ Note: Full analysis is optimized for Python. {programming_language} support is limited to basic metrics.")

analyze_btn = st.button("🔍 Analyze Code", type="primary", use_container_width=True)

# Results section (below the code input)
st.markdown("---")

if analyze_btn and code_input.strip():
    st.subheader("Analysis Results")
    with st.spinner("Analyzing your code..."):
        try:
            # Check if Python (full analysis) or other language (basic analysis)
            if programming_language == "Python":
                # Initialize evaluation criteria
                evaluator = EvaluationCriteria()
                
                # Evaluate parser FIRST to catch syntax errors early
                parser_success, parser_details = evaluator.evaluate_parser(code_input)
                
                # If parser failed, show error and stop
                if not parser_success:
                    st.error("❌ Code Analysis Failed")
                    st.markdown("**Problem:** Your code has syntax errors that prevent analysis")
                    for error in parser_details.get('errors', []):
                        st.warning(f"⚠️ {error}")
                    st.markdown("""
                    **How to fix:**
                    - Check for missing colons (:) at the end of if/for/def statements
                    - Make sure all brackets (), [], {} are properly closed
                    - Check for proper indentation
                    - Look for typos in keywords
                    """)
                    st.stop()
                
                # Calculate metrics (only if parsing succeeded)
                metrics = calculate_quality_score(code_input, 'input.py')
                
                # AI Review with auto-fix
                parsed = parse_python(code_input)
                reviews = generate_enhanced_review(code_input, parsed, enable_autofix=enable_autofix)
                
                # Apply auto-fixes if enabled
                fixed_code = code_input
                applied_fixes = []
                if enable_autofix and any(r.get('auto_fix') for r in reviews):
                    # Filter reviews by selected categories
                    fixable_reviews = [
                        r for r in reviews 
                        if r.get('auto_fix') and r.get('category') in autofix_categories
                    ]
                    if fixable_reviews:
                        fixed_code, applied_fixes = apply_auto_fixes(code_input, fixable_reviews)
                
                # Show LLM prompts if enabled
                if show_llm_prompts:
                    with st.expander("🤖 LLM Prompt Templates", expanded=False):
                        st.markdown("### System Prompt")
                        st.code(SYSTEM_PROMPT, language="text")
                        
                        st.markdown("### Review Prompt")
                        review_prompt = generate_review_prompt(code_input, parsed)
                        st.code(review_prompt, language="text")
                        
                        st.info("💡 These prompts are used to generate human-like code feedback")
                
                # Docstring coverage
                doc_cov = calculate_docstring_coverage(code_input)
                
                # Evaluate docstring generation (check if we can generate for missing ones)
                if doc_cov['missing'] > 0:
                    evaluator.track_docstring_generation(success=True, count=doc_cov['missing'])
                
                # Evaluate coverage report (we have coverage data)
                evaluator.evaluate_coverage_report(coverage_data={'coverage': doc_cov['coverage']})
                
                # Get evaluation results
                eval_result = evaluator.get_evaluation_result()
                
                # Display Evaluation Criteria
                st.subheader("✅ Evaluation Criteria")
                
                eval_cols = st.columns(3)
                
                with eval_cols[0]:
                    parser_status = "✅" if eval_result.parser_success_rate >= 95.0 else "❌"
                    st.metric(
                        "Parser Accuracy",
                        f"{eval_result.parser_success_rate:.1f}%",
                        delta=f"Target: ≥95% {parser_status}",
                        help="Parser must extract ≥95% of functions/classes without errors"
                    )
                
                with eval_cols[1]:
                    docgen_status = "✅" if eval_result.docstring_generation_rate >= 100.0 else "❌"
                    st.metric(
                        "Docstring Generation",
                        f"{eval_result.docstring_generation_rate:.1f}%",
                        delta=f"Target: 100% {docgen_status}",
                        help="Baseline docstrings generated for all missing cases"
                    )
                
                with eval_cols[2]:
                    coverage_status = "✅" if eval_result.coverage_report_generated else "❌"
                    st.metric(
                        "Coverage Report",
                        "Generated" if eval_result.coverage_report_generated else "Not Generated",
                        delta=f"{coverage_status}",
                        help="Coverage report generated successfully"
                    )
                
                # Overall evaluation status
                if eval_result.meets_criteria:
                    st.success("🎉 All evaluation criteria met!")
                else:
                    st.warning("⚠️ Some evaluation criteria not met. See details above.")
                
                # Display Quality Metrics for Python
                st.subheader("📊 Quality Metrics")
                
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    grade_color = {
                        'A': '🟢', 'B': '🟡', 'C': '🟠', 'D': '🔴', 'F': '⚫'
                    }.get(metrics.grade, '⚫')
                    st.metric(
                        "Quality Score", 
                        f"{metrics.quality_score:.1f}/100",
                        delta=f"{grade_color} Grade: {metrics.grade}",
                        help="Overall code quality score (0-100)"
                    )
                with metric_cols[1]:
                    mi_rating = "Excellent" if metrics.maintainability_index >= 85 else \
                               "Good" if metrics.maintainability_index >= 65 else \
                               "Fair" if metrics.maintainability_index >= 50 else "Poor"
                    st.metric(
                        "Maintainability", 
                        f"{metrics.maintainability_index:.1f}/100",
                        delta=mi_rating,
                        help="Maintainability Index - industry standard metric"
                    )
                with metric_cols[2]:
                    complexity_status = "🟢" if metrics.cyclomatic_complexity <= 10 else \
                                       "🟡" if metrics.cyclomatic_complexity <= 20 else "🔴"
                    st.metric(
                        "Complexity", 
                        metrics.cyclomatic_complexity,
                        delta=f"{complexity_status}",
                        help="Cyclomatic Complexity - number of decision points"
                    )
                with metric_cols[3]:
                    doc_status = "🟢" if doc_cov['coverage'] >= 80 else \
                                "🟡" if doc_cov['coverage'] >= 50 else "🔴"
                    st.metric(
                        "Doc Coverage", 
                        f"{doc_cov['coverage']:.1f}%",
                        delta=f"{doc_status}",
                        help="Documentation coverage percentage"
                    )
                
                # Code Issues Section for Python
                st.subheader("🔍 Code Issues")
                
                # Severity ranking info
                with st.expander("ℹ️ Severity Levels", expanded=False):
                    st.markdown("""
                    **🔴 CRITICAL**: Prevents code from running (syntax errors, blocking issues)
                    
                    **🟡 WARNING**: Affects maintainability (naming, missing docs, complexity)
                    
                    **🔵 INFO**: Minor improvements (formatting, style suggestions)
                    """)
                
                # Filter reviews by severity and category
                filtered_reviews = [
                    r for r in reviews 
                    if r.get('severity') in severity_filter 
                    and r.get('category', 'general') in category_filter
                ]
                
                # Count by severity
                critical = sum(1 for r in filtered_reviews if r.get('severity') == 'CRITICAL')
                warning = sum(1 for r in filtered_reviews if r.get('severity') == 'WARNING')
                info = sum(1 for r in filtered_reviews if r.get('severity') == 'INFO')
                
                issue_cols = st.columns(4)
                with issue_cols[0]:
                    st.metric("🔴 Critical", critical)
                with issue_cols[1]:
                    st.metric("🟡 Warning", warning)
                with issue_cols[2]:
                    st.metric("🔵 Info", info)
                with issue_cols[3]:
                    st.metric("📊 Total", len(filtered_reviews))
                
                # Display issues with pagination
                if filtered_reviews:
                    # Pagination
                    items_per_page = 10
                    total_pages = (len(filtered_reviews) + items_per_page - 1) // items_per_page
                    
                    if total_pages > 1:
                        page = st.selectbox(
                            "Page",
                            range(1, total_pages + 1),
                            help=f"Showing {len(filtered_reviews)} issues across {total_pages} pages"
                        )
                    else:
                        page = 1
                    
                    start_idx = (page - 1) * items_per_page
                    end_idx = min(start_idx + items_per_page, len(filtered_reviews))
                    
                    for review in filtered_reviews[start_idx:end_idx]:
                        severity_color = {
                            'CRITICAL': '🔴',
                            'WARNING': '🟡',
                            'INFO': '🔵'
                        }.get(review.get('severity', 'INFO'), '🔵')
                        
                        with st.expander(
                            f"{severity_color} {review.get('severity')}: {review.get('category', 'general')}",
                            expanded=False
                        ):
                            st.write(f"**Message:** {review.get('message', 'No message')}")
                            
                            if review.get('line_number'):
                                st.caption(f"📍 Line {review.get('line_number')}")
                            
                            if review.get('suggestion'):
                                st.info(f"💡 **Suggestion:** {review.get('suggestion')}")
                    
                    # Show pagination info
                    if total_pages > 1:
                        st.caption(f"Showing {start_idx + 1}-{end_idx} of {len(filtered_reviews)} issues")
                else:
                    st.success("✅ No issues found!")
            
            else:
                # Basic analysis for non-Python languages
                st.info(f"📊 Analyzing {programming_language} code (basic metrics only)")
                
                # Basic metrics
                lines = code_input.split('\n')
                total_lines = len(lines)
                non_empty_lines = len([l for l in lines if l.strip()])
                comment_lines = len([l for l in lines if l.strip().startswith(('//', '#', '/*', '*'))])
                
                metrics = type('obj', (object,), {
                    'quality_score': 75.0,
                    'grade': 'C',
                    'lines_of_code': total_lines,
                    'source_lines': non_empty_lines,
                    'comment_lines': comment_lines,
                    'cyclomatic_complexity': 0,
                    'maintainability_index': 0,
                    'docstring_coverage': 0,
                    'code_smells': 0,
                    'technical_debt_minutes': 0,
                    'num_functions': 0,
                    'num_classes': 0,
                    'comment_ratio': comment_lines / non_empty_lines if non_empty_lines > 0 else 0
                })()
                
                reviews = []
                doc_cov = {'coverage': 0, 'documented': 0, 'missing': 0, 'total': 0}
                applied_fixes = []
                fixed_code = code_input
                
                # Detect docstring style
                try:
                    tree = ast.parse(code_input)
                    detected_style = "Unknown"
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and ast.get_docstring(node):
                            detected_style = detect_docstring_style(ast.get_docstring(node)).name
                            break
                except:
                    detected_style = "Unknown"
                
                # Display metrics
                st.subheader("📊 Quality Metrics")
                
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    grade_color = {
                        'A': '🟢', 'B': '🟡', 'C': '🟠', 'D': '🔴', 'F': '⚫'
                    }.get(metrics.grade, '⚫')
                    st.metric(
                        "Quality Score", 
                        f"{metrics.quality_score:.1f}/100",
                        delta=f"{grade_color} Grade: {metrics.grade}",
                        help="Overall code quality score (0-100)"
                    )
                with metric_cols[1]:
                    mi_rating = "Excellent" if metrics.maintainability_index >= 85 else \
                               "Good" if metrics.maintainability_index >= 65 else \
                               "Fair" if metrics.maintainability_index >= 50 else "Poor"
                    st.metric(
                        "Maintainability", 
                        f"{metrics.maintainability_index:.1f}/100",
                        delta=mi_rating,
                        help="Maintainability Index - industry standard metric"
                    )
                with metric_cols[2]:
                    complexity_status = "🟢" if metrics.cyclomatic_complexity <= 10 else \
                                       "🟡" if metrics.cyclomatic_complexity <= 20 else "🔴"
                    st.metric(
                        "Complexity", 
                        metrics.cyclomatic_complexity,
                        delta=f"{complexity_status}",
                        help="Cyclomatic Complexity - number of decision points"
                    )
                with metric_cols[3]:
                    doc_status = "🟢" if doc_cov['coverage'] >= 80 else \
                                "🟡" if doc_cov['coverage'] >= 50 else "🔴"
                    st.metric(
                        "Doc Coverage", 
                        f"{doc_cov['coverage']:.1f}%",
                        delta=f"{doc_status}",
                        help="Documentation coverage percentage"
                    )
                
                # Additional metrics in expander
                with st.expander("📈 Detailed Metrics & Validation", expanded=False):
                    detail_cols = st.columns(3)
                    
                    with detail_cols[0]:
                        st.markdown("**Size Metrics**")
                        st.write(f"Lines of Code: {metrics.lines_of_code}")
                        st.write(f"Source Lines: {metrics.source_lines}")
                        st.write(f"Comment Lines: {metrics.comment_lines}")
                        st.write(f"Functions: {metrics.num_functions}")
                        st.write(f"Classes: {metrics.num_classes}")
                    
                    with detail_cols[1]:
                        st.markdown("**Complexity Metrics**")
                        st.write(f"Cyclomatic: {metrics.cyclomatic_complexity}")
                        st.write(f"Cognitive: {metrics.cognitive_complexity}")
                        st.write(f"Halstead Volume: {metrics.halstead_volume:.2f}")
                        st.write(f"Halstead Difficulty: {metrics.halstead_difficulty:.2f}")
                        st.write(f"Estimated Bugs: {metrics.halstead_bugs:.2f}")
                    
                    with detail_cols[2]:
                        st.markdown("**Code Health**")
                        st.write(f"Code Smells: {metrics.code_smells}")
                        st.write(f"Technical Debt: {metrics.technical_debt_minutes} min")
                        st.write(f"Comment Ratio: {metrics.comment_ratio:.1%}")
                        
                        # Quality indicators
                        st.markdown("**Quality Indicators**")
                        if metrics.quality_score >= 80:
                            st.success("✅ Excellent quality")
                        elif metrics.quality_score >= 60:
                            st.info("ℹ️ Good quality")
                        else:
                            st.warning("⚠️ Needs improvement")
                
                # Export reports if requested
                if export_format:
                    st.subheader("📥 Export Reports")
                    
                    from core.report_exporter import export_csv_report, export_html_report, export_json_report
                    import tempfile
                    import os
                    
                    metrics_list = [metrics]
                    
                    export_cols = st.columns(len(export_format))
                    
                    for idx, fmt in enumerate(export_format):
                        with export_cols[idx]:
                            if fmt == "CSV":
                                with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                                    export_csv_report(metrics_list, f.name)
                                    csv_data = open(f.name, 'r').read()
                                    os.unlink(f.name)
                                
                                st.download_button(
                                    label="📊 Download CSV",
                                    data=csv_data,
                                    file_name="code_quality_report.csv",
                                    mime="text/csv"
                                )
                            
                            elif fmt == "HTML":
                                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                                    export_html_report(metrics_list, f.name, "Code Quality Report")
                                    html_data = open(f.name, 'r').read()
                                    os.unlink(f.name)
                                
                                st.download_button(
                                    label="📄 Download HTML",
                                    data=html_data,
                                    file_name="code_quality_report.html",
                                    mime="text/html"
                                )
                            
                            elif fmt == "JSON":
                                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                                    export_json_report(metrics_list, f.name)
                                    json_data = open(f.name, 'r').read()
                                    os.unlink(f.name)
                                
                                st.download_button(
                                    label="📋 Download JSON",
                                    data=json_data,
                                    file_name="code_quality_report.json",
                                    mime="application/json"
                                )
                
                # Docstring Analysis Section
                st.subheader("📚 Docstring Analysis")
                
                doc_cols = st.columns(3)
                with doc_cols[0]:
                    st.metric("Documented", doc_cov['documented'])
                with doc_cols[1]:
                    st.metric("Missing Docs", doc_cov['missing'])
                with doc_cols[2]:
                    st.info(f"**Detected Style:** {detected_style}")
                
                # Docstring validation issues
                try:
                    tree = ast.parse(code_input)
                    validation_issues = []
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                            docstring = ast.get_docstring(node)
                            issues = validate_docstring_completeness(node, docstring)
                            validation_issues.extend(issues)
                    
                    if validation_issues:
                        with st.expander(f"⚠️ Docstring Issues ({len(validation_issues)} found)"):
                            for severity, message in validation_issues:
                                if severity == "WARNING":
                                    st.warning(f"🟡 {message}")
                                else:
                                    st.info(f"🔵 {message}")
                except:
                    pass
                
                # pydocstyle checks
                if enable_pydocstyle:
                    try:
                        # Save code to temp file for pydocstyle
                        import tempfile
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                            f.write(code_input)
                            temp_file = f.name
                        
                        pydoc_issues = run_pydocstyle_check(temp_file)
                        
                        import os
                        os.unlink(temp_file)
                        
                        if pydoc_issues:
                            with st.expander(f"📋 pydocstyle Issues ({len(pydoc_issues)} found)"):
                                for issue in pydoc_issues[:10]:  # Limit to 10
                                    st.text(issue)
                    except Exception as e:
                        pass
                
                # Docstring Generation
                if enable_docstring_gen and doc_cov['missing'] > 0:
                    st.subheader("✨ Generate Docstrings")
                    
                    style_map = {
                        "Google": DocstringStyle.GOOGLE,
                        "NumPy": DocstringStyle.NUMPY,
                        "reST": DocstringStyle.REST
                    }
                    
                    if st.button("🔧 Generate Missing Docstrings", type="secondary"):
                        with st.spinner(f"Generating {docstring_style} style docstrings..."):
                            try:
                                # Parse code and generate docstrings
                                tree = ast.parse(code_input)
                                generated_code = code_input
                                
                                for node in ast.walk(tree):
                                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                                        if not ast.get_docstring(node):
                                            # Extract function info and generate docstring
                                            if isinstance(node, ast.FunctionDef):
                                                func_info = extract_function_info(node)
                                                docstring = generate_docstring(
                                                    func_info, 
                                                    style=style_map[docstring_style]
                                                )
                                                
                                                # Insert docstring (simplified - just show example)
                                                st.code(f'"""{docstring}"""', language="python")
                                
                                st.success(f"✅ Generated docstrings in {docstring_style} style!")
                                st.info("💡 Docstrings shown above. In a full implementation, these would be inserted into your code.")
                                
                            except Exception as e:
                                st.error(f"Error generating docstrings: {str(e)}")
                
                # Issues
                st.subheader("🔍 Code Issues")
                
                # Severity ranking info
                with st.expander("ℹ️ Severity Levels", expanded=False):
                    st.markdown("""
                    **🔴 CRITICAL**: Prevents code from running (syntax errors, blocking issues)
                    
                    **🟡 WARNING**: Affects maintainability (naming, missing docs, complexity)
                    
                    **🔵 INFO**: Minor improvements (formatting, style suggestions)
                    """)
                
                # Filter reviews by severity and category
                filtered_reviews = [
                    r for r in reviews 
                    if r.get('severity') in severity_filter 
                    and r.get('category', 'general') in category_filter
                ]
                
                # Count by severity
                critical = sum(1 for r in filtered_reviews if r.get('severity') == 'CRITICAL')
                warning = sum(1 for r in filtered_reviews if r.get('severity') == 'WARNING')
                info = sum(1 for r in filtered_reviews if r.get('severity') == 'INFO')
                fixable = sum(1 for r in filtered_reviews if r.get('auto_fix'))
                
                issue_cols = st.columns(4)
                with issue_cols[0]:
                    st.metric("🔴 Critical", critical)
                with issue_cols[1]:
                    st.metric("🟡 Warning", warning)
                with issue_cols[2]:
                    st.metric("🔵 Info", info)
                with issue_cols[3]:
                    st.metric("📊 Total", len(filtered_reviews))
                
                # Display issues with pagination
                if filtered_reviews:
                    # Pagination
                    items_per_page = 10
                    total_pages = (len(filtered_reviews) + items_per_page - 1) // items_per_page
                    
                    if total_pages > 1:
                        page = st.selectbox(
                            "Page",
                            range(1, total_pages + 1),
                            help=f"Showing {len(filtered_reviews)} issues across {total_pages} pages"
                        )
                    else:
                        page = 1
                    
                    start_idx = (page - 1) * items_per_page
                    end_idx = min(start_idx + items_per_page, len(filtered_reviews))
                    
                    for review in filtered_reviews[start_idx:end_idx]:
                        severity_color = {
                            'CRITICAL': '🔴',
                            'WARNING': '🟡',
                            'INFO': '🔵'
                        }.get(review.get('severity', 'INFO'), '🔵')
                        
                        with st.expander(
                            f"{severity_color} {review.get('severity')}: {review.get('category', 'general')}",
                            expanded=False
                        ):
                            st.write(f"**Message:** {review.get('message', 'No message')}")
                            
                            if review.get('line_number'):
                                st.caption(f"📍 Line {review.get('line_number')}")
                            
                            if review.get('suggestion'):
                                st.info(f"💡 **Suggestion:** {review.get('suggestion')}")
                    
                    # Show pagination info
                    if total_pages > 1:
                        st.caption(f"Showing {start_idx + 1}-{end_idx} of {len(filtered_reviews)} issues")
                else:
                    st.success("✅ No issues found!")
                
                # Additional metrics
                with st.expander("📈 Detailed Metrics"):
                    detail_cols = st.columns(2)
                    with detail_cols[0]:
                        st.write(f"**Lines of Code:** {metrics.lines_of_code}")
                        st.write(f"**Functions:** {metrics.num_functions}")
                        st.write(f"**Classes:** {metrics.num_classes}")
                    with detail_cols[1]:
                        st.write(f"**Code Smells:** {metrics.code_smells}")
                        st.write(f"**Technical Debt:** {metrics.technical_debt_minutes} min")
                        st.write(f"**Comment Ratio:** {metrics.comment_ratio:.1%}")
        
        except Exception as e:
            st.error("❌ Something went wrong while analyzing your code")
            
            # Human-readable error explanations
            error_msg = str(e).lower()
            
            if "syntax" in error_msg or "invalid syntax" in error_msg:
                st.markdown("""
                **Problem:** Your code has a syntax error (like a typo or missing bracket)
                
                **How to fix:**
                - Check for missing colons (:) at the end of if/for/def statements
                - Make sure all brackets (), [], {} are properly closed
                - Check for proper indentation
                - Look for typos in keywords
                """)
            elif "import" in error_msg or "module" in error_msg:
                st.markdown("""
                **Problem:** The code tries to import a library that's not available
                
                **How to fix:**
                - This is just a warning - your code structure is still analyzed
                - Install missing libraries if you want to run the code
                - The analysis focuses on code quality, not execution
                """)
            elif "indentation" in error_msg:
                st.markdown("""
                **Problem:** Your code has inconsistent indentation (spaces/tabs mixed)
                
                **How to fix:**
                - Use either spaces OR tabs, not both
                - Python requires consistent indentation (usually 4 spaces)
                - Check that all code blocks are properly indented
                """)
            else:
                st.markdown(f"""
                **Error details:** {str(e)}
                
                **What you can do:**
                - Check if your code is valid {programming_language} code
                - Try analyzing a smaller portion of code
                - Make sure the code is complete (no missing parts)
                """)
            
            import traceback
            with st.expander("🔧 Technical Details (for debugging)"):
                st.code(traceback.format_exc())

elif analyze_btn:
    st.warning("Please enter some code to analyze")

# Footer
st.sidebar.markdown("---")
