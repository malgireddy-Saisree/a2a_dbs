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
    user_query = state.get("user_query", query)

    print(f"\n⚡ Executing → DB: {db} | Action: {action} | Query: {query}")

    try:
        if db == "postgres":
            # sqlite_db.run() handles SELECT vs INSERT/UPDATE/DELETE internally
            result = sqlite_db.run(query)

        elif db == "mongo":
            # tinydb_db.run() uses GET/INSERT/UPDATE/DELETE command format
            result = tinydb_db.run(query)

        elif db == "redis":
            # redis_mock.run() uses GET/SET/DELETE/INCR/ALL command format
            result = redis_mock.run(query)

        elif db == "neo4j":
            # graph_db.run() uses natural language commands
            result = graph_db.run(query)

        else:
            result = f"❌ Unknown database: '{db}'"

    except Exception as e:
        result = f"❌ Execution Error: {str(e)}"

    # Confirm writes with a clear message
    if action in ("add", "update", "delete") and isinstance(result, str):
        print(f"✅ Write operation result: {result}")

    return {
        **state,
        "db_result": result
    }