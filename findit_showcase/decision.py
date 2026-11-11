"""Illustrative intent selector, not the private trained Laya model."""

from dataclasses import dataclass
from enum import Enum
import re


class Route(str, Enum):
    STRUCTURED = "structured"
    SEMANTIC = "semantic"
    GENERAL = "general"


@dataclass(frozen=True)
class Decision:
    route: Route
    rationale: str
    needs_clarification: bool = False


EXACT = re.compile(r"\b(how many|count|number of|total|list all|show all|show my|status of)\b", re.I)
MEANING = re.compile(r"\b(similar|related|discussion|discussions|mentioned|mentions|notes about|documents about|find information about)\b", re.I)


def route_question(question: str) -> Decision:
    """Select a reference route or ask for clarification on ambiguous intent."""
    if not question.strip():
        return Decision(Route.GENERAL, "Empty question", True)
    exact = bool(EXACT.search(question))
    meaning = bool(MEANING.search(question))
    if exact and meaning:
        return Decision(Route.GENERAL, "Overlapping exact and semantic intents", True)
    if exact:
        return Decision(Route.STRUCTURED, "Exact query or aggregation requested")
    if meaning:
        return Decision(Route.SEMANTIC, "Meaning-based document search requested")
    return Decision(Route.GENERAL, "No reliable retrieval intent recognized")
