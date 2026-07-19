from sqlalchemy.orm import Session
from app.curd.jobs import *
from app.schemas.jobs import *
from app.utils.helpers import *
from fastapi import HTTPException
from app.models.user import User
from app.utils.exception import NotAdminError,JobNotFoundError,ServiceExceptions
from sqlalchemy.exc import SQLAlchemyError
from app.core.dependencies import UserRole

def create_job_service(db: Session, data: JobCreate,current_user:User):
   
    is_admin=current_user.role==UserRole.ADMIN
    is_recrut=current_user.role==UserRole.RECRUITER
    
    if not (is_recrut or is_admin):
        raise NotAdminError
    
    existing = (
        db.query(Job)
        .filter(Job.title == data.title, Job.company == data.company)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Job with this title already exists for this company")
    last_added = find_last(db)
    next_job_id = (last_added.id+ 1) if last_added else 1    

    job_code = Jobs_code(data.title, next_job_id)

    payload = Job(
        title=data.title,
        company=data.company,
        description=data.description,
        id=next_job_id,
        job_code=job_code,
        Min_sal=data.Min_sal,
        Max_sal=data.Max_sal,
        location=data.location,
        skills_required=data.skills_required,
        posted_by=current_user.id
    )

    try:
        db.add(payload)
        db.commit()
        db.refresh(payload)
    
    except SQLAlchemyError as e:
        db.rollback()
        print("🔥 ACTUAL ERROR:", repr(e))
        raise HTTPException(status_code=500,detail="Database error occured")

    return payload


def delete_job_service(
    db: Session,
    job_id: int,
    current_user: User
) -> None:

    job = get_job(db, job_id)
    if not job:
        raise JobNotFoundError()

    is_admin = current_user.role == UserRole.ADMIN
    is_owner = job.posted_by == current_user.id

    if not (is_admin or is_owner):
        raise NotAdminError()

    del_job(db, job)

def get_jobs(db:Session,page:int,limit:int,location: str | None = None,
    company: str | None = None,
    skills: str | None = None,
    keyword: str | None = None,):


    location = location.strip() if location else None
    company =  company.strip() if company else None
    skills =  skills.strip() if skills else None
    keyword = keyword.strip() if keyword else None 

    if keyword and len(keyword)<2:
        raise ServiceExceptions("Keyword must be at least 2 characters long")
    
    offset = (page-1)*limit
    try:
        jobs,total= get_jobs_filter(
            db=db,
            limit_n=limit,
            Offset_s=offset,
            location=location,
            company=company,
            skills=skills,
            keyword=keyword,
        )
    except SQLAlchemyError as e:
        raise ServiceExceptions("Failed to fetch jobs. Please try again later.")
    
    total_pages = math.ceil(total/limit) if total > 0 else 1
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "data": jobs,
    }   


# ---------- Service layer (service.py) ----------

def update_job_service(
    db: Session,
    data: JobUpdate,
    job_id: int,
    current_user: User,
) -> Job:
    job = get_job(db, job_id)
    if not job:
        raise JobNotFoundError

    update_values = data.model_dump(exclude_unset=True)
    if not update_values:
        raise HTTPException(status_code=400, detail="No update fields provided")

    is_admin = current_user.role == UserRole.ADMIN
    is_owner = current_user.id == job.posted_by

    # Only admins, or the recruiter who created THIS job, can update it.
    if not (is_admin or is_owner):
        raise NotAdminError

    updated_job = update_job_db(db, job_id, data)
    if not updated_job:
        raise JobNotFoundError

    return updated_job