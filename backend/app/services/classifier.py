from typing import Optional
import re

# Простая rule-based классификация; можно заменить на ML модель
def classify_input(text: Optional[str], link: Optional[str]) -> dict:
    if link:
        return {"task": "web_parse", "recommended_model": "mws-gpt-alpha"}
    if text:
        t = text.lower()
        if re.search(r"(покажи|создай|сгенерируй|нарисуй|изображение|картинку)", t):
            return {"task": "image_gen", "recommended_model": "qwen-image"}
        if re.search(r"(аудио|запись|послушай|расшифруй)", t):
            return {"task": "asr", "recommended_model": "whisper-turbo-local"}
        if len(t.split()) < 6:
            return {"task": "short_answer", "recommended_model": "mws-gpt-alpha"}
        return {"task": "rag", "recommended_model": "qwen2.5-72b-instruct"}
    return {"task": "chat", "recommended_model": "mws-gpt-alpha"}
