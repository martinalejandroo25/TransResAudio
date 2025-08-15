# app/schemas.py
from pydantic import BaseModel
from typing import List

class SegmentOut(BaseModel):
    t0: float
    t1: float
    speaker: str
    text: str

class RecordingOut(BaseModel):
    id: int
    filename: str
    duration_sec: float
    sample_rate: int
    segments: List[SegmentOut]
    summary_md: str | None = None