# agents/executor_agent.py
# -----------------------------------------------------------
# Executor Agent
#
# A2A role : RECEIVER from router_agent, SENDER to responder_agent
# Receives  : RouterDecision
# Returns   : DBResult
#
# Responsibility: run the DB command produced by the router
# against the real database and return raw results.
# No LLM involved — pure deterministic code.
# -----------------------------------------------------------

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dbs import sqlite_db, tinydb_db, redis_mock, graph_db
from protocol.messages import AgentCard, RouterDecision, DBResult


class ExecutorAgent:

    card = AgentCard(
        name="executor_agent",
        role="Database executor",
        version="1.0",
        description="Receives a RouterDecision, runs the command against the real DB, returns raw results."
    )

    # Map db_choice → handler function
    DB_HANDLERS = {
        "postgres": lambda cmd: sqlite_db.run(cmd),
        "mongo":    lambda cmd: tinydb_db.run(cmd),
        "redis":    lambda cmd: redis_mock.run(cmd),
        "neo4j":    lambda cmd: graph_db.run(cmd),
    }

    def invoke(self, decision: RouterDecision) -> DBResult:
        """
        Receive a RouterDecision from the router agent.
        Return a DBResult for the responder agent.
        """
        print(f"\n[{self.card.name}] ⚡ Executing → db={decision.db_choice} | cmd={decision.db_query}")

        handler = self.DB_HANDLERS.get(decision.db_choice)

        if not handler:
            return DBResult(
                task_id=decision.task_id,
                query=decision.query,
                action=decision.action,
                db_choice=decision.db_choice,
                data=f"❌ Unknown database: '{decision.db_choice}'",
                success=False,
                sender=self.card.name
            )

        try:
            raw = handler(decision.db_query)
            success = not (isinstance(raw, str) and raw.startswith("❌"))
            print(f"[{self.card.name}] ✅ Result: {str(raw)[:80]}...")
        except Exception as e:
            raw = f"❌ Execution error: {str(e)}"
            success = False
            print(f"[{self.card.name}] ❌ Error: {e}")

        return DBResult(
            task_id=decision.task_id,
            query=decision.query,
            action=decision.action,
            db_choice=decision.db_choice,
            data=raw,
            success=success,
            sender=self.card.name
        )


# Singleton instance
executor_agent = ExecutorAgent()