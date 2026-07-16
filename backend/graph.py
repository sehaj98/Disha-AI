from langgraph.graph import StateGraph, START, END

from state import DishaState

from nodes.status_node import status_node
from nodes.profile_node import profile_node
from nodes.stream_node import stream_node
from nodes.upskill_node import upskill_node


workflow = StateGraph(DishaState)

workflow.add_node("status", status_node)
workflow.add_node("profile", profile_node)
workflow.add_node("stream", stream_node)
workflow.add_node("upskill", upskill_node)


def route_status(state: DishaState):
    if state["status"] == "dropout":
        return "upskill"
    return "profile"


workflow.add_edge(START, "status")

workflow.add_conditional_edges(
    "status",
    route_status,
    {
        "profile": "profile",
        "upskill": "upskill",
    },
)

workflow.add_edge("profile", "stream")
workflow.add_edge("stream", END)
workflow.add_edge("upskill", END)

graph = workflow.compile()