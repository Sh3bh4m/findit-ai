import unittest
from findit_showcase.semantic import (
    CurrentRecord, IndexedRecord, SemanticIndex, cosine_similarity, content_sha256
)


def indexed(record, vector):
    return IndexedRecord(record.record_id, record.collection, record.owner_id,
                         content_sha256(record.text), vector)


class SemanticTests(unittest.TestCase):
    def setUp(self):
        self.a = CurrentRecord("a", "notes", "alice", "Delayed review")
        self.b = CurrentRecord("b", "notes", "alice", "Meeting setup")
        self.other = CurrentRecord("c", "notes", "bob", "Private record")
        self.index = SemanticIndex([indexed(self.a, (1., 0.)),
                                    indexed(self.b, (0., 1.)),
                                    indexed(self.other, (1., 0.))])
        self.current = {v.record_id: v for v in (self.a, self.b, self.other)}

    def search(self, current=None):
        return self.index.search((1., 0.), authenticated_owner="alice",
                                 allowed_collection="notes",
                                 current_records=current if current is not None else self.current)

    def test_ranking(self):
        self.assertEqual(self.search()[0].record_id, "a")
        self.assertAlmostEqual(cosine_similarity((1, 0), (1, 0)), 1.)

    def test_owner_isolation(self):
        self.assertNotIn("c", [h.record_id for h in self.search()])

    def test_stale_record_excluded(self):
        updated = dict(self.current)
        updated["a"] = CurrentRecord("a", "notes", "alice", "Changed text")
        self.assertNotIn("a", [h.record_id for h in self.search(updated)])

    def test_missing_source_excluded(self):
        updated = dict(self.current)
        updated.pop("a")
        self.assertNotIn("a", [h.record_id for h in self.search(updated)])

    def test_zero_vector_rejected(self):
        with self.assertRaises(ValueError):
            cosine_similarity((0., 0.), (1., 0.))
