from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from app.db.sessions import SessionLocal, get_db
from app.schemas.user import *
from app.core.security import get_current_user
from app.models.job import *
from app.services.jobs_service import *
from app.core.roles import UserRole
from app.curd.jobs  import *
from app.core.dependencies import require_role
router = APIRouter()


@router.get(
    "/jobs",
    response_model=PaginatedJobsResponse
)
def list_jobs(
    page: int = Query(1, ge=1, le=100, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    location: str | None = Query(None, description="Filter by job location"),
    company: str | None = Query(None, description="Filter by company"),
    skills: str | None = Query(None, description="Filter by skills"),
    keyword: str | None = Query(None, description="Search title & description"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    jobs, total = get_jobs_filter(
        db=db,
        location=location,
        limit_n=limit,
        Offset_s=offset,
        company=company,
        skills=skills,
        keyword=keyword
    )

    total_pages = (total + limit - 1) // limit  # ceiling division, avoids importing math

    return PaginatedJobsResponse(
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        data=jobs
    )

@router.post("/create-new")
def create_job(data:JobCreate,db:Session=Depends(get_db),user:User=Depends(require_role([UserRole.RECRUITER,UserRole.ADMIN]))):
    return create_job_service(db=db,data=data,current_user=user)

@router.post("/delete/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(require_role([UserRole.RECRUITER, UserRole.ADMIN]))):
    return delete_job_service(db, job_id, user)

@router.patch("/update/{job_id}", response_model=JobResponse)
def update_job_endpoint(
    data: JobUpdate = Body(...),
    job_id: int = Path(..., description="Job ID to update"),
    db: Session = Depends(get_db),
    user: User = Depends(require_role([UserRole.RECRUITER, UserRole.ADMIN])),
) -> Job:
    return update_job_service(db, data, job_id, user)


