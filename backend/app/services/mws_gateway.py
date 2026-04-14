import os, requests, time

MWS_URL = os.getenv("MWS_GPT_URL")
API_KEY = os.getenv("MWS_API_KEY")

def call_mws(prompt: str, model: str = "mws-gpt-alpha", meta: dict = None, timeout=60):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "input": prompt,
        "meta": meta or {}
    }
    start = time.time()
    r = requests.post(f"{MWS_URL}/generate", json=payload, headers=headers, timeout=timeout)
    latency = time.time() - start
    if r.status_code != 200:
        raise Exception(f"MWS error: {r.status_code} {r.text}")
    data = r.json()
    # meta info for transparency
    return {"text": data.get("output", ""), "meta": {"model": model, "latency": latency, "tool_calls": data.get("tool_calls", [])}}
