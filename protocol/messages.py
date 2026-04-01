# protocol/messages.py
# -----------------------------------------------------------
# A2A Protocol — typed messages passed between agents.
# Instead of sharing a raw dict, each agent sends and receives
# a well-defined message object. This is the A2A contract.
# -----------------------------------------------------------

from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
import time


def new_task_id() -> str:
    return str(uuid.uuid4())[:8]


@dataclass
class AgentCard:
    """
    Metadata about an agent — who it is and what it does.
    In a true A2A system this would be served at /.well-known/agent.json
    """
    name: str
    role: str
    version: str = "1.0"
    description: str = ""


@dataclass
class A2AMessage:
    """
    The initial message sent TO the router agent by the CLI.
    Carries the raw user query and a unique task id.
    """
    query: str
    task_id: str = field(default_factory=new_task_id)
    sender: str = "cli"
    timestamp: float = field(default_factory=time.time)


@dataclass
class RouterDecision:
    """
    What the router agent sends TO the executor agent.
    Contains the routing decision + the exact DB command to run.
    """
    task_id: str
    query: str                # original user query (kept for responder)
    db_choice: str            # postgres | mongo | redis | neo4j
    action: str               # read | add | update | delete
    db_query: str             # exact executable command
    reason: str = ""
    sender: str = "router_agent"


@dataclass
class DBResult:
    """
    What the executor agent sends TO the responder agent.
    Contains the raw result from the database.
    """
    task_id: str
    query: str                # original user query
    action: str               # read | add | update | delete
    db_choice: str
    data: Any                 # raw db result (rows, string, list, etc.)
    success: bool = True
    sender: str = "executor_agent"


@dataclass
class A2AResponse:
    """
    The final message produced by the responder agent.
    Returned to the CLI as the final answer.
    """
    task_id: str
    answer: str
    status: str = "success"   # success | error
    sender: str = "responder_agent"