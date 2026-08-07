"""State models for ORACLE.

Define global state representations used by agents and the graph.
Pydantic-based for validation and forward-compatibility.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AgentResponse(BaseModel):
    """Response from a single agent."""
    agent_name: str
    analysis: str
    confidence: float = Field(ge=0, le=1)
    reasoning: Optional[str] = None


class State(BaseModel):
    """Complete runtime state for ORACLE multi-agent system."""
    
    # Input
    user_input: str = ""
    problem_description: str = ""
    
    # Agent responses
    climate_analysis: Optional[AgentResponse] = None
    economy_analysis: Optional[AgentResponse] = None
    health_analysis: Optional[AgentResponse] = None
    citizen_perspective: Optional[AgentResponse] = None
    ethics_evaluation: Optional[AgentResponse] = None
    
    # Judge decision
    judge_recommendation: Optional[str] = None
    final_decision: Optional[str] = None
    final_confidence: float = 0.0
    
    # Metadata
    all_agent_responses: List[AgentResponse] = Field(default_factory=list)
    decision_reasoning: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
