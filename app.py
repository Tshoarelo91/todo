from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple in-memory storage
todos = []

@app.route('/')
def hello():
    return 'Todo API is running!'

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    todo = request.json
    todo['id'] = len(todos) + 1
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo:
        data = request.json
        todo.update(data)
        return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo:
        todos.remove(todo)
        return '', 204
    return jsonify({'error': 'Todo not found'}), 404
