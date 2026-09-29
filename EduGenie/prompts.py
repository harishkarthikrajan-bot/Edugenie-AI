EDUCATOR_SYSTEM = (
    "You are EduGenie, a friendly educational assistant. "
    "Give accurate, age-appropriate, concise explanations. "
    "When a question is ambiguous, state the assumption briefly. "
    "Do not invent citations or claim certainty when the answer is uncertain."
)


def qna_prompt(question: str) -> str:
    return f"Answer this student's academic/general knowledge question clearly:\n\n{question}"


def explain_prompt(topic: str) -> str:
    return (
        "Explain the following topic for a beginner. Use a short definition, "
        "simple language, one intuitive example, and 3 key points. Avoid unnecessary jargon.\n\n"
        f"Topic: {topic}"
    )


def summary_prompt(text: str) -> str:
    return (
        "Summarize the following educational text for quick revision. Preserve the core facts, "
        "remove repetition, and use concise bullet points when helpful.\n\n" + text
    )


def learning_path_prompt(topic: str) -> str:
    return (
        "Create a personalized learning path for the topic below. Organize it from beginner "
        "to advanced. Include stages, suggested timeline, practice activities, and resource "
        "types (videos, articles, books, documentation). Do not fabricate specific URLs.\n\n"
        f"Topic: {topic}"
    )


def quiz_prompt(source: str) -> str:
    return (
        "Create exactly 3 multiple-choice questions from the supplied topic/text. "
        "Each question must have exactly 4 options and exactly one correct answer. "
        "Return ONLY valid JSON in this shape: "
        '{"questions":[{"question":"...","options":["...","...","...","..."],"correct_answer":0,"explanation":"..."}]}.'
        "The correct_answer must be a zero-based option index. No Markdown fences.\n\n"
        f"Source:\n{source}"
    )
