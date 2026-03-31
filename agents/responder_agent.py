# agents/responder_agent.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm import call_llm

def responder_agent(state):
    query = state["query"]
    result = state["db_result"]

    prompt = f"""
User asked: {query}

Database result:
{result}

Generate a clean, helpful answer.
"""

    answer = call_llm(prompt)

    return {
        **state,
        "final_answer": answer
    }


# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("🔍 Testing Responder Agent...\n")

    # Simulated state (like executor output)
    test_state = {
        "query": "Get all users",
        "db_result": [(1, "Sai"), (2, "John"), (3, "Alice")]
    }

    try:
        result = responder_agent(test_state)

        print("🧠 Final Answer:\n")
        print(result["final_answer"])

    except Exception as e:
        print("❌ Error:", e)


# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()