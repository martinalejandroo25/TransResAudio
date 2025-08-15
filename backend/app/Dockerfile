# Imagen base CUDA + cuDNN -> necesario para acelerar faster-whisper con GPU
# Instala dependencias del sistema y Python
# Copia la app al contenedor y expone el puerto 8000
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 python3-pip ffmpeg build-essential git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/ /app/
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]