# agents/responder_agent.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm import call_llm

def responder_agent(state):
    query = state["query"]
    action = state.get("action", "read")
    db = state.get("db_choice", "unknown")
    result = state["db_result"]

    # Tailor the prompt based on whether it was a read or write
    if action in ("add", "update", "delete"):
        prompt = f"""
User asked: {query}

The system performed a write operation on the {db} database.
Result: {result}

Write a short, friendly confirmation message telling the user what was done.
If the result contains an error (starts with ❌), explain what went wrong clearly.
Keep it concise — 1-2 sentences max.
"""
    else:
        prompt = f"""
User asked: {query}

Database ({db}) returned:
{result}

Write a clean, helpful answer summarizing the data for the user.
Format any lists or tables in a readable way.
If the result is empty or an error, say so clearly.
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

    test_cases = [
        {
            "query": "Add user Tulasi",
            "action": "add",
            "db_choice": "postgres",
            "db_result": "✅ Query executed successfully"
        },
        {
            "query": "Get all users",
            "action": "read",
            "db_choice": "postgres",
            "db_result": [(1, "Sai"), (2, "John"), (3, "Alice")]
        }
    ]

    for state in test_cases:
        result = responder_agent(state)
        print(f"Query: {state['query']}")
        print(f"Answer: {result['final_answer']}\n")


if __name__ == "__main__":
    main()