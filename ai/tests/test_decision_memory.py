import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from oracle.memory import DecisionMemory


class DecisionMemoryTests(unittest.TestCase):
    def test_stores_and_retrieves_related_decisions_in_same_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            memory = DecisionMemory(f"sqlite:///{Path(temporary_directory) / 'memory.sqlite3'}")
            memory.initialize()
            memory.store(
                memory_scope="neighborhood-a",
                problem_description="Should we build a new community center in the neighborhood?",
                user_input="Consider environmental effects",
                final_decision="Approve with low-carbon construction conditions.",
                decision_reasoning="The social benefit is high and emissions can be mitigated.",
                final_confidence=0.82,
                analyses={"climate": "Use low-carbon materials."},
            )

            matches = memory.find_relevant(
                memory_scope="neighborhood-a",
                problem_description="Should the neighborhood build a community center?",
                user_input="",
            )

            self.assertEqual(len(matches), 1)
            self.assertIn("Approve", matches[0].final_decision)
            self.assertIn("Previous decision", memory.format_context(matches))

            other_scope_matches = memory.find_relevant(
                memory_scope="neighborhood-b",
                problem_description="Should the neighborhood build a community center?",
                user_input="",
            )
            self.assertEqual(other_scope_matches, [])


if __name__ == "__main__":
    unittest.main()
