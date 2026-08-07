"""Minimal climate agent implementation."""

from typing import Any

from oracle.state.state import State


class ClimateAgent:
    """Climate-focused agent that reads state and returns a response.

    This is intentionally minimal and does not implement RAG, memory, or
    orchestration. It only consumes the current state and returns a simple,
    structured response for future integration into the graph.
    """

    def __init__(self) -> None:
        self.name = "climate"

    def run(self, state: State) -> dict[str, Any]:
        """Return a structured climate analysis response from the given state."""
        prompt = state.user_input.strip() or "No input provided"
        return {
            "agent": self.name,
            "response": f"Climate analysis: {prompt}",
        }



