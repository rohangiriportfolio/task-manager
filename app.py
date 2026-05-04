from flask import Flask, jsonify, request, abort
from utils import validate_task

app = Flask(__name__)

tasks = []
next_id = 1

@app.route('/tasks')
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    title = data.get('title', '')
    description = data.get('description', '')

    is_valid, error = validate_task(title)
    if not is_valid:
        return jsonify({"error": error}), 400

    task = {
        "id": next_id,
        "title": title.strip(),
        "description": description.strip(),
        "done": False
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        abort(404, description="Task not found")
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        abort(404, description="Task not found")

    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    title = data.get('title', task['title'])

    is_valid, error = validate_task(title)
    if not is_valid:
        return jsonify({"error": error}), 400

    task['title'] = title.strip()
    task['description'] = data.get('description', task['description']).strip()
    task['done'] = data.get('done', task['done'])

    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        abort(404, description="Task not found")

    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
