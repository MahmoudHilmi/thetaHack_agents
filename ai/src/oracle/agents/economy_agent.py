"""Economy Agent for analyzing economic impact."""

from typing import Any
from langchain_core.prompts import PromptTemplate
from oracle.config import get_chat_model, settings
from oracle.state.state import State, AgentResponse
from oracle.prompts.loader import ECONOMY_PROMPT


class EconomyAgent:
    """Analyzes economic impact of decisions."""

    def __init__(self) -> None:
        self.name = "economy"
        self.model = get_chat_model(
            model="gpt-4-turbo",
            temperature=0.7
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["problem"],
            template=ECONOMY_PROMPT
        )

    def run(self, state: State) -> dict[str, Any]:
        """Return economic impact analysis."""
        problem = state.analysis_prompt
        
        if not self.model:
            return {
                "agent": self.name,
                "response": "Economy Agent: API key not configured",
                "economy_analysis": AgentResponse(
                    agent_name="Economy Agent",
                    analysis="API key not configured",
                    confidence=0.0
                )
            }
        
        try:
            prompt = self.prompt_template.format(problem=problem)
            response = self.model.invoke(prompt).content
            
            analysis = AgentResponse(
                agent_name="Economy Agent",
                analysis=response.strip(),
                confidence=0.82,
                reasoning="Analysis based on economic impact assessment"
            )
            
            return {
                "agent": self.name,
                "response": response.strip(),
                "economy_analysis": analysis
            }
        except Exception as e:
            return {
                "agent": self.name,
                "response": f"Error in economic analysis: {str(e)}",
                "economy_analysis": AgentResponse(
                    agent_name="Economy Agent",
                    analysis=f"Error: {str(e)}",
                    confidence=0.0
                )
            }

