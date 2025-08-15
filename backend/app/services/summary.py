# Si ollama esta activo, genera un resumen con Llama 3
# Construye un prompt a partir de los segmentos transcritos
# app/services/summary.py
import requests
import textwrap

OLLAMA = "http://ollama:11434"
MODEL = "llama3:instruct"  # `docker compose --profile ollama up` y luego `ollama pull llama3:instruct`

def summarize_md(segments: list[dict]) -> str:
    # Construye prompt compacto con turnos por hablante
    transcript = "\n".join(
        f"[{s['t0']:.1f}-{s['t1']:.1f}] {s.get('speaker','S?')}: {s['text']}" for s in segments
    )
    prompt = textwrap.dedent(f"""
    Resume en viñetas concisas esta transcripción por puntos clave.
    Separa: *Decisiones*, *Tareas*, *Dudas*. Mantén etiquetas de hablante.

    Texto:
    {transcript}
    """)
    try:
        r = requests.post(f"{OLLAMA}/api/generate", json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=120)
        r.raise_for_status()
        return r.json().get("response", "")
    except Exception:
        return ""