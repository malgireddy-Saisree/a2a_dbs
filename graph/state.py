# graph/state.py

from typing import TypedDict, Optional, Any

class GraphState(TypedDict):
    query: str
    db_choice: Optional[str]
    action: Optional[str]
    db_query: Optional[Any]
    db_result: Optional[Any]
    final_answer: Optional[str]