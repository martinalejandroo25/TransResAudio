#Carga el modelo faster-whisper una sola vez
#transcribe(): convierte audio a texto con timestamps
# app/services/stt.py
from faster_whisper import WhisperModel

_model = None

def get_model():
    global _model
    if _model is None:
        # medium o large-v3 si tienes GPU
        _model = WhisperModel("medium", device="cuda", compute_type="float16")
    return _model


def transcribe(path: str, language: str = "es"):
    model = get_model()
    segments, info = model.transcribe(path, language=language, vad_filter=True)
    out = []
    for seg in segments:
        out.append({
            "t0": float(seg.start),
            "t1": float(seg.end),
            "text": seg.text.strip()
        })
    return out