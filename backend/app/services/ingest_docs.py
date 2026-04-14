import os, json
from app.services.mws_gateway import call_mws
from app.services.utils import extract_text_from_file
import requests
import time

CHROMA_URL = os.getenv("CHROMA_URL", "http://localhost:8000")

def ingest_document(file_path: str, metadata: dict):
    """
    1) извлекает текст
    2) получает эмбеддинги через MWS (endpoint /embed или /generate with model qwen3-embedding-8b)
    3) отправляет в Chroma (HTTP API)
    """
    text = extract_text_from_file(file_path)
    if not text:
        return {"status":"empty"}
    # get embedding via MWS (assumes MWS supports /embed or /generate returning embedding)
    try:
        emb_resp = call_mws(prompt=text[:2000], model="qwen3-embedding-8b", meta={"action":"embed"})
        embedding = emb_resp.get("meta", {}).get("embedding")
        # if MWS returns embedding in output, adapt accordingly
        if not embedding:
            # fallback: call /embed endpoint if available
            r = requests.post(f"{os.getenv('MWS_GPT_URL')}/embed", json={"input": text[:2000]})
            if r.status_code == 200:
                embedding = r.json().get("embedding")
    except Exception as e:
        print("Embedding error:", e)
        embedding = None

    # push to Chroma via REST API (simple example)
    try:
        payload = {
            "collection_name": "documents",
            "documents": [text[:2000]],
            "metadatas": [metadata],
            "ids": [os.path.basename(file_path)]
        }
        r = requests.post(f"{CHROMA_URL}/collections/documents/insert", json=payload, timeout=10)
        if r.status_code not in (200,201):
            print("Chroma insert status:", r.status_code, r.text)
    except Exception as e:
        print("Chroma error:", e)

    return {"status":"ok"}
