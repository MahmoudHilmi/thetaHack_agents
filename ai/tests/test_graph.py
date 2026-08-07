import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from oracle.graph.graph import build_graph
from oracle.state.state import State


class GraphTests(unittest.TestCase):
    def test_build_graph_creates_a_single_climate_entry_node(self) -> None:
        graph = build_graph().compile()
        result = graph.invoke(State(user_input="Assess climate impact"))

        self.assertEqual(result["last_agent_response"], "Climate analysis: Assess climate impact")


if __name__ == "__main__":
    unittest.main()
