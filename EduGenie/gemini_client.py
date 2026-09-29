from functools import lru_cache

from config import settings


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    if not settings.gemini_api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. Add it to the .env file."
        )
    from google import genai
    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(prompt: str, *, system_instruction: str | None = None, max_output_tokens: int = 1200) -> str:
    from google.genai import types
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=0.4,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
