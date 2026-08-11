import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from oracle.graph.graph import build_graph
from oracle.state.state import AgentResponse, State


class GraphTests(unittest.TestCase):
    def test_graph_returns_all_analyses_and_judgment(self) -> None:
        agent_responses = {
            "climate": ("climate_analysis", "Climate analysis"),
            "economy": ("economy_analysis", "Economy analysis"),
            "health": ("health_analysis", "Health analysis"),
            "citizen": ("citizen_perspective", "Citizen analysis"),
            "ethics": ("ethics_evaluation", "Ethics analysis"),
        }

        def agent_result(agent_name, field_name, analysis):
            return {
                "agent": agent_name,
                "response": analysis,
                field_name: AgentResponse(
                    agent_name=agent_name,
                    analysis=analysis,
                    confidence=0.8,
                ),
            }

        patches = []
        for agent_name, (field_name, analysis) in agent_responses.items():
            patches.append(patch(
                f"oracle.graph.graph.{agent_name}_agent.run",
                return_value=agent_result(agent_name, field_name, analysis),
            ))

        with patches[0], patches[1], patches[2], patches[3], patches[4], patch(
            "oracle.graph.graph.judge_agent.run",
            return_value={
                "final_decision": "Approve with conditions",
                "decision_reasoning": "Benefits outweigh manageable risks.",
                "final_confidence": 0.82,
                "response": "Synthetic judgment",
            },
        ):
            result = build_graph().invoke(State(user_input="Assess climate impact"))

        self.assertEqual(result["final_decision"], "Approve with conditions")
        self.assertEqual(result["final_confidence"], 0.82)
        self.assertEqual(result["climate_analysis"].analysis, "Climate analysis")
        self.assertEqual(result["ethics_evaluation"].analysis, "Ethics analysis")


if __name__ == "__main__":
    unittest.main()
