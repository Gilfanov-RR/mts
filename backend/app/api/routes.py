from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import shutil, os
from pydantic import BaseModel
from app.api.schemas import ChatRequest, ChatResponse, UploadResponse, TranscribeResponse
from app.services.classifier import classify_input
from app.services.mws_gateway import call_mws
from app.services.rag import query_rag
from app.services.memory import get_relevant_memory, save_memory
from app.services.asr import transcribe_audio
from app.services.web_parser import parse_url
from app.services.utils import save_uploaded_file, extract_text_from_file
from app.services.ingest_docs import ingest_document

router = APIRouter()

@router.get("/health")
async def health():
    return {"status":"ok"}

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # 1. classify
    task_info = classify_input(req.text, req.link)
    task = task_info.get("task")
    recommended = task_info.get("recommended_model")
    # 2. gather memory/context
    memory_ctx = get_relevant_memory(req.user_id, req.text)
    # 3. route by task
    prompt_parts = []
    if memory_ctx:
        prompt_parts.append("UserProfile:\n" + memory_ctx)
    if task == "web_parse" and req.link:
        parsed = await parse_url(req.link)
        prompt_parts.append("WebPageSummary:\n" + parsed.get("summary",""))
        prompt_parts.append("WebPageText:\n" + parsed.get("text","")[:4000])
    elif task == "rag":
        rag_ctx = query_rag(req.text)
        prompt_parts.append("RetrievedDocuments:\n" + rag_ctx)
    if req.text:
        prompt_parts.append("UserQuestion:\n" + req.text)
    prompt = "\n\n".join(prompt_parts) if prompt_parts else (req.text or "")

    # 4. choose model
    model = req.model or recommended or "mws-gpt-alpha"
    # 5. call MWS
    try:
        resp = call_mws(prompt=prompt, model=model, meta={"task": task})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"answer": resp.get("text",""), "meta": resp.get("meta", {})}

@router.post("/upload", response_model=UploadResponse)
async def upload_file(user_id: str = Form(...), file: UploadFile = File(...)):
    # save file to disk
    saved_path = save_uploaded_file(file, subdir="uploads")
    # extract text
    text = extract_text_from_file(saved_path)
    # persist document record (optional)
    try:
        ingest_document(saved_path, {"user_id": user_id, "filename": file.filename})
    except Exception as e:
        # log but continue
        print("Ingest error:", e)
    # create quick summary via MWS
    try:
        summary_resp = call_mws(prompt=f"Summarize the following document:\n\n{text[:4000]}", model="mws-gpt-alpha")
        summary = summary_resp.get("text","")
    except Exception:
        summary = text[:500]
    meta = {"filename": file.filename, "path": saved_path, "summary_preview": summary[:400]}
    return {"answer": f"Файл {file.filename} загружен и проиндексирован.", "meta": meta}

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(user_id: str = Form(...), audio: UploadFile = File(...), model: Optional[str] = Form(None)):
    # save audio
    saved_path = save_uploaded_file(audio, subdir="audio")
    # read bytes
    with open(saved_path, "rb") as f:
        audio_bytes = f.read()
    # call ASR
    try:
        transcript_resp = transcribe_audio(audio_bytes)
        # transcribe_audio returns string (per earlier implementation)
        transcript = transcript_resp if isinstance(transcript_resp, str) else transcript_resp.get("text","")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ASR error: {e}")
    return {"transcript": transcript, "meta": {"source_file": saved_path}}
