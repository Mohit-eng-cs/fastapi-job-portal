from sqlalchemy.orm import Session
from app.models.resume import Resume

def create_resume(db:Session,application_id:int,file_name:str,file_path:str,file_size:str,content_type:str):
    resume_data = Resume(application_id=application_id,file_name=file_name,file_path=file_path,file_size=file_size,content_type=content_type)

    db.add(resume_data)
    db.commit()
    db.refresh(resume_data)


    return resume_data