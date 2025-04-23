from flask import Flask, render_template, request, jsonify
import os
import subprocess
import tempfile
import json
from pathlib import Path
import sys

app = Flask(__name__)

# Get the absolute path to the project root
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def check_tools():
    """Check if required tools are installed"""
    tools = {
        'gcc': 'MinGW-w64',
        'win_flex': 'WinFlexBison',
        'win_bison': 'WinFlexBison'
    }
    
    missing_tools = []
    for tool, package in tools.items():
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(f"{tool} (from {package})")
    
    return missing_tools

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        # Check for required tools
        missing_tools = check_tools()
        if missing_tools:
            return jsonify({
                'success': False,
                'error': f"Missing required tools: {', '.join(missing_tools)}. Please install them first."
            })

        code = request.json.get('code', '')
        input_data = request.json.get('input', '')
        
        # Create a temporary file for the MiniC code
        with tempfile.NamedTemporaryFile(suffix='.mc', delete=False) as temp_mc:
            temp_mc.write(code.encode())
            temp_mc_path = temp_mc.name
        
        # Create a temporary file for the output
        with tempfile.NamedTemporaryFile(suffix='.uco', delete=False) as temp_uco:
            temp_uco_path = temp_uco.name
        
        try:
            # Check if compiler exists
            minic_path = PROJECT_ROOT / 'minic.exe'
            if not minic_path.exists():
                return jsonify({
                    'success': False,
                    'error': f"Compiler not found at {minic_path}. Please run build.bat first."
                })

            # Compile the MiniC code
            compile_result = subprocess.run(
                [str(minic_path), temp_mc_path],
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT)
            )
            
            if compile_result.returncode != 0:
                return jsonify({
                    'success': False,
                    'error': compile_result.stderr or 'Compilation failed'
                })
            
            # Check if interpreter exists
            ucodei_path = PROJECT_ROOT / 'ucodei.exe'
            if not ucodei_path.exists():
                return jsonify({
                    'success': False,
                    'error': f"Interpreter not found at {ucodei_path}. Please run build.bat first."
                })

            # Run the compiled code
            process = subprocess.Popen(
                [str(ucodei_path), temp_uco_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(PROJECT_ROOT)
            )
            
            # Send input and get output
            stdout, stderr = process.communicate(input=input_data)
            
            return jsonify({
                'success': True,
                'output': stdout or 'No output',
                'error': stderr or ''
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Execution error: {str(e)}'
            })
        finally:
            # Clean up temporary files
            if os.path.exists(temp_mc_path):
                os.unlink(temp_mc_path)
            if os.path.exists(temp_uco_path):
                os.unlink(temp_uco_path)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000) 