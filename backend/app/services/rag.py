from chromadb import Client
from chromadb.config import Settings
import os

CHROMA_URL = os.getenv("CHROMA_URL", "http://chroma:8000")
# Пример: используем HTTP API клиента chromadb (псевдокод)
client = Client(Settings(chroma_api_impl="rest", chroma_server_host="chroma", chroma_server_http_port=8000))

def query_rag(query: str, top_k=5):
    # 1. получить эмбеддинг через модель эмбеддингов (через MWS)
    # 2. запросить Chroma
    # Здесь упрощённый интерфейс:
    collection = client.get_collection("documents")
    results = collection.query(query_texts=[query], n_results=top_k)
    # собрать контекст
    ctx = "\n".join([r["metadata"]["text"] for r in results["documents"][0]])
    return ctx
