from gemini_client import generate_text
from prompts import EDUCATOR_SYSTEM, qna_prompt


def answer_question(question: str) -> str:
    return generate_text(qna_prompt(question), system_instruction=EDUCATOR_SYSTEM, max_output_tokens=900)
