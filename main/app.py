from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demonstration
data_store = []

@app.route('/')
def home():
    """Homepage route"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Lab Project</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f4f4f4;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
            }
            .endpoint {
                background-color: #e9ecef;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
            }
            code {
                background-color: #f8f9fa;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Flask Lab Project! 🚀</h1>
            <p>This is a simple Flask application with multiple endpoints.</p>
            
            <h2>Available Endpoints:</h2>
            <div class="endpoint">
                <strong>GET /</strong> - Homepage (you are here)
            </div>
            <div class="endpoint">
                <strong>GET /health</strong> - Health check endpoint
            </div>
            <div class="endpoint">
                <strong>POST /data</strong> - Submit data endpoint
            </div>
            <div class="endpoint">
                <strong>GET /data</strong> - Retrieve all submitted data
            </div>
            
            <h2>Test the API:</h2>
            <p>Use curl or Postman to test the POST endpoint:</p>
            <code>curl -X POST http://localhost:5000/data -H "Content-Type: application/json" -d '{"name":"test","value":"123"}'</code>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health_check():
    """Health check route"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'flask-lab-project',
        'version': '1.0.0'
    }), 200

@app.route('/data', methods=['POST'])
def create_data():
    """POST endpoint to receive data"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate that data exists
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body must contain JSON data'
            }), 400
        
        # Add timestamp and ID to the data
        data_entry = {
            'id': len(data_store) + 1,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store the data
        data_store.append(data_entry)
        
        return jsonify({
            'message': 'Data received successfully',
            'id': data_entry['id'],
            'data': data_entry
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to process data',
            'message': str(e)
        }), 500

@app.route('/data', methods=['GET'])
def get_data():
    """GET endpoint to retrieve all data"""
    return jsonify({
        'count': len(data_store),
        'data': data_store
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)