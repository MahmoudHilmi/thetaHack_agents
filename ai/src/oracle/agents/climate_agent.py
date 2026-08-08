"""Climate Agent for analyzing climate and environmental impact."""

from typing import Any
from langchain_core.prompts import PromptTemplate
from oracle.config import get_chat_model, settings
from oracle.state.state import State, AgentResponse
from oracle.prompts.loader import CLIMATE_PROMPT


class ClimateAgent:
    """Climate-focused agent that analyzes environmental impact."""

    def __init__(self) -> None:
        self.name = "climate"
        self.model = get_chat_model(
            model="gpt-4-turbo",
            temperature=0.7
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["problem"],
            template=CLIMATE_PROMPT
        )

    def run(self, state: State) -> dict[str, Any]:
        """Return a structured climate analysis response from the given state."""
        problem = state.problem_description or state.user_input or "No input provided"
        
        if not self.model:
            return {
                "agent": self.name,
                "response": "Climate Agent: API key not configured",
                "climate_analysis": AgentResponse(
                    agent_name="Climate Agent",
                    analysis="API key not configured",
                    confidence=0.0
                )
            }
        
        try:
            prompt = self.prompt_template.format(problem=problem)
            response = self.model.invoke(prompt).content
            
            analysis = AgentResponse(
                agent_name="Climate Agent",
                analysis=response.strip(),
                confidence=0.85,
                reasoning="Analysis based on climate impact assessment"
            )
            
            return {
                "agent": self.name,
                "response": response.strip(),
                "climate_analysis": analysis
            }
        except Exception as e:
            return {
                "agent": self.name,
                "response": f"Error in climate analysis: {str(e)}",
                "climate_analysis": AgentResponse(
                    agent_name="Climate Agent",
                    analysis=f"Error: {str(e)}",
                    confidence=0.0
                )
            }



