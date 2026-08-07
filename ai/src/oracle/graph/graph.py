"""LangGraph graph orchestration for ORACLE multi-agent system.

Coordinates all agents (Climate, Economy, Health, Citizen, Ethics)
through a graph workflow and finalizes with Judge Agent.
"""

from typing import Any
from langgraph.graph import StateGraph, END

from oracle.agents.climate_agent import ClimateAgent
from oracle.agents.economy_agent import EconomyAgent
from oracle.agents.health_agent import HealthAgent
from oracle.agents.citizen_agent import CitizenAgent
from oracle.agents.ethics_agent import EthicsAgent
from oracle.agents.judge_agent import JudgeAgent
from oracle.state.state import State

__all__ = ["build_graph"]


# Initialize agents
climate_agent = ClimateAgent()
economy_agent = EconomyAgent()
health_agent = HealthAgent()
citizen_agent = CitizenAgent()
ethics_agent = EthicsAgent()
judge_agent = JudgeAgent()


def climate_node(state: State) -> dict[str, Any]:
    """Run climate agent analysis."""
    response = climate_agent.run(state)
    return {"climate_analysis": response.get("climate_analysis")}


def economy_node(state: State) -> dict[str, Any]:
    """Run economy agent analysis."""
    response = economy_agent.run(state)
    return {"economy_analysis": response.get("economy_analysis")}


def health_node(state: State) -> dict[str, Any]:
    """Run health agent analysis."""
    response = health_agent.run(state)
    return {"health_analysis": response.get("health_analysis")}


def citizen_node(state: State) -> dict[str, Any]:
    """Run citizen perspective analysis."""
    response = citizen_agent.run(state)
    return {"citizen_perspective": response.get("citizen_perspective")}


def ethics_node(state: State) -> dict[str, Any]:
    """Run ethics evaluation analysis."""
    response = ethics_agent.run(state)
    return {"ethics_evaluation": response.get("ethics_evaluation")}


def judge_node(state: State) -> dict[str, Any]:
    """Run judge agent to synthesize all perspectives."""
    response = judge_agent.run(state)
    return {
        "final_decision": response.get("final_decision"),
        "decision_reasoning": response.get("decision_reasoning"),
        "final_confidence": response.get("final_confidence"),
        "judge_response": response.get("response")
    }


def build_graph() -> StateGraph:
    """Create a LangGraph with all agent nodes and judge synthesis.
    
    Workflow:
    1. Run all domain agents in parallel
    2. Collect their perspectives
    3. Judge agent synthesizes into final decision
    """
    graph = StateGraph(State)
    
    # Add all agent nodes
    graph.add_node("climate", climate_node)
    graph.add_node("economy", economy_node)
    graph.add_node("health", health_node)
    graph.add_node("citizen", citizen_node)
    graph.add_node("ethics", ethics_node)
    graph.add_node("judge", judge_node)
    
    # Set entry point to run all domain agents first
    graph.set_entry_point("climate")
    
    # Connect climate to other agents (parallel execution conceptually)
    graph.add_edge("climate", "economy")
    graph.add_edge("climate", "health")
    graph.add_edge("climate", "citizen")
    graph.add_edge("climate", "ethics")
    
    # All domain agents lead to judge
    graph.add_edge("economy", "judge")
    graph.add_edge("health", "judge")
    graph.add_edge("citizen", "judge")
    graph.add_edge("ethics", "judge")
    
    # Judge is the final node
    graph.add_edge("judge", END)
    
    return graph.compile()



