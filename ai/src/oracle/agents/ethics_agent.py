"""Ethics Agent for analyzing ethical implications."""

from typing import Any
from langchain_core.prompts import PromptTemplate
from oracle.config import get_chat_model, settings
from oracle.state.state import State, AgentResponse
from oracle.prompts.loader import ETHICS_PROMPT


class EthicsAgent:
    """Analyzes ethical and moral implications of decisions."""

    def __init__(self) -> None:
        self.name = "ethics"
        self.model = get_chat_model(
            model="gpt-4-turbo",
            temperature=0.7
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["problem", "language_instruction"],
            template=ETHICS_PROMPT
        )

    def run(self, state: State) -> dict[str, Any]:
        """Return ethics impact analysis."""
        problem = state.analysis_prompt
        
        if not self.model:
            return {
                "agent": self.name,
                "response": "Ethics Agent: API key not configured",
                "ethics_evaluation": AgentResponse(
                    agent_name="Ethics Agent",
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
                agent_name="Ethics Agent",
                analysis=response.strip(),
                confidence=0.84,
                reasoning="Analysis based on ethical evaluation framework"
            )
            
            return {
                "agent": self.name,
                "response": response.strip(),
                "ethics_evaluation": analysis
            }
        except Exception as e:
            return {
                "agent": self.name,
                "response": f"Error in ethics analysis: {str(e)}",
                "ethics_evaluation": AgentResponse(
                    agent_name="Ethics Agent",
                    analysis=f"Error: {str(e)}",
                    confidence=0.0
                )
            }
