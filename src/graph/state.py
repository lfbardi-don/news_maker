from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Role(Enum):
    anchor = "anchor"
    reporter = "reporter"
    screen_writer = "screen_writer"

class Step(Enum):
    anchor_opening = "anchor_opening"
    handoff_question = "handoff_question"
    reporter_block = "reporter_block"
    anchor_closing = "anchor_closing"
    catchphrase = "catchphrase"

class Line(BaseModel):
    step: Step
    role: Role
    line: str 

class GraphState(BaseModel):
    cursor: int = 0
    current_line: Optional[Line] = None
    topic: str = ""
    context_summary: str = ""
    news_script: list[Line] = []

def next_step(state: GraphState) -> dict:
    new_cursor = state.cursor + 1
    new_current: Optional[Line] = (
        state.news_script[new_cursor] if new_cursor < len(state.news_script) else None
    )
    return {"cursor": new_cursor, "current_line": new_current}
    