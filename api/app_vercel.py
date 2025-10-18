"""
Anomalyze - Network Intrusion Detection System
Vercel Frontend - Calls Render API for predictions
"""

from __future__ import annotations
from flask import Flask, render_template, request, jsonify
import requests
import os
from pathlib import Path

# Get the directory where this file is located
BASE_DIR = Path(__file__).parent.absolute()

# Initialize Flask with explicit paths
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

# API endpoint for Render service
API_URL = os.environ.get('ANOMALYZE_API_URL', 'http://localhost:10000')


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', results=None, accuracy=None)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and send to API for prediction."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Forward file to API server
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(f'{API_URL}/api/predict', files=files, timeout=300)
        
        # Handle different response status codes
        if response.status_code == 400:
            # Validation error (bad request)
            try:
                error_data = response.json()
                error_msg = error_data.get('error', 'Invalid file format')
                error_type = error_data.get('error_type', 'unknown')
                
                return render_template('index.html', 
                                     error=error_msg,
                                     error_type='validation',
                                     results=None, 
                                     accuracy=None)
            except:
                return render_template('index.html', 
                                     error='Invalid file format. Please upload a valid NSL-KDD network traffic log.',
                                     error_type='validation',
                                     results=None, 
                                     accuracy=None)
        
        elif response.status_code != 200:
            # Other API errors (500, etc.)
            try:
                error_data = response.json()
                error_msg = error_data.get('error', response.text)
                details = error_data.get('details', '')
            except:
                error_msg = response.text
                details = ''
            
            return render_template('index.html', 
                                 error=f"API Error: {error_msg}",
                                 error_details=details,
                                 error_type='server',
                                 results=None, 
                                 accuracy=None)
        
        result = response.json()
        
        if not result.get('success'):
            error_msg = result.get('error', 'Unknown error')
            error_type = result.get('error_type', 'unknown')
            details = result.get('details', '')
            
            return render_template('index.html', 
                                 error=error_msg,
                                 error_details=details,
                                 error_type=error_type,
                                 results=None, 
                                 accuracy=None)
        
        # Render results
        anomalies = result.get('anomalies', [])
        metrics = result.get('metrics', {})
        
        return render_template('index.html', 
                             results=anomalies, 
                             metrics=metrics,
                             accuracy=metrics.get('accuracy'))
        
    except requests.exceptions.Timeout:
        return render_template('index.html', 
                             error='API request timed out. The file may be too large or the server is busy.',
                             error_type='timeout',
                             results=None, 
                             accuracy=None)
    except requests.exceptions.RequestException as e:
        return render_template('index.html', 
                             error=f'API connection error: {str(e)}',
                             error_type='connection',
                             results=None, 
                             accuracy=None)
    except Exception as e:
        return render_template('index.html', 
                             error=f'Error processing file: {str(e)}',
                             error_type='unknown',
                             results=None, 
                             accuracy=None)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check health of frontend and backend API."""
    try:
        response = requests.get(f'{API_URL}/health', timeout=5)
        api_status = response.json() if response.status_code == 200 else {'status': 'unhealthy'}
    except Exception as e:
        api_status = {'status': 'error', 'message': str(e)}
    
    return jsonify({
        'frontend': 'healthy',
        'api': api_status,
        'api_url': API_URL
    })


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information from API."""
    try:
        response = requests.get(f'{API_URL}/api/model-info', timeout=10)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to fetch model info'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 503


if __name__ == '__main__':
    print(f"Starting Anomalyze Frontend...")
    print(f"API URL: {API_URL}")
    app.run(debug=True, port=5000)
