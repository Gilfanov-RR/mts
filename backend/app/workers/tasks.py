from celery import Celery
from app.services.rag import ingest_document
from app.services.mws_gateway import call_mws

celery = Celery("tasks", broker="redis://redis:6379/0")

@celery.task
def ingest_doc_task(file_path, metadata):
    ingest_document(file_path, metadata)

@celery.task
def async_model_call(prompt, model):
    return call_mws(prompt=prompt, model=model)
