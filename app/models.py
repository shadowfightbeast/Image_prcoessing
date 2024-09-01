# app/models.py

from sqlmodel import SQLModel, Field
from typing import Optional

class ProcessingRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: str
    input_csv_path: str
    status: str = "Pending"
    output_csv_path: Optional[str] = None
