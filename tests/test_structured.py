import unittest
from findit_showcase.structured import TaskStore


class StructuredTests(unittest.TestCase):
    def setUp(self):
        self.store = TaskStore.synthetic()

    def tearDown(self):
        self.store.connection.close()

    def test_count(self):
        self.assertEqual(self.store.count_tasks("user-001", "open"), 2)

    def test_scoped_users(self):
        self.assertEqual(self.store.count_tasks("user-002", "open"), 1)
        self.assertEqual(len(self.store.list_tasks("user-001")), 3)

    def test_rejects_injection(self):
        with self.assertRaises(ValueError):
            self.store.count_tasks("user-001", "open' OR 1=1 --")

    def test_identity_required(self):
        with self.assertRaises(ValueError):
            self.store.count_tasks("")
