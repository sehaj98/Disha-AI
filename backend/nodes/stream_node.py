from state import DishaState

def stream_node(state: DishaState):

    interests = " ".join(state.get("interests", [])).lower()

    if "coding" in interests or "computer" in interests:
        state["response"] = (
            "You may enjoy the Science stream with Computer Science. "
            "It can lead to careers in Software Engineering, AI, Data Science, and Cybersecurity."
        )

    elif "biology" in interests:
        state["response"] = (
            "You may enjoy the Science stream with Biology. "
            "It can lead to careers in Medicine, Pharmacy, Biotechnology, and Research."
        )

    elif "business" in interests:
        state["response"] = (
            "You may enjoy the Commerce stream. "
            "It can lead to careers in CA, Finance, Banking, and Business Management."
        )

    else:
        state["response"] = (
            "Based on your interests, explore different streams before making a final decision."
        )

    return state