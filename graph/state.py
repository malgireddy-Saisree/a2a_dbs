# graph/state.py
# -----------------------------------------------------------
# GraphState holds the A2A typed messages as they travel
# through the LangGraph pipeline.
#
# Each field corresponds to a protocol message type —
# the agents don't share a raw dict, they read/write
# typed dataclass objects stored here.
# -----------------------------------------------------------

from typing import TypedDict, Optional
from protocol.messages import A2AMessage, RouterDecision, DBResult, A2AResponse


class GraphState(TypedDict):
    
    message: A2AMessage

   
    decision: Optional[RouterDecision]

    
    db_result: Optional[DBResult]

    
    response: Optional[A2AResponse]