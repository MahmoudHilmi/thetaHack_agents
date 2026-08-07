"""State models for ORACLE.

Define global state representations used by agents and the graph. Kept minimal
and Pydantic-based for validation and forward-compatibility.
"""
from pydantic import BaseModel


class State(BaseModel):
    """Global runtime state placeholder.

    Extend this model with the actual state fields when implementing business logic.
    """
    pass
