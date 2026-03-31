# agents/router_agent.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import re
from llm import call_llm   # ✅ correct import


def router_agent(state):
    query = state["query"]

    prompt = f"""
You are a database routing agent.

User Query: {query}

Databases:
- postgres → users, orders (SQL → SQLite)
- mongo → products (TinyDB)
- redis → sessions, cache
- neo4j → friendships, relationships

IMPORTANT RULES:
- Decide the correct database
- Generate VALID query/action
- Support CRUD operations
- DO NOT include markdown or ```json
- Return ONLY raw JSON

Format:
{{
  "db_choice": "postgres|mongo|redis|neo4j",
  "action": "read|add|update|delete",
  "db_query": "query string OR structured JSON",
  "reason": "short reason"
}}
"""

    response = call_llm(prompt)

    print("\n🔍 RAW LLM RESPONSE:\n", response)

    # -------------------------------
    # 🔥 CLEAN RESPONSE (REMOVE MARKDOWN)
    # -------------------------------
    cleaned = re.sub(r"```json|```", "", response).strip()
    cleaned = cleaned.strip("`").strip()

    print("\n🧹 CLEANED RESPONSE:\n", cleaned)

    # -------------------------------
    # 🔥 SAFE JSON PARSE
    # -------------------------------
    try:
        parsed = json.loads(cleaned)
    except Exception as e:
        print("❌ JSON PARSE ERROR")
        print("Response was:", cleaned)
        raise ValueError("❌ LLM returned invalid JSON")

    print("\n🧠 Parsed Decision:", parsed)

    return {
        **state,
        "db_choice": parsed.get("db_choice"),
        "action": parsed.get("action"),
        "db_query": parsed.get("db_query")
    }


# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("🔍 Testing Router Agent...\n")

    test_queries = [
        "Get all users",
        "Show all electronics products",
        "Get session details",
        "Find friends of Sai",
        "Add a new product iPad price 800 category electronics"
    ]

    for i, q in enumerate(test_queries, 1):
        print(f"\n🧪 Test Case {i}: {q}")

        state = {
            "query": q
        }

        try:
            result = router_agent(state)
            print("✅ Final Output:", result)

        except Exception as e:
            print("❌ Error:", e)


# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()