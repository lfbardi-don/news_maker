from ..state import GraphState, Line, Step, Role
from ..prompts.screen_writer import ScreenWriterOutput, screen_writer_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def screen_writer(state: GraphState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured = llm.with_structured_output(ScreenWriterOutput)
    output: ScreenWriterOutput = structured.invoke(screen_writer_prompt(state.topic))

    script: list[Line] = []

    for step in Step:
        match step:
            case Step.anchor_opening:
                script.append(Line(step=step, role=Role.anchor, line=output.anchor_opening))
            case Step.handoff_question:
                script.append(Line(step=step, role=Role.anchor, line=output.handoff_question))
            case Step.reporter_block:
                script.append(Line(step=step, role=Role.reporter, line=output.reporter_block))
            case Step.anchor_closing:
                script.append(Line(step=step, role=Role.anchor, line=output.anchor_closing))
            case Step.catchphrase:
                script.append(Line(step=step, role=Role.anchor, line=output.catchphrase))
    
    return { "news_script": script, "cursor": 0, "current_line": script[0] }
