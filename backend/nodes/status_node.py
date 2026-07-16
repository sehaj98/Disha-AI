from state import DishaState

def status_node(state: DishaState):

    message = state["messages"][-1].lower()

    dropout_words = [
        "dropout",
        "dropped out",
        "left school",
        "not studying",
        "quit school"
    ]

    if any(word in message for word in dropout_words):
        state["status"] = "dropout"
    else:
        state["status"] = "studying"

    return state