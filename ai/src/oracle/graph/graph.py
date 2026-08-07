"""LangGraph graph scaffold for ORACLE.

This module creates the graph entry point for future orchestration. For Step 5,
we connect a single climate agent node to the graph without adding any other
agents.
"""

from typing import Any

from langgraph.graph import StateGraph

from oracle.agents.climate_agent import ClimateAgent
from oracle.state.state import State

__all__ = ["build_graph"]


def climate_node(state: State) -> dict[str, Any]:
    """Run the climate agent and store its response in the graph state."""
    agent = ClimateAgent()
    response = agent.run(state)
    return {"last_agent_response": response["response"]}


def build_graph() -> StateGraph:
    """Create a LangGraph graph with a single climate node."""
    graph = StateGraph(State)
    graph.add_node("climate", climate_node)
    graph.set_entry_point("climate")
    return graph



