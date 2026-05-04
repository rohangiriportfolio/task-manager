import pytest
from utils import validate_task, format_task_response

def test_validate_task_with_valid_input():
    is_valid, msg = validate_task("Buy groceries")
    assert is_valid is True
    assert msg == ""

def test_validate_task_empty_title():
    is_valid, msg = validate_task("")
    assert is_valid is False
    assert "Title cannot be empty" in msg

def test_validate_task_too_long_title():
    long_title = "a" * 101
    is_valid, msg = validate_task(long_title)
    assert is_valid is False
    assert "too long" in msg

@pytest.mark.parametrize("title,expected_valid", [
    ("Valid task", True),
    ("", False),
    ("a"*100, True),
    ("a"*101, False),
    ("   ", False),
])
def test_validate_task_parametrized(title, expected_valid):
    is_valid, _ = validate_task(title)
    assert is_valid == expected_valid

def test_format_task_response():
    task = {"id": 1, "title": "Learn Docker", "done": False}
    formatted = format_task_response(task)
    assert "Learn Docker" in formatted
    assert "Done: False" in formatted
