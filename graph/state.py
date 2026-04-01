# graph/state.py

from typing import TypedDict, Optional, Any

class GraphState(TypedDict):
    query: str                    # Original user query (natural language)
    user_query: Optional[str]     # Preserved user query passed through pipeline
    db_choice: Optional[str]      # Which DB: postgres | mongo | redis | neo4j
    action: Optional[str]         # Operation type: read | add | update | delete
    db_query: Optional[Any]       # Exact executable command for the DB
    db_result: Optional[Any]      # Raw result returned from the DB
    final_answer: Optional[str]   # Human-readable answer from responder