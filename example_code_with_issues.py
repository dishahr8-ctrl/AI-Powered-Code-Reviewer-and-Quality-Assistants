"""Example code with various severity issues for testing"""

# WARNING: Bad naming (should be snake_case)
def CalculateTotal(items):
    total = 0
    for item in items:
        total += item
    return total

# WARNING: Bad class naming (should be PascalCase)
class user_account:
    def __init__(self, name):
        self.userName = name
    
    # WARNING: Bad method naming (should be snake_case)
    def GetBalance(self):
        return 0

# WARNING: Missing docstring
def process_data(data):
    return [x * 2 for x in data]

# WARNING: High complexity
def complex_logic(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        return a + b + c + d + e
    return 0

# INFO: Formatting issues (spacing)
def calculate(x,y):
    return x+y

# INFO: Trailing whitespace and formatting
def format_test():
    x = 1   
    return x
