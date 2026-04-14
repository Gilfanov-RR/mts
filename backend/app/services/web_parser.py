import requests
from bs4 import BeautifulSoup
from app.services.rag import query_rag

async def parse_url(url: str):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    # простая очистка
    texts = [p.get_text() for p in soup.find_all("p")]
    full_text = "\n".join(texts)
    # краткое суммирование через MWS
    from app.services.mws_gateway import call_mws
    summary = call_mws(prompt=f"Summarize the following page:\n\n{full_text[:2000]}", model="mws-gpt-alpha")
    return {"text": full_text, "summary": summary["text"]}
