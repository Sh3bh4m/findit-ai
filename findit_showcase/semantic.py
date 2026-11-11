"""Synthetic vector search with fresh-record validation and access scoping.

This accepts supplied numeric vectors. It does not reproduce the private
EmbeddingGemma runtime or contain real customer text.
"""

from dataclasses import dataclass
import hashlib
import math
from typing import Mapping, Sequence


def content_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or len(left) != len(right):
        raise ValueError("Vector dimensions must be nonempty and equal")
    if not all(math.isfinite(float(v)) for v in (*left, *right)):
        raise ValueError("Vectors must contain finite numbers")
    norm = math.sqrt(sum(v * v for v in left)) * math.sqrt(sum(v * v for v in right))
    if norm == 0:
        raise ValueError("Zero-norm vectors are invalid")
    return sum(x * y for x, y in zip(left, right)) / norm


@dataclass(frozen=True)
class CurrentRecord:
    record_id: str
    collection: str
    owner_id: str
    text: str


@dataclass(frozen=True)
class IndexedRecord:
    record_id: str
    collection: str
    owner_id: str
    text_hash: str
    vector: tuple[float, ...]


@dataclass(frozen=True)
class SearchHit:
    record_id: str
    text: str
    score: float


class SemanticIndex:
    """Rank read-only candidate vectors; reject stale or out-of-scope records."""

    def __init__(self, entries: Sequence[IndexedRecord]):
        self.entries = tuple(entries)

    def search(
        self,
        query_vector: Sequence[float],
        *,
        authenticated_owner: str,
        allowed_collection: str,
        current_records: Mapping[str, CurrentRecord],
        top_k: int = 5,
        minimum_score: float = 0.0,
    ) -> list[SearchHit]:
        if not authenticated_owner or not allowed_collection:
            raise ValueError("Authenticated owner and collection are required")
        if not isinstance(top_k, int) or not 1 <= top_k <= 50:
            raise ValueError("top_k outside supported range")
        hits = []
        for entry in self.entries:
            if entry.owner_id != authenticated_owner or entry.collection != allowed_collection:
                continue
            current = current_records.get(entry.record_id)
            if current is None or current.owner_id != authenticated_owner:
                continue
            if current.collection != allowed_collection or content_sha256(current.text) != entry.text_hash:
                continue
            score = cosine_similarity(query_vector, entry.vector)
            if score >= minimum_score:
                hits.append(SearchHit(current.record_id, current.text, score))
        return sorted(hits, key=lambda hit: (-hit.score, hit.record_id))[:top_k]

