from typing import Callable, Optional
from openai import OpenAI
import numpy as np
import sounddevice as sd

class TTSAdapter:
    def __init__(self, sample_rate: int = 24000, model: str = "gpt-4o-mini-tts", voice: str = "alloy") -> None:
        self.sample_rate = sample_rate
        self.model = model
        self.voice = voice
        try:
            self.client: Optional[OpenAI] = OpenAI()
        except Exception:
            self.client = None

    def stream_play(
        self, text: str,
        on_start: Optional[Callable[[str], None]] = None,
        on_chunk: Optional[Callable[[int], None]] = None,
        on_end: Optional[Callable[[], None]] = None,
    ) -> None:
        """Stream TTS from OpenAI and play incrementally as PCM int16."""
        if not self.client or not text.strip():
            return

        if on_start:
            on_start(text)

        try:
            with self.client.audio.speech.with_streaming_response.create(
                model=self.model,
                voice=self.voice,
                input=text.strip(),
                response_format="pcm",
            ) as response:
                iterator = getattr(response, "iter_bytes", None)
                if callable(iterator):
                    pending = b""
                    written = 0
                    with sd.OutputStream(samplerate=self.sample_rate, channels=1, dtype="int16") as stream:
                        for chunk in response.iter_bytes():
                            if not chunk:
                                continue
                            pending += chunk
                            usable_len = len(pending) - (len(pending) % 2)
                            if usable_len <= 0:
                                continue
                            stream.write(np.frombuffer(pending[:usable_len], dtype=np.int16))
                            written += usable_len
                            if on_chunk:
                                on_chunk(written)
                            pending = pending[usable_len:]
                else:
                    audio = response.read()
                    usable_len = len(audio) - (len(audio) % 2)
                    if usable_len > 0:
                        with sd.OutputStream(samplerate=self.sample_rate, channels=1, dtype="int16") as stream:
                            stream.write(np.frombuffer(audio[:usable_len], dtype=np.int16))

        except Exception as e:
            print("Error streaming TTS")
            print(e)
            return
        
        finally:
            if on_end:
                on_end()