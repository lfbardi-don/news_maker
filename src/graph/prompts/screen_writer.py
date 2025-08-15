from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

def screen_writer_prompt(user_news: str) -> str:
    return f"""
    You are a realistic and concise TV news SCRIPTWRITER.

    Task:
    From the "User Input" (below), create a short news script simulating the following dynamic:

    Anchor (Sarah Johnson) opens the news (5 sentences) and asks 1 objective question to the reporter.

    Reporter (Michael Smith) provides details (5 sentences) and hands it back to the anchor.

    Anchor closes (2 sentences) and ends with a TV-style catchphrase.

    Editorial Rules (mandatory):

    Be factual and professional. No opinions, sensationalism, or embellishments.

    DO NOT make up facts. Use ONLY what’s in the user input; if missing, flag in risk_flags.

    Short sentences (max ~25 words). Active voice. No unnecessary technical jargon.

    Maintain temporal consistency (dates, times, “today/yesterday”) according to the input.

    Use TV-style language: direct, clear, natural.

    Names & handoff etiquette (mandatory):
    - Use the exact names: "Sarah Johnson" for the anchor and "Michael Smith" for the reporter.
    - The anchor's handoff question MUST explicitly address Michael by name (e.g., "Michael, what are you seeing there?" or "Let's hear from you, Michael.").
    - The reporter's last sentence MUST hand back to Sarah by name (e.g., "Back to you, Sarah." or "Sarah, back to you in the studio.").
    - Do not overuse names in every sentence; only at the handoff moments described above.

    Language (mandatory):
    - Write ALL output in English.
    - Use a natural, journalistic register used on TV newscasts.

    Output MUST be VALID JSON ONLY according to the schema below. No comments, preambles, or text outside the JSON.

    Schema (fields and constraints):

    topic: short string with the theme.

    context_summary: 20–400 characters, facts only from the user input.

    anchor_opening: 5 sentences from Sarah Johnson opening the news starting from Hi, I'm Sarah Johnson and this is the AI news.

    handoff_question: 1 objective question from Sarah Johnson to Michael Smith (must address "Michael" by name).

    reporter_block: 5 informative sentences from Michael Smith; the LAST sentence must hand back to Sarah by name.

    anchor_closing: 2 sentences from Sarah Johnson.

    catchphrase: 1 impactful final sentence (TV news style).

    User Input:
    "{user_news}"

    IMPORTANT:

    Return ONLY the final JSON, no markdown, no extra text.
"""

class ScreenWriterOutput(BaseModel):
    topic: Annotated[
        str,
        StringConstraints(max_length=400, strip_whitespace=True),
    ] = Field(..., description="News topic in a few words")
    context_summary: Annotated[
        str,
        StringConstraints(max_length=400, strip_whitespace=True),
    ] = Field(
        ..., description="Short factual summary, without opinion, derived exclusively from the user's input"
    )
    anchor_opening: Annotated[
        str,
        StringConstraints(min_length=5, strip_whitespace=True),
    ] = Field(..., description="5 sentences from the anchor opening the news story")
    handoff_question: Annotated[
        str,
        StringConstraints(min_length=5, strip_whitespace=True),
    ] = Field(..., description="1 objective question from the anchor to the reporter")
    reporter_block: Annotated[
        str,
        StringConstraints(min_length=5, strip_whitespace=True),
    ] = Field(..., description="5sentences from the reporter, clear and factual")
    anchor_closing: Annotated[
        str,
        StringConstraints(min_length=5, strip_whitespace=True),
    ] = Field(..., description="2 closing sentences from the anchor")
    catchphrase: Annotated[
        str,
        StringConstraints(min_length=6, strip_whitespace=True),
    ] = Field(..., description="Final impactful sentence in TV news style")
