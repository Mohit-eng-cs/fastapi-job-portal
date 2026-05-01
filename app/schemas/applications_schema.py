from pydantic import BaseModel
from models import Application
from datetime import datetime

class ApplicationBase(BaseModel):
    job_id: int
    resume_url:str | None =None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    status: str
    resume_url: str | None
    created_at: datetime 
