import re
from state import DishaState

def profile_node(state: DishaState):

    message = state["messages"][-1].lower()

    # Extract class
    match = re.search(r'class\s*(\d+)', message)
    if match:
        state["student_class"] = match.group(1)

    # Extract country
    if "india" in message:
        state["country"] = "India"

    # Extract interests
    interests = []

    keywords = [
        "coding",
        "computer",
        "biology",
        "business",
        "math",
        "physics",
        "chemistry",
        "design",
        "art"
    ]

    for word in keywords:
        if word in message:
            interests.append(word)

    state["interests"] = interests

    return state