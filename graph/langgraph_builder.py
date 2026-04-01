# graph/builder.py
# -----------------------------------------------------------
# LangGraph orchestrator for A2A agents.
#
# Each node is a thin wrapper that:
#   1. Unpacks the typed message from GraphState
#   2. Calls agent.invoke(message)
#   3. Stores the typed response back into GraphState
#
# The agents themselves know NOTHING about LangGraph —
# they only speak in A2A protocol messages.
# This is the key A2A design: agents are independently
# testable without the graph.
# -----------------------------------------------------------

from langgraph.graph import StateGraph
from graph.state import GraphState
from agents.router_agent import router_agent
from agents.executor_agent import executor_agent
from agents.responder_agent import responder_agent


# -----------------------------------------------------------
# Node wrappers — translate GraphState <-> A2A messages
# -----------------------------------------------------------

def router_node(state: GraphState) -> GraphState:
    decision = router_agent.invoke(state["message"])
    return {**state, "decision": decision}


def executor_node(state: GraphState) -> GraphState:
    db_result = executor_agent.invoke(state["decision"])
    return {**state, "db_result": db_result}


def responder_node(state: GraphState) -> GraphState:
    response = responder_agent.invoke(state["db_result"])
    return {**state, "response": response}


# -----------------------------------------------------------
# Build and compile the graph
# -----------------------------------------------------------

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("router",    router_node)
    builder.add_node("executor",  executor_node)
    builder.add_node("responder", responder_node)

    builder.set_entry_point("router")
    builder.add_edge("router",   "executor")
    builder.add_edge("executor", "responder")

    return builder.compile()