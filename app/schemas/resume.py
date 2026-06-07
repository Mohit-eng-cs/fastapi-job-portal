from pydantic import BaseModel
from datetime import datetime

class Resumeupload(BaseModel):
    id:int
    application_id:int
    file_name:str
    file_path:str
    file_size:int
    content_type:str
    uploaded_at:datetime

    class Config:
        from_attributes = True


