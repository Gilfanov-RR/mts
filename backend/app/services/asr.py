import subprocess, os, tempfile
from app.services.mws_gateway import call_mws

WHISPER_MODEL = "whisper-turbo-local"

def transcribe_audio(file_bytes: bytes) -> str:
    # Простой путь: отправляем файл в MWS, где развернут whisper
    prompt = "<transcribe audio>"
    # MWS может принимать multipart; здесь упрощённо:
    resp = call_mws(prompt=prompt, model=WHISPER_MODEL, meta={"audio_bytes_len": len(file_bytes)})
    return resp["text"]
