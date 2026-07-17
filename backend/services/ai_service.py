import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=20.0,      # fail fast instead of hanging forever on a stalled connection
    max_retries=2,     # automatically retry once or twice on a transient network blip
)

# openai/gpt-oss-20b is Groq's current recommended free-tier general model
# (fast, no card required, generous daily limits as of mid-2026).
MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = (
    "You are Disha, a warm, encouraging guidance counselor for Indian "
    "students who are either choosing a stream or restarting after "
    "dropping out. Give a specific, concrete answer based on exactly what "
    "the student told you — never a generic list of every option. Keep it "
    "under 120 words, plain language, no headings or markdown."
)


def generate_response(prompt: str) -> str:
    """Calls Groq's chat completions API and returns the model's reply.
    Falls back to a friendly error message if the API call fails, so a
    bad key or a rate limit never crashes the /chat endpoint."""
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_tokens=300,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print("AI service error:", e)
        return (
            "I'm having trouble reaching the AI service right now. "
            "Please try again in a moment."
        )