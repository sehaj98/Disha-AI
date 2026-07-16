from typing import TypedDict, List

class DishaState(TypedDict):

    messages: List[str]

    status: str

    student_class: str

    country: str

    interests: List[str]

    stream: str

    response: str