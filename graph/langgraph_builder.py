# graph/builder.py

from langgraph.graph import StateGraph
from graph.state import GraphState

from agents.router_agent import router_agent
from agents.executor_agent import executor_agent
from agents.responder_agent import responder_agent

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("router", router_agent)
    builder.add_node("executor", executor_agent)
    builder.add_node("responder", responder_agent)

    builder.set_entry_point("router")

    builder.add_edge("router", "executor")
    builder.add_edge("executor", "responder")

    return builder.compile()