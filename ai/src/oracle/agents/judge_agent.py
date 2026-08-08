"""Judge Agent for synthesizing all agent perspectives into final decision."""

from typing import Any, List
from langchain_core.prompts import PromptTemplate
from oracle.config import get_chat_model, settings
from oracle.state.state import State, AgentResponse
from oracle.prompts.loader import JUDGE_PROMPT


class JudgeAgent:
    """Synthesizes perspectives from all agents into final balanced decision."""

    def __init__(self) -> None:
        self.name = "judge"
        self.model = get_chat_model(
            model="gpt-4-turbo",
            temperature=0.5  # Lower temperature for balanced judgment
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["problem", "perspectives"],
            template=JUDGE_PROMPT
        )

    def run(self, state: State) -> dict[str, Any]:
        """Synthesize all perspectives into final decision."""
        if not self.model:
            return {
                "agent": self.name,
                "response": "Judge Agent: API key not configured",
                "final_decision": "Unable to make decision - API key not configured",
                "final_confidence": 0.0
            }
        
        # Format all perspectives
        perspectives = self._format_perspectives(state)
        problem = state.problem_description or state.user_input or "No problem specified"
        
        try:
            prompt = self.prompt_template.format(
                problem=problem,
                perspectives=perspectives
            )
            response = self.model.invoke(prompt).content
            
            # Parse response
            decision, reasoning, confidence = self._parse_response(response)
            
            return {
                "agent": self.name,
                "response": response.strip(),
                "final_decision": decision,
                "decision_reasoning": reasoning,
                "final_confidence": confidence
            }
        except Exception as e:
            return {
                "agent": self.name,
                "response": f"Error in judge decision: {str(e)}",
                "final_decision": f"Error: {str(e)}",
                "final_confidence": 0.0
            }
    
    def _format_perspectives(self, state: State) -> str:
        """Format all agent responses for judge consideration."""
        perspectives = []
        
        if state.climate_analysis:
            perspectives.append(f"🌍 CLIMATE: {state.climate_analysis.analysis}\n")
        if state.economy_analysis:
            perspectives.append(f"💰 ECONOMY: {state.economy_analysis.analysis}\n")
        if state.health_analysis:
            perspectives.append(f"❤️ HEALTH: {state.health_analysis.analysis}\n")
        if state.citizen_perspective:
            perspectives.append(f"👥 CITIZEN: {state.citizen_perspective.analysis}\n")
        if state.ethics_evaluation:
            perspectives.append(f"⚖️ ETHICS: {state.ethics_evaluation.analysis}\n")
        
        return "\n".join(perspectives) if perspectives else "No perspectives provided"
    
    def _parse_response(self, response: str) -> tuple:
        """Parse judge response to extract decision, reasoning, and confidence."""
        try:
            lines = response.split("\n")
            decision = ""
            reasoning = ""
            confidence = 0.5
            
            for line in lines:
                if line.startswith("RECOMMENDATION:"):
                    decision = line.replace("RECOMMENDATION:", "").strip()
                elif line.startswith("REASONING:"):
                    reasoning = line.replace("REASONING:", "").strip()
                elif line.startswith("CONFIDENCE:"):
                    try:
                        confidence = float(line.replace("CONFIDENCE:", "").strip())
                    except:
                        confidence = 0.5
            
            return decision or response[:100], reasoning or response, min(max(confidence, 0), 1)
        except:
            return response[:100], response, 0.5
