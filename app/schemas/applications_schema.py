from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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

class Apphist(BaseModel):
    application_id:int
    old_status:str
    new_status:str
    changed_by:int

class Apphistcreate(Apphist):
    pass



