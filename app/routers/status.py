from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from app.models import ProcessingRequest
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/status/{request_id}")
def check_status(request_id: str, session: Session = Depends(get_session)):
    processing_request = session.query(ProcessingRequest).filter_by(request_id=request_id).first()
    if not processing_request:
        raise HTTPException(status_code=404, detail="Request ID not found.")

    response = {
        "request_id": processing_request.request_id,
        "status": processing_request.status,
        "created_at": processing_request.created_at,
        "updated_at": processing_request.updated_at
    }

    if processing_request.status == "Completed" and processing_request.output_csv_path:
        response["output_csv_url"] = f"http://localhost:8000/{processing_request.output_csv_path}"

    return response

@router.get("/download/{request_id}")
def download_output_csv(request_id: str, session: Session = Depends(get_session)):
    processing_request = session.query(ProcessingRequest).filter_by(request_id=request_id).first()
    if not processing_request or processing_request.status != "Completed":
        raise HTTPException(status_code=404, detail="Output CSV not available.")

    return FileResponse(path=processing_request.output_csv_path, filename=f"{request_id}_output.csv", media_type='text/csv')
