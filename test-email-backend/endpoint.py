from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import threading
import os

app = Flask(__name__)
CORS(app)

@app.route('/emails', methods=['GET'])
def get_emails():
    log_path = 'log.log'
    if not os.path.exists(log_path):
        return Response('No emails found.', mimetype='text/plain')
    with open(log_path, 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/plain')

@app.route('/')
def home():
    return 'Flask endpoint is running!'

@app.route('/status')
def status():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
