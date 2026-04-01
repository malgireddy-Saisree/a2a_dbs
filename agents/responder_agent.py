# agents/responder_agent.py
# -----------------------------------------------------------
# Responder Agent
#
# A2A role : RECEIVER from executor_agent, SENDER to CLI
# Receives  : DBResult
# Returns   : A2AResponse
#
# Responsibility: turn raw DB results into a clean,
# human-readable answer using the LLM.
# -----------------------------------------------------------

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import call_llm
from protocol.messages import AgentCard, DBResult, A2AResponse


class ResponderAgent:

    card = AgentCard(
        name="responder_agent",
        role="Answer generator",
        version="1.0",
        description="Receives raw DB results and produces a clean, human-readable answer via LLM."
    )

    def invoke(self, result: DBResult) -> A2AResponse:
        """
        Receive a DBResult from the executor agent.
        Return an A2AResponse for the CLI.
        """
        print(f"\n[{self.card.name}] 💬 Generating answer for task={result.task_id}")

        # Different prompt for reads vs writes
        if result.action in ("add", "update", "delete"):
            prompt = f"""
User asked: {result.query}

A {result.action} operation was performed on the {result.db_choice} database.
Result: {result.data}

Write a short, friendly confirmation (1-2 sentences).
If the result starts with ❌, explain what went wrong clearly.
"""
        else:
            prompt = f"""
User asked: {result.query}

The {result.db_choice} database returned:
{result.data}

Write a clean, helpful answer summarizing this data.
Format lists or tables readably. If empty or error, say so clearly.
"""

        try:
            answer = call_llm(prompt)
            status = "success" if result.success else "error"
        except Exception as e:
            answer = f"❌ Could not generate answer: {str(e)}"
            status = "error"

        print(f"[{self.card.name}] ✅ Answer ready")

        return A2AResponse(
            task_id=result.task_id,
            answer=answer,
            status=status,
            sender=self.card.name
        )


# Singleton instance
responder_agent = ResponderAgent()