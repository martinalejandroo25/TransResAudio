# TransResAudio

Sistema de transcripcion de audio, diarizacion de interlocutores y generacion de resumenes automaticos mediante modelos de lenguaje locales.

## Modulos

- `backend/`: Servicio API REST con FastAPI, Faster-Whisper para transcripcion y conexion con Ollama para generacion de resumenes.
- `android/`: Aplicacion cliente Android para grabacion y envio de notas de voz.

## Despliegue Backend

1. Configurar variables de entorno copiando `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Iniciar servicios mediante Docker Compose:
   ```bash
   cd backend/app && docker compose up -d
   ```
El servicio API estara accesible en el puerto 8000 y la documentacion interactiva en `/docs`.
