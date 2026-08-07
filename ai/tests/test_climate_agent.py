import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from oracle.agents.climate_agent import ClimateAgent
from oracle.state.state import State


class ClimateAgentTests(unittest.TestCase):
    def test_run_returns_structured_response_from_state(self) -> None:
        state = State(user_input="Assess climate impact")
        agent = ClimateAgent()

        response = agent.run(state)

        self.assertEqual(response["agent"], "climate")
        self.assertIn("Assess climate impact", response["response"])


if __name__ == "__main__":
    unittest.main()
