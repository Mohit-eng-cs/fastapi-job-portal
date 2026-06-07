import os
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.curd.resume import create_resume

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_TYPES = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

async def upload_resume(
        db:Session,
        application_id:int,
        file:UploadFile
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400,detail="invalid file type")
    
    file.file.seek(0,2)
    size= file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400,detail="File too large")
      
    file_extention = os.path.splitext(file.filename)[1]

    unique_name = f"{uuid.uuid4()}{file_extention}"

    file_path = os.path.join(UPLOAD_DIR,unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    resume = create_resume(
        db=db,
        application_id=application_id,
        file_name=file.filename,
        file_path=file_path,
        file_size=size,
        content_type=file.content_type
    )

    return resume 



    
    


