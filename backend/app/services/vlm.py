from app.services.mws_gateway import call_mws

VLM_MODEL = "qwen3-vl-30b-a3b-instruct"

def analyze_image(image_bytes: bytes, question: str = None):
    # Отправляем изображение в MWS GPT с указанием VLM модели
    prompt = "Analyze image and answer the question: " + (question or "Describe the image.")
    resp = call_mws(prompt=prompt, model=VLM_MODEL, meta={"has_image": True})
    return resp
