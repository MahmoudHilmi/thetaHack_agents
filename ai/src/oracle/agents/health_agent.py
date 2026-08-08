"""Health Agent for analyzing health impact."""

from typing import Any
from langchain_core.prompts import PromptTemplate
from oracle.config import get_chat_model, settings
from oracle.state.state import State, AgentResponse
from oracle.prompts.loader import HEALTH_PROMPT


class HealthAgent:
    """Analyzes health impact of decisions."""

    def __init__(self) -> None:
        self.name = "health"
        self.model = get_chat_model(
            model="gpt-4-turbo",
            temperature=0.7
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["problem"],
            template=HEALTH_PROMPT
        )

    def run(self, state: State) -> dict[str, Any]:
        """Return health impact analysis."""
        problem = state.problem_description or state.user_input or "No input provided"
        
        if not self.model:
            return {
                "agent": self.name,
                "response": "Health Agent: API key not configured",
                "health_analysis": AgentResponse(
                    agent_name="Health Agent",
                    analysis="API key not configured",
                    confidence=0.0
                )
            }
        
        try:
            prompt = self.prompt_template.format(problem=problem)
            response = self.model.invoke(prompt).content
            
            analysis = AgentResponse(
                agent_name="Health Agent",
                analysis=response.strip(),
                confidence=0.83,
                reasoning="Analysis based on health impact assessment"
            )
            
            return {
                "agent": self.name,
                "response": response.strip(),
                "health_analysis": analysis
            }
        except Exception as e:
            return {
                "agent": self.name,
                "response": f"Error in health analysis: {str(e)}",
                "health_analysis": AgentResponse(
                    agent_name="Health Agent",
                    analysis=f"Error: {str(e)}",
                    confidence=0.0
                )
            }
