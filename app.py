from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Use a global variable for todos in serverless environment
TODOS = []

# Valid status values
VALID_STATUSES = ['pending', 'in_progress', 'completed']

@app.route('/')
def hello():
    return jsonify({"message": "Todo API is running!"})

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(TODOS)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({"error": "Title is required"}), 400
        
        new_todo = {
            'id': len(TODOS) + 1,
            'title': data['title'],
            'status': data.get('status', 'pending')  # Default to pending
        }
        
        if new_todo['status'] not in VALID_STATUSES:
            return jsonify({"error": "Invalid status. Must be one of: pending, in_progress, completed"}), 400
            
        TODOS.append(new_todo)
        return jsonify(new_todo), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    try:
        todo = next((t for t in TODOS if t['id'] == todo_id), None)
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        data = request.get_json()
        if 'title' in data:
            todo['title'] = data['title']
        if 'status' in data:
            if data['status'] not in VALID_STATUSES:
                return jsonify({"error": "Invalid status. Must be one of: pending, in_progress, completed"}), 400
            todo['status'] = data['status']
        return jsonify(todo)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todo = next((t for t in TODOS if t['id'] == todo_id), None)
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        TODOS.remove(todo)
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
