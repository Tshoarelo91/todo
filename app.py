from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# In-memory storage
todos = []

def validate_todo(todo):
    if not todo.get('title'):
        return False, 'Title is required'
    
    status = todo.get('status', 'pending')
    if status not in ['pending', 'in_progress', 'completed']:
        return False, 'Invalid status'
    
    due_date = todo.get('due_date')
    if due_date:
        try:
            datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except ValueError:
            return False, 'Invalid due date format. Please use ISO format (YYYY-MM-DDTHH:mm:ss.sssZ)'
    
    return True, None

@app.route('/')
def hello():
    return jsonify({"message": "Todo API is running!"})

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    todo = request.json
    
    # Validate todo
    is_valid, error = validate_todo(todo)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    # Set default values
    todo['id'] = len(todos) + 1
    todo['status'] = todo.get('status', 'pending')
    todo['created_at'] = datetime.utcnow().isoformat() + 'Z'
    
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = next((t for t in todos if t['id'] == id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    updates = request.json
    
    # Validate updates
    is_valid, error = validate_todo({**todo, **updates})
    if not is_valid:
        return jsonify({'error': error}), 400
    
    # Update todo
    todo.update(updates)
    return jsonify(todo)

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = next((t for t in todos if t['id'] == id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    todos.remove(todo)
    return '', 204

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
