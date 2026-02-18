"""Demo: Docstring Tools"""
from core.docstring_parser import parse_google_docstring, parse_numpy_docstring, detect_docstring_style, DocstringStyle
from core.docstring_generator import generate_docstring, extract_function_info
from core.docstring_validator import calculate_docstring_coverage
import ast

print("📚 DOCSTRING TOOLS DEMO")
print("=" * 60)

# Sample docstrings
google_doc = """
Calculate the sum of two numbers.

Args:
    a (int): First number
    b (int): Second number

Returns:
    int: Sum of a and b

Raises:
    ValueError: If inputs are not numbers
"""

numpy_doc = """
Calculate the sum of two numbers.

Parameters
----------
a : int
    First number
b : int
    Second number

Returns
-------
int
    Sum of a and b

Raises
------
ValueError
    If inputs are not numbers
"""

# 1. Style Detection
print("\n1️⃣  Style Detection")
print("-" * 60)
google_style = detect_docstring_style(google_doc)
numpy_style = detect_docstring_style(numpy_doc)
print(f"Google docstring detected as: {google_style.name}")
print(f"NumPy docstring detected as: {numpy_style.name}")

# 2. Parsing
print("\n2️⃣  Parsing Docstrings")
print("-" * 60)
print("\nGoogle Style:")
parsed_google = parse_google_docstring(google_doc)
print(f"  Description: {parsed_google.get('description', '')[:50]}...")
print(f"  Args: {len(parsed_google.get('args', []))}")
print(f"  Returns: {bool(parsed_google.get('returns'))}")
print(f"  Raises: {len(parsed_google.get('raises', []))}")

print("\nNumPy Style:")
parsed_numpy = parse_numpy_docstring(numpy_doc)
print(f"  Description: {parsed_numpy.get('description', '')[:50]}...")
print(f"  Parameters: {len(parsed_numpy.get('parameters', []))}")
print(f"  Returns: {bool(parsed_numpy.get('returns'))}")
print(f"  Raises: {len(parsed_numpy.get('raises', []))}")

# 3. Generation
print("\n3️⃣  Generating Docstrings")
print("-" * 60)

sample_code = """
def calculate_sum(a, b):
    return a + b

def process_data(data, threshold=10):
    if not data:
        raise ValueError("Data cannot be empty")
    return [x for x in data if x > threshold]
"""

tree = ast.parse(sample_code)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        func_info = extract_function_info(node)
        
        print(f"\nFunction: {node.name}")
        
        # Generate in different styles
        for style_name, style in [("Google", DocstringStyle.GOOGLE), ("NumPy", DocstringStyle.NUMPY)]:
            docstring = generate_docstring(func_info, style)
            print(f"\n{style_name} Style:")
            print('"""')
            print(docstring)
            print('"""')

# 4. Coverage
print("\n4️⃣  Coverage Calculation")
print("-" * 60)

code_with_docs = """
def documented_function():
    '''This function has a docstring'''
    pass

def undocumented_function():
    pass

class DocumentedClass:
    '''This class has a docstring'''
    pass
"""

coverage = calculate_docstring_coverage(code_with_docs)
print(f"Coverage: {coverage['coverage']:.1f}%")
print(f"Total items: {coverage['total']}")
print(f"Documented: {coverage['documented']}")
print(f"Missing: {coverage['missing']}")

print("\n✨ Demo complete!")
