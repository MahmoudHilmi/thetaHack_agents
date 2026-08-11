import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from oracle.agents.climate_agent import ClimateAgent
from oracle.state.state import State


class ClimateAgentTests(unittest.TestCase):
    def test_run_returns_structured_response_from_state(self) -> None:
        state = State(user_input="Assess climate impact")
        agent = ClimateAgent()
        agent.model = Mock()
        agent.model.invoke.return_value = Mock(content="Reduce emissions and monitor air quality.")

        response = agent.run(state)

        self.assertEqual(response["agent"], "climate")
        self.assertEqual(response["response"], "Reduce emissions and monitor air quality.")
        self.assertEqual(
            response["climate_analysis"].analysis,
            "Reduce emissions and monitor air quality.",
        )
        agent.model.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()
