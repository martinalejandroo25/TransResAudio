# Endpoint /api/recordings
# 1. Guarda archivo
# 2. Extrae metadatos
# 3. Aplica VAD y STT
# 4. Asigna speakers
# 5. Guarda en DB
# 6. Genera resumen si esta habilitado
# app/main.py
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Recording, Segment, Summary
from utils.audio import read_wav_meta
from services.stt import transcribe
from services.diarization import vad_segments, diarize
from services.summary import summarize_md
import soundfile as sf
import numpy as np

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://plaud:plaudpass@db:3306/plaud")
DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/recordings")
async def upload_recording(file: UploadFile = File(...), language: str = Form("es"), speakers: int | None = Form(None)):
    # 1) Guardar archivo
    dest = os.path.join(DATA_DIR, file.filename)
    with open(dest, "wb") as f:
        f.write(await file.read())

    # 2) Metadatos
    sr, dur = read_wav_meta(dest)
    db = SessionLocal()
    rec = Recording(filename=file.filename, duration_sec=dur, sample_rate=sr)
    db.add(rec)
    db.commit()
    db.refresh(rec)

    # 3) Cargar audio para VAD
    pcm, sr2 = sf.read(dest, dtype='int16')
    if pcm.ndim > 1:
        pcm = pcm.mean(axis=1).astype(np.int16)
    seg_vad = vad_segments(pcm, sr2)

    # 4) STT (segmentos enteros de whisper para MVP)
    stt_segments = transcribe(dest, language=language)

    # 5) Diarización simple: asigna speakers a ventanas detectadas
    diar = diarize(speakers or 0, seg_vad)

    # 6) Fusionar texto + speaker por solapamiento simple
    def assign_speaker(t0, t1):
        best = "S1"
        best_overlap = 0.0
        for d in diar:
            a0, a1 = d["t0"], d["t1"]
            ov = max(0.0, min(t1, a1) - max(t0, a0))
            if ov > best_overlap:
                best_overlap = ov
                best = d["speaker"]
        return best

    merged = []
    for s in stt_segments:
        spk = assign_speaker(s["t0"], s["t1"])
        merged.append({"t0": s["t0"], "t1": s["t1"], "speaker": spk, "text": s["text"]})

    # 7) Persistencia
    for m in merged:
        db.add(Segment(recording_id=rec.id, t0=m['t0'], t1=m['t1'], speaker=m['speaker'], text=m['text']))
    db.commit()

    # 8) Resumen (opcional)
    summary_md = summarize_md(merged)
    if summary_md:
        db.add(Summary(recording_id=rec.id, bullets_md=summary_md))
        db.commit()

    # 9) Respuesta
    return {
        "id": rec.id,
        "filename": rec.filename,
        "duration_sec": rec.duration_sec,
        "sample_rate": rec.sample_rate,
        "segments": merged,
        "summary_md": summary_md or None
    }