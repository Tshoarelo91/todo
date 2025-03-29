from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Simple in-memory storage (using a list to store todos)
todos = []

@app.route('/')
def hello():
    return jsonify({"message": "Todo API is running!"})

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    todo = {
        'id': len(todos) + 1,
        'title': data['title'],
        'completed': data.get('completed', False)
    }
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    data = request.json
    if 'title' in data:
        todo['title'] = data['title']
    if 'completed' in data:
        todo['completed'] = data['completed']
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    todos.remove(todo)
    return '', 204

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
