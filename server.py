from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

item_to_give = None
item_list = []

try:
    with open('items.json', 'r') as f:
        item_list = json.load(f)
except FileNotFoundError:
    pass

@app.route('/give-item', methods=['POST'])
def handle_give_item():
    global item_to_give
    data = request.get_json()
    if data and data.get('itemId'):
        item_to_give = {
            "Id": data.get('itemId'),
            "Index": data.get('index'),
            "Stack": data.get('stack')
        }
        return jsonify({"message": "Item queued"}), 200
    return jsonify({"message": "Invalid data"}), 400

@app.route('/get-item', methods=['GET'])
def handle_get_item():
    global item_to_give
    if item_to_give:
        response = jsonify(item_to_give)
        item_to_give = None
        return response
    return jsonify(None)

@app.route('/get-all-items', methods=['GET'])
def get_all_items():
    return jsonify(item_list)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
