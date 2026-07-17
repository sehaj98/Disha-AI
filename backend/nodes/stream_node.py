from state import DishaState
from services.ai_service import generate_response


def stream_node(state: DishaState):

    prompt = (
        f"Student details -> Class: {state.get('student_class') or 'unknown'}, "
        f"Country: {state.get('country') or 'unknown'}, "
        f"Interests: {', '.join(state.get('interests', [])) or 'not specified'}.\n"
        f'Their message: "{state["messages"][-1]}"\n\n'
        "Recommend a suitable academic stream (Science, Commerce, or Arts, "
        "with a specific specialization if relevant) and 2-3 realistic career "
        "paths it opens up. Be specific to their interests, not a generic list."
    )

    state["response"] = generate_response(prompt)

    return state