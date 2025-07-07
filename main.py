import sys
from json import dumps, loads
from typing import final
from flask import Flask, render_template, request
from api import Api

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api_handler():
    if request.content_length and request.content_length > 1024 * 1024:
        return 'Request entity too large', 413

    try:
        data = request.get_json(force=True)
    except Exception as e:
        print('JSON parsing error:', e)
        return 'Invalid JSON', 400

    if not isinstance(data, list):
        return 'Expected list of IDs', 400

    ids = []
    for d in data:
        try:
            i = int(d)
            ids.append(i)
        except (ValueError, TypeError):
            return 'Data contains invalid ID', 400

    print(ids)

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
