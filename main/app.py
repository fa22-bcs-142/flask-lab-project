from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Flask Lab Project</h1><p>Welcome to our collaborative Flask app!</p>'

@app.route('/health')
def health():
    return jsonify({"status": "OK", "message": "Application is running"}), 200

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    return jsonify({
        "received": data,
        "message": "Data processed successfully"
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)