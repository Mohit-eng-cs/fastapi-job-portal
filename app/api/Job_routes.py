from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.sessions import SessionLocal,get_db
from app.schemas.user import *
from app.core.security import get_current_user
from app.models.job import *
from app.services.jobs_service import *
from app.core.roles import UserRole
from app.core.dependencies import require_role
router = APIRouter()


@router.get(
    "/jobs",
    response_model=PaginatedJobsResponse
)
def list_jobs(
    limit : int =Query(10,ge=1,le=100,description="Page number"),
    page : int = Query(10,ge=1,le=100,description="items per page"),
    location: str | None = Query(None, description="Filter by job location"),
    company: str | None = Query(None, description="Filter by company"),
    skills: str | None = Query(None, description="Filter by skills"),
    keyword: str | None = Query(None, description="Search title & description"),
    db: Session = Depends(get_db)
):
    return get_jobs(
        db=db,
        location=location,
        page=page,
        limit=limit,
        company=company,
        skills=skills,
        keyword=keyword
    )

@router.post("/create-new")
def create_job(data:JobCreate,db:Session=Depends(get_db),user:User=Depends(require_role([UserRole.RECRUITER,UserRole.ADMIN]))):
    return create_job_service(db=db,data=data,current_user=user)

@router.put("/update/${job_id}")
def update_job(updte:JobUpdate,jobs_id:int,db:Session=Depends(get_db),user:User=Depends(require_role([UserRole.RECRUITER,UserRole.ADMIN]))):
    return update_job_service(db,updte,jobs_id,require_role([UserRole.ADMIN,UserRole.RECRUITER]))


@router.post("/delete/${job_id}")
def delete_job(jobs_id:int,db:Session=Depends(get_db),user:User=Depends(require_role([UserRole.RECRUITER,UserRole.ADMIN]))):
    return delete_job_service(db,jobs_id,user)
