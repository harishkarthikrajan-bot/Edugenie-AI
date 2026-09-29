from gemini_client import generate_text
from prompts import EDUCATOR_SYSTEM, summary_prompt


def summarize_text(text: str) -> str:
    return generate_text(summary_prompt(text), system_instruction=EDUCATOR_SYSTEM, max_output_tokens=1000)
