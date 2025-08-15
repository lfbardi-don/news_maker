from typing import Literal

from langgraph.graph import END
from ..state import GraphState, Role


def manager(state: GraphState) -> dict:
    """Manager node performs no state updates directly."""
    return {}


def route(state: GraphState) -> Literal["screen_writer", "anchor", "reporter", END]:
    if not state.topic:
        return END

    if not state.news_script:
        return "screen_writer"

    if state.cursor >= len(state.news_script):
        return END

    next_line = state.news_script[state.cursor]
    if next_line.role == Role.anchor:
        return "anchor"
    if next_line.role == Role.reporter:
        return "reporter"
    return "screen_writer"


