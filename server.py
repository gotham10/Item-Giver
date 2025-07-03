from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

pending_items = {}
item_list = []

try:
    with open('items.json', 'r') as f:
        item_list = json.load(f)
except FileNotFoundError:
    print("Warning: items.json not found. Autocomplete will not work.")

@app.route('/give-item', methods=['POST'])
def handle_give_item():
    data = request.get_json()
    if not data or not data.get('itemId') or not data.get('userId'):
        return jsonify({"message": "itemId and userId are required"}), 400
    
    user_id = str(data['userId'])
    item_data = {
        "Id": data.get('itemId'),
        "Index": data.get('index'),
        "Stack": data.get('stack')
    }
    pending_items[user_id] = item_data
    return jsonify({"message": "Item queued for user " + user_id}), 200

@app.route('/get-item/<user_id>', methods=['GET'])
def handle_get_item(user_id):
    user_id_str = str(user_id)
    if user_id_str in pending_items:
        item = pending_items.pop(user_id_str)
        return jsonify(item)
    return jsonify(None)

@app.route('/get-all-items', methods=['GET'])
def get_all_items():
    return jsonify(item_list)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
