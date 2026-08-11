import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from oracle.api.main import DecisionRequest, make_decision
from oracle.state.state import AgentResponse


class ApiTests(unittest.TestCase):
    def test_decide_returns_complete_response(self) -> None:
        analyses = {
            "climate_analysis": "Use clean power.",
            "economy_analysis": "Costs are manageable.",
            "health_analysis": "Air quality improves.",
            "citizen_perspective": "Support is likely.",
            "ethics_evaluation": "Benefits are fairly shared.",
        }

        def agent_result(field_name, text):
            return {
                field_name: AgentResponse(
                    agent_name=field_name,
                    analysis=text,
                    confidence=0.8,
                )
            }

        graph = Mock()
        graph.invoke.return_value = {
            **{
                field: AgentResponse(agent_name=field, analysis=text, confidence=0.8)
                for field, text in analyses.items()
            },
            "final_decision": "Approve with safeguards",
            "decision_reasoning": "The overall benefit is positive.",
            "final_confidence": 0.85,
        }

        with patch("oracle.api.main.settings.OPENAI_API_KEY", "test-key"), patch(
            "oracle.api.main.graph", graph
        ), patch("oracle.api.main.decision_memory.find_relevant", return_value=[]), patch(
            "oracle.api.main.decision_memory.store"
        ):
            response = asyncio.run(
                make_decision(DecisionRequest(problem_description="Should the city electrify its buses?"))
            )

        self.assertEqual(response.final_decision, "Approve with safeguards")
        self.assertEqual(response.final_confidence, 0.85)
        self.assertEqual(response.climate_analysis, "Use clean power.")
        self.assertEqual(response.status, "success")

    def test_decide_surfaces_provider_failure(self) -> None:
        graph = Mock()
        graph.invoke.return_value = {
            "final_decision": "Error: Error code: 429 - insufficient balance",
            "decision_reasoning": "Analysis pending",
            "final_confidence": 0.0,
        }

        with patch("oracle.api.main.settings.ZAI_API_KEY", "test-key"), patch(
            "oracle.api.main.graph", graph
        ), patch("oracle.api.main.decision_memory.find_relevant", return_value=[]):
            with self.assertRaises(HTTPException) as context:
                asyncio.run(
                    make_decision(DecisionRequest(problem_description="Test provider failure"))
                )

        self.assertEqual(context.exception.status_code, 502)


if __name__ == "__main__":
    unittest.main()
