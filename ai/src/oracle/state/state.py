"""State models for ORACLE.

Define global state representations used by agents and the graph. Kept minimal
and Pydantic-based for validation and forward-compatibility.
"""
from pydantic import BaseModel


class State(BaseModel):
    """Minimal runtime state for the initial agent scaffold.

    The field is intentionally simple so agents can receive a single input string
    and return a structured response without introducing orchestration logic.
    """

    user_input: str = ""
