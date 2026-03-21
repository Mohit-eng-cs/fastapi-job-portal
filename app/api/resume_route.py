from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.services.reusme_service import upload_resume
from app.schemas.resume import Resumeupload

router = APIRouter(prefix="/applications", tags=["Resumes"])


@router.post("/{application_id}/resume", response_model=Resumeupload)
async def upload_resume_api(
    application_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await upload_resume(db, application_id, file)