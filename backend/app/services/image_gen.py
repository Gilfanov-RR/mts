from app.services.mws_gateway import call_mws

IMAGE_MODEL = "qwen-image"

def generate_image(prompt_text: str, style: str = "illustration"):
    prompt = f"Generate an image: {prompt_text} ; style: {style}"
    resp = call_mws(prompt=prompt, model=IMAGE_MODEL, meta={"image_request": True})
    # resp["meta"] может содержать ссылку/ID изображения, который frontend загрузит
    return resp
