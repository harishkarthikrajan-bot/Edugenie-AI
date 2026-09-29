from config import settings
from gemini_client import generate_text
from prompts import EDUCATOR_SYSTEM, explain_prompt


def _local_explanation(topic: str) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires the optional transformers and torch packages. "
            "Install with: pip install -r requirements-local.txt"
        ) from exc

    generator = pipeline("text2text-generation", model=settings.local_explanation_model)
    prompt = (
        "Explain this topic to a beginner in simple language with a definition and one example: "
        + topic
    )
    result = generator(prompt, max_new_tokens=180, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    if settings.explanation_provider == "local":
        return _local_explanation(topic)
    return generate_text(explain_prompt(topic), system_instruction=EDUCATOR_SYSTEM, max_output_tokens=700)
