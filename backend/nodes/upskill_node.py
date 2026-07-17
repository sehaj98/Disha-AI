from state import DishaState
from services.ai_service import generate_response


def upskill_node(state: DishaState):

    prompt = (
        f'Their message: "{state["messages"][-1]}"\n\n'
        "This student has dropped out of school. Suggest 2-3 concrete "
        "upskilling paths (specific skills or courses, not vague categories) "
        "they could start learning now, and one realistic first step they "
        "could take this week."
    )

    state["response"] = generate_response(prompt)

    return state