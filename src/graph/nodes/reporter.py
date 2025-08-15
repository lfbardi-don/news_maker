from tts.adapter import TTSAdapter
from ..state import GraphState, Role, next_step

def reporter(state: GraphState) -> dict:
    if state.current_line.role != Role.reporter:
        return state

    text = (state.current_line.line or "").strip()
    if text:
        tts = TTSAdapter(voice="verse")
        tts.stream_play(
            text,
            on_start=lambda t: print(f"\nREPORTER: {t}\n", flush=True),
            on_chunk=lambda _: (print("·", end="", flush=True)),
            on_end=lambda: print()
        )

    return next_step(state)