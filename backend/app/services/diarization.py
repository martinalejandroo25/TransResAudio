# Implementa detección de voz(VAD) con webrtcvad
# Usa clustering simulado para asignar speakers (placeholder para futuro pyannote)
# app/services/diarization.py
import webrtcvad
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# Simple VAD-based segmentation
def vad_segments(wav_pcm16: np.ndarray, sr: int, frame_ms=30):
    vad = webrtcvad.Vad(2)
    frame_len = int(sr * frame_ms / 1000)
    speech = []
    cur_on = None
    for i in range(0, len(wav_pcm16) - frame_len, frame_len):
        frame = wav_pcm16[i:i+frame_len].tobytes()
        if vad.is_speech(frame, sr):
            if cur_on is None:
                cur_on = i
        else:
            if cur_on is not None:
                speech.append((cur_on / sr, i / sr))
                cur_on = None
    if cur_on is not None:
        speech.append((cur_on / sr, len(wav_pcm16) / sr))
    return speech

# Finge embeddings (placeholder). Sustituye por ECAPA‑TDNN ONNX para mejor calidad

def fake_embeddings(n: int, dim: int = 64):
    rng = np.random.default_rng(0)
    return rng.normal(size=(n, dim)).astype(np.float32)


def diarize(num_speakers: int, segments: list[tuple[float,float]]):
    if not segments:
        return []
    X = fake_embeddings(len(segments))
    k = max(2, num_speakers) if num_speakers else 2
    labels = AgglomerativeClustering(n_clusters=k).fit_predict(X)
    diar = []
    for (t0, t1), lab in zip(segments, labels):
        diar.append({"t0": float(t0), "t1": float(t1), "speaker": f"S{lab+1}"})
    return diar