from django.conf import settings
from groq import Groq


def ask_groq(question, context):
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured.")

    client = Groq(
        api_key=settings.GROQ_API_KEY
    )

    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are FIDS AI, a professional football "
                    "intelligence analyst. Analyze matches, players, "
                    "teams and global football news. Use supplied data, "
                    "never invent statistics or transfer confirmations, "
                    "and answer in the user's language."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"FIDS Football Data:\n{context}"
                ),
            },
        ],
        temperature=0.3,
        max_completion_tokens=1800,
    )

    return completion.choices[0].message.content or ""