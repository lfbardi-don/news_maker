from tts.adapter import TTSAdapter
from ..state import GraphState, Role, next_step

def anchor(state: GraphState) -> dict:
    if state.current_line.role != Role.anchor:
        return state

    text = (state.current_line.line or "").strip()
    if text:
        tts = TTSAdapter(voice="alloy")
        tts.stream_play(
            text,
            on_start=lambda t: print(f"\nANCHOR: {t}\n", flush=True),
            on_chunk=lambda _: (print("·", end="", flush=True)),
            on_end=lambda: print(),
        )
        
    return next_step(state)
