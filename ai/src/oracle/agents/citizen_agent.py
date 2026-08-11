"""Citizen Agent for representing citizen perspective."""

from typing import Any
from langchain_core.prompts import PromptTemplate
from oracle.config import get_chat_model, settings
from oracle.state.state import State, AgentResponse
from oracle.prompts.loader import CITIZEN_PROMPT


class CitizenAgent:
    """Represents citizen perspective and public opinion."""

    def __init__(self) -> None:
        self.name = "citizen"
        self.model = get_chat_model(
            model="gpt-4-turbo",
            temperature=0.7
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["problem", "language_instruction"],
            template=CITIZEN_PROMPT
        )

    def run(self, state: State) -> dict[str, Any]:
        """Return citizen perspective analysis."""
        problem = state.analysis_prompt
        
        if not self.model:
            return {
                "agent": self.name,
                "response": "Citizen Agent: API key not configured",
                "citizen_perspective": AgentResponse(
                    agent_name="Citizen Agent",
                    analysis="API key not configured",
                    confidence=0.0
                )
            }
        
        try:
            prompt = self.prompt_template.format(
                problem=problem,
                language_instruction=state.language_instruction,
            )
            response = self.model.invoke(prompt).content
            
            analysis = AgentResponse(
                agent_name="Citizen Agent",
                analysis=response.strip(),
                confidence=0.80,
                reasoning="Analysis based on citizen perspective assessment"
            )
            
            return {
                "agent": self.name,
                "response": response.strip(),
                "citizen_perspective": analysis
            }
        except Exception as e:
            return {
                "agent": self.name,
                "response": f"Error in citizen perspective analysis: {str(e)}",
                "citizen_perspective": AgentResponse(
                    agent_name="Citizen Agent",
                    analysis=f"Error: {str(e)}",
                    confidence=0.0
                )
            }

