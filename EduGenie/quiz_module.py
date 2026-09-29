import json
import re

from gemini_client import generate_text
from prompts import EDUCATOR_SYSTEM, quiz_prompt


def clean_json_block(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text


def _validate_quiz(data: object) -> list[dict]:
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ValueError("Quiz response must contain a questions array.")
    questions = data["questions"]
    if len(questions) != 3:
        raise ValueError("Quiz must contain exactly 3 questions.")
    validated = []
    for item in questions:
        if not isinstance(item, dict):
            raise ValueError("Each quiz question must be an object.")
        question = item.get("question")
        options = item.get("options")
        correct = item.get("correct_answer")
        explanation = item.get("explanation", "")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Every question needs text.")
        if not isinstance(options, list) or len(options) != 4 or not all(isinstance(x, str) for x in options):
            raise ValueError("Every question must have exactly 4 text options.")
        if not isinstance(correct, int) or correct not in range(4):
            raise ValueError("correct_answer must be an option index from 0 to 3.")
        validated.append({
            "question": question.strip(),
            "options": [x.strip() for x in options],
            "correct_answer": correct,
            "explanation": str(explanation).strip(),
        })
    return validated


def generate_quiz(source: str) -> list[dict]:
    raw = generate_text(
        quiz_prompt(source),
        system_instruction=EDUCATOR_SYSTEM,
        max_output_tokens=1400,
    )
    try:
        data = json.loads(clean_json_block(raw))
        return _validate_quiz(data)
    except (json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(f"Gemini returned an invalid quiz format: {exc}") from exc
