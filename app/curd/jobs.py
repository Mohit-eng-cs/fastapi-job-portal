import math
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.job import Job 
from app.schemas.jobs import JobCreate,JobUpdate

def create_job(db:Session,data:JobCreate):
    job = Job(**data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def find_last(db:Session):
    last_job = db.query(Job).order_by(Job.id.desc()).first()
    return last_job

def get_job(db:Session,job_id:int):
    return db.query(Job).filter(Job.id ==job_id).first()

def get_jobs(db:Session):
    return db.query(Job).all()

    
def del_job(db:Session,job_id:int):
    job = get_job(db,job_id)
    if not job:
        return None
    
    db.delete(job)
    db.commit()
    return job

def get_jobs_filter(
    db: Session,
    limit_n: int,
    Offset_s: int,
    location: str | None = None,
    company: str | None = None,
    skills: str | None = None,
    keyword: str | None = None,
):
    base = db.query(Job)
    if location:
        base = base.filter(Job.location.ilike(f"%{location}%"))
    if company:
        base = base.filter(Job.company == company)
    if skills:
        base = base.filter(Job.skills_required.ilike(f"%{skills}%"))
    if keyword:
        base = base.filter(or_(
            Job.title.ilike(f"%{keyword}%"),
            Job.description.ilike(f"%{keyword}%")
        ))

    total = base.count()
    jobs = base.limit(limit_n).offset(Offset_s).all()
    return jobs, total


def update_job_db(db: Session, job_id: int, data: JobUpdate) -> Job | None:
    job = get_job(db, job_id)
    if not job:
        return None

    update_values = data.model_dump(exclude_unset=True)
    for field, value in update_values.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job