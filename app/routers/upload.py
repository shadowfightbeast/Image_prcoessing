from celery import Celery
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlmodel import select
import aiofiles
import uuid
import os
from app.models import ProcessingRequest
from app.database import get_session
from app.tasks import process_images
from app.celery_config import celery_app

router = APIRouter()

UPLOAD_DIR = 'uploads/'

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app = Celery('tasks', broker='redis://localhost:6379/0')

@router.post("/upload/")
async def upload_csv(file: UploadFile = File(...), session=Depends(get_session)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # CSV Validation should be here
    validation_error = None  # Placeholder for CSV validation
    if validation_error:
        raise HTTPException(status_code=400, detail=validation_error)

    request_id = str(uuid.uuid4())
    processing_request = ProcessingRequest(
        request_id=request_id,
        input_csv_path=file_path
    )
    session.add(processing_request)
    session.commit()
    
    # Send task to Celery
    process_images.delay(request_id, file_path)

    return {"request_id": request_id}

@router.get("/status/{request_id}")
async def check_status(request_id: str, session=Depends(get_session)):
    statement = select(ProcessingRequest).where(ProcessingRequest.request_id == request_id)
    processing_request = session.exec(statement).first()
    if not processing_request:
        raise HTTPException(status_code=404, detail="Request ID not found")
    
    response = {"status": processing_request.status}

    if processing_request.status == "Completed":
        response["output_csv"] = processing_request.output_csv_path

    return response
