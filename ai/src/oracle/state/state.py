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
    memory_context: str = ""
    response_language: str = ""

    @property
    def analysis_prompt(self) -> str:
        """Return the problem enriched with relevant historical decisions."""
        problem = self.problem_description or self.user_input or "No input provided"
        return f"{problem}\n\n{self.memory_context}" if self.memory_context else problem

    @property
    def language_instruction(self) -> str:
        """Return a language directive for model prompts."""
        if self.response_language:
            return (
                f"Respond in {self.response_language}. "
                "Use the same language for all answers and explanations."
            )
        return (
            "Respond in the same language as the problem description. "
            "If the problem is in Arabic, answer in Arabic; if it is in English, answer in English."
        )
    
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
