import unittest
from findit_showcase.decision import Route, route_question


class DecisionTests(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(route_question("How many open tasks?").route, Route.STRUCTURED)

    def test_semantic(self):
        self.assertEqual(route_question("Find discussions about approvals").route, Route.SEMANTIC)

    def test_general(self):
        self.assertEqual(route_question("Explain task dependencies").route, Route.GENERAL)

    def test_ambiguous(self):
        self.assertTrue(route_question("How many discussions about delays?").needs_clarification)

    def test_blank(self):
        self.assertTrue(route_question("   ").needs_clarification)
