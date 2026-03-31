# agents/executor_agent.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dbs import sqlite_db
from dbs import tinydb_db
from dbs import redis_mock
from dbs import graph_db


def executor_agent(state):
    db = state["db_choice"]
    action = state["action"]
    query = state["db_query"]

    print(f"⚡ Executing → {db} | Action → {action}")

    try:
        if db == "postgres":
            result = sqlite_db.run(query)

        elif db == "mongo":
            result = tinydb_db.run(query)

        elif db == "redis":
            result = redis_mock.run(query)

        elif db == "neo4j":
            result = graph_db.run(query)

        else:
            result = "❌ Unknown DB"

    except Exception as e:
        result = f"❌ Error: {str(e)}"

    return {
        **state,
        "db_result": result
    }


# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("🔍 Testing Executor Agent...\n")

    test_cases = [
        {
            "db_choice": "postgres",
            "action": "read",
            "db_query": "SELECT * FROM users"
        },
        {
            "db_choice": "mongo",
            "action": "read",
            "db_query": "electronics"
        },
        {
            "db_choice": "redis",
            "action": "read",
            "db_query": "GET session:abc123"
        },
        {
            "db_choice": "neo4j",
            "action": "read",
            "db_query": "friends of Sai"
        }
    ]

    for i, state in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}:")
        result = executor_agent(state)
        print("📊 Result:", result["db_result"])


# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()