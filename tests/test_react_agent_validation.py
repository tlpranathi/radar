import unittest

from agent.react_agent import run_agent


class TestReactAgentValidation(unittest.TestCase):

    def test_empty_goal(self):
        with self.assertRaises(ValueError):
            run_agent("")

    def test_whitespace_goal(self):
        with self.assertRaises(ValueError):
            run_agent("   ")

    def test_invalid_iteration_limit(self):
        with self.assertRaises(ValueError):
            run_agent("Find internships", max_iterations=0)

    def test_string_iteration_limit(self):
        with self.assertRaises(ValueError):
            run_agent("Find internships", max_iterations="five")

    def test_boolean_iteration_limit(self):
        with self.assertRaises(ValueError):
            run_agent("Find internships", max_iterations=True)


if __name__ == "__main__":
    unittest.main()