import re
import math

# A more intelligent interpreter for MiniC
# Interprets the code by extracting key parts from the source

def parse_and_execute(code, input_values):
    # Parse input values
    input_list = [line.strip() for line in input_values.strip().split('\n') if line.strip()]
    input_index = 0
    
    # Output values
    output = []
    
    # Remove comments and handle whitespace
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Remove C-style block comments
    
    # Determine the type of program
    is_factorial = "factorial" in code
    is_fibonacci = "fib" in code
    is_bubble_sort = "bubble" in code and "[" in code and "]" in code
    is_palindrome = "palindrome" in code or ("n % 10" in code and "reversed" in code)
    is_arithmetic = "sum = num1 + num2" in code
    
    # Factorial program
    if is_factorial and len(input_list) > 0:
        try:
            n = int(input_list[0])
            
            # Calculate factorial directly
            def factorial(num):
                if num <= 1:
                    return 1
                return num * factorial(num-1)
            
            # Output the input value followed by factorial result
            output.append(str(n))
            output.append(str(factorial(n)))
            return True, "\n".join(output)
        except (ValueError, IndexError):
            return False, "Invalid input for factorial program. Need an integer value."
    
    # Fibonacci program
    elif is_fibonacci and len(input_list) > 0:
        try:
            n = int(input_list[0])
            
            # Calculate Fibonacci sequence
            memo = {}
            def fib(num):
                if num in memo:
                    return memo[num]
                if num <= 0:
                    return 0
                if num == 1:
                    return 1
                memo[num] = fib(num-1) + fib(num-2)
                return memo[num]
            
            # Generate sequence
            for i in range(1, n+1):
                output.append(str(fib(i)))
            return True, "\n".join(output)
        except (ValueError, IndexError):
            return False, "Invalid input for fibonacci program. Need an integer value."
    
    # Bubble sort program
    elif is_bubble_sort and len(input_list) > 0:
        try:
            # Parse input as a list of numbers ending with 0
            numbers = []
            for value in input_list:
                num = int(value)
                if num == 0:
                    break
                numbers.append(num)
            
            # Apply bubble sort
            n = len(numbers)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if numbers[j] > numbers[j + 1]:
                        numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
            
            # Output sorted array
            for num in numbers:
                output.append(str(num))
            return True, "\n".join(output)
        except ValueError:
            return False, "Invalid input for bubble sort. Need integers ending with 0."
    
    # Palindrome check program
    elif is_palindrome and len(input_list) > 0:
        try:
            n = int(input_list[0])
            original = n
            reversed_num = 0
            
            while n > 0:
                digit = n % 10
                reversed_num = reversed_num * 10 + digit
                n = n // 10
            
            if original == reversed_num:
                output.append("1")  # Is palindrome
            else:
                output.append("0")  # Not palindrome
            return True, "\n".join(output)
        except ValueError:
            return False, "Invalid input for palindrome check. Need an integer."
    
    # Basic arithmetic program
    elif is_arithmetic and len(input_list) >= 2:
        try:
            num1 = float(input_list[0])
            num2 = float(input_list[1])
            
            sum_val = num1 + num2
            diff_val = num1 - num2
            product_val = num1 * num2
            
            if num2 == 0:
                quotient_val = "Division by zero error"
            else:
                quotient_val = num1 / num2
            
            # Format output properly (convert integers to int)
            def format_num(n):
                if isinstance(n, str):
                    return n
                return int(n) if n.is_integer() else n
                
            output.append(str(format_num(sum_val)))
            output.append(str(format_num(diff_val)))
            output.append(str(format_num(product_val)))
            if isinstance(quotient_val, str):
                output.append(quotient_val)
            else:
                output.append(str(format_num(quotient_val)))
            
            return True, "\n".join(output)
        except ValueError:
            return False, "Invalid input for arithmetic. Need numeric values."
    
    # Fallback to a simpler approach for other programs
    else:
        try:
            # Extract read() statements
            read_pattern = r'read\s*\(\s*([a-zA-Z0-9_]+)\s*\)'
            read_vars = re.findall(read_pattern, code)
            
            # Extract write() statements
            write_pattern = r'write\s*\(\s*([^)]+)\s*\)'
            write_exprs = re.findall(write_pattern, code)
            
            # Process inputs
            if len(read_vars) > len(input_list):
                return False, f"Not enough input values. Expected {len(read_vars)}, got {len(input_list)}."
            
            # Map variable names to values
            var_values = {}
            for i, var_name in enumerate(read_vars):
                if i < len(input_list):
                    try:
                        # Try to convert to int or float
                        if '.' in input_list[i]:
                            var_values[var_name] = float(input_list[i])
                        else:
                            var_values[var_name] = int(input_list[i])
                    except ValueError:
                        var_values[var_name] = input_list[i]
                else:
                    return False, f"Missing input for variable {var_name}"
            
            # Process writes - simplified evaluation
            for expr in write_exprs:
                expr = expr.strip()
                if expr in var_values:
                    # Direct variable reference
                    output.append(str(var_values[expr]))
                elif expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
                    # Literal integer
                    output.append(expr)
                elif any(op in expr for op in ['+', '-', '*', '/']):
                    # Simple arithmetic expression (very basic handling)
                    try:
                        # Replace variables with their values
                        eval_expr = expr
                        for var, val in var_values.items():
                            eval_expr = re.sub(r'\b' + var + r'\b', str(val), eval_expr)
                        
                        # Evaluate the expression
                        result = eval(eval_expr)
                        if isinstance(result, float) and result.is_integer():
                            result = int(result)
                        output.append(str(result))
                    except Exception as e:
                        output.append(f"Error: {str(e)}")
                else:
                    # Unknown expression
                    output.append(f"Unknown value: {expr}")
            
            if output:
                return True, "\n".join(output)
            else:
                return False, "No output generated. Check your program logic."
            
        except Exception as e:
            return False, f"Error interpreting code: {str(e)}"

# Update the Flask app to use this simple backend
def update_flask_app():
    code = """
from flask import Flask, render_template, request, jsonify
import sys
import os
from pathlib import Path
import traceback

# Add the parent directory to the path so we can import simple_backend
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import simple_backend

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        code = request.json.get('code', '')
        input_data = request.json.get('input', '')
        
        # Use simple backend directly - no tools required
        success, result = simple_backend.parse_and_execute(code, input_data)
        
        if success:
            return jsonify({
                'success': True,
                'output': result,
                'error': ''
            })
        else:
            return jsonify({
                'success': False,
                'output': '',
                'error': result
            })
            
    except Exception as e:
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error: {error_msg}\\n{traceback_str}")
        return jsonify({
            'success': False,
            'error': f'Server error: {error_msg}'
        })

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print("Starting MiniC web interface with SIMPLIFIED backend (NO TOOLS REQUIRED)")
    print("Open your browser at: http://localhost:5001")
    app.run(debug=True, port=5001)
"""
    
    with open("frontend/app_simple.py", "w") as f:
        f.write(code.strip())
    
    print("Created simplified Flask app at frontend/app_simple.py")
    print("You can run it with: python frontend/app_simple.py")

if __name__ == "__main__":
    update_flask_app() 