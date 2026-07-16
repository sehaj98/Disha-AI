from state import DishaState

def upskill_node(state: DishaState):

    state["response"] = (
        "You can restart your learning journey by learning digital skills like "
        "Python, Web Development, Graphic Design, Digital Marketing, or Data Analytics."
    )

    return state