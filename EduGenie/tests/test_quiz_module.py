import pytest

from quiz_module import clean_json_block, _validate_quiz


def test_clean_json_block():
    assert clean_json_block('```json\n{"a": 1}\n```') == '{"a": 1}'


def test_validate_quiz():
    data = {
        "questions": [
            {"question": f"Q{i}", "options": ["A", "B", "C", "D"], "correct_answer": i % 4, "explanation": "Because."}
            for i in range(3)
        ]
    }
    assert len(_validate_quiz(data)) == 3


def test_validate_quiz_rejects_wrong_count():
    with pytest.raises(ValueError):
        _validate_quiz({"questions": []})
