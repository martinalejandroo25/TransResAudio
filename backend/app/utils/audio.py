# app/utils/audio.py
import wave

def read_wav_meta(path: str) -> tuple[int, float]:
    with wave.open(path, 'rb') as wf:
        sr = wf.getframerate()
        frames = wf.getnframes()
        dur = frames / float(sr)
        return sr, dur