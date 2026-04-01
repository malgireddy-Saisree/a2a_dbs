#!/usr/bin/env python3
# main.py
# -----------------------------------------------------------
# CLI entry point for the A2A multi-agent system.
#
# Flow:
#   User types query
#     → wrapped in A2AMessage
#     → sent through LangGraph (router → executor → responder)
#     → A2AResponse printed to terminal
# -----------------------------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from protocol.messages import A2AMessage
from graph.langgraph_builder import build_graph

# Compile graph once at startup
graph = build_graph()


def run_query(query: str):
    """Wrap a query in an A2AMessage and run it through the graph."""

    # Create the A2A message (CLI is the sender)
    message = A2AMessage(query=query, sender="cli")

    print(f"\n{'='*60}")
    print(f"📨 Task ID : {message.task_id}")
    print(f"❓ Query   : {query}")
    print(f"{'='*60}")

    # Invoke the graph
    final_state = graph.invoke({"message": message, "decision": None, "db_result": None, "response": None})

    # Extract the A2AResponse
    response = final_state["response"]

    print(f"\n{'='*60}")
    print(f"✅ Task ID : {response.task_id}")
    print(f"📤 From    : {response.sender}")
    print(f"📊 Status  : {response.status}")
    print(f"\n💬 Answer:\n{response.answer}")
    print(f"{'='*60}\n")

    return response


def main():
    print("\n🤖 A2A Multi-Agent System")
    print("   Agents: RouterAgent → ExecutorAgent → ResponderAgent")
    print("   Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            query = input("💬 Ask: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Bye!")
            break

        if not query:
            continue

        if query.lower() in ("exit", "quit", "q"):
            print("👋 Bye!")
            break

        try:
            run_query(query)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()