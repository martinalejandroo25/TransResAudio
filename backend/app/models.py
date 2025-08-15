# Define las tablas SQLAlchemy: Recording, Segment, Summary
#           Recording: info de la grabacion
#           Segment: fragmento con tiempo, hablante y texto
#           summary: resumen en formato Markdown
# app/models.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text, Float, func

class Base(DeclarativeBase):
    pass

class Recording(Base):
    __tablename__ = "recordings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    duration_sec: Mapped[float] = mapped_column(Float)
    sample_rate: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    segments: Mapped[list[Segment]] = relationship(back_populates="recording")
    summary: Mapped["Summary" | None] = relationship(back_populates="recording", uselist=False)

class Segment(Base):
    __tablename__ = "segments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recording_id: Mapped[int] = mapped_column(ForeignKey("recordings.id"))
    t0: Mapped[float] = mapped_column(Float)
    t1: Mapped[float] = mapped_column(Float)
    speaker: Mapped[str] = mapped_column(String(32))
    text: Mapped[str] = mapped_column(Text)

    recording: Mapped[Recording] = relationship(back_populates="segments")

class Summary(Base):
    __tablename__ = "summaries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recording_id: Mapped[int] = mapped_column(ForeignKey("recordings.id"))
    bullets_md: Mapped[str] = mapped_column(Text)

    recording: Mapped[Recording] = relationship(back_populates="summary")