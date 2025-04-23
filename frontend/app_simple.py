from flask import Flask, render_template, request, jsonify
import sys
import os
from pathlib import Path
import traceback
from flask_cors import CORS

# Add the parent directory to the path so we can import simple_backend
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import simple_backend

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST', 'OPTIONS'])
def compile_code():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
        
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
        print(f"Error: {error_msg}\n{traceback_str}")
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
    app.run(debug=True, port=5001, host='0.0.0.0')