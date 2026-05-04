def validate_task(title, description=""):
    if not title or not title.strip():
        return False, "Title cannot be empty"
    if len(title) > 100:
        return False, "Title too long (max 100 characters)"
    return True, ""

def format_task_response(task):
    return f"Task: {task['title']} | Done: {task['done']}"
