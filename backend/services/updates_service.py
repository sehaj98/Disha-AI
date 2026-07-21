from services.search_service import search_web
from services.ai_service import client as groq_client, MODEL


def build_query(student) -> str:
    """Turns a stored student profile into a search query. This is the
    piece that makes updates 'class-aware' — a class 9 student and a
    class 12 student searching the same interest get different results
    because the class number is baked into the query itself."""
    parts = []
    if student.current_class:
        parts.append(f"for class {student.current_class} students in India")
    if student.interests:
        parts.append(" ".join(student.interests))
    parts.append("scholarships opportunities competitions 2026")
    return " ".join(parts)


def get_updates_for_student(student) -> str:
    """The core of the 'automatic updates' feature: searches the live web
    for this specific student's stage + interests, then has the AI turn
    the raw results into a short personal digest."""
    query = build_query(student)
    results = search_web(query)

    if not results:
        return (
            "I couldn't find fresh updates right now — this can happen if "
            "the search service is briefly unavailable. Try refreshing in "
            "a little while."
        )

    sources_text = "\n\n".join(
        f"- {r.get('title')}: {r.get('content', '')[:300]}" for r in results[:5]
    )

    prompt = (
        f"Student profile -> Class: {student.current_class or 'unknown'}, "
        f"Interests: {', '.join(student.interests or []) or 'not specified'}, "
        f"Country: {student.country or 'unknown'}.\n\n"
        f"Current web search results:\n{sources_text}\n\n"
        "Write a short, encouraging personalized update (under 150 words) "
        "highlighting 2-3 of the most relevant items above for this exact "
        "student. Mention them by name. Plain language, no headings or "
        "markdown, only reference the sources given."
    )

    completion = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Disha, turning real search results into a short "
                    "personal update for one student. Never invent facts that "
                    "aren't in the sources given."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=320,
    )
    return completion.choices[0].message.content.strip()
    