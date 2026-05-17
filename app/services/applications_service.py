from sqlalchemy.orm import Session
from app.curd.jobs import *
from app.curd.applications import* 
from app.schemas.applications_schema import *
from app.utils.helpers import *
from fastapi import HTTPException
from app.models.user import User



def create_application_ser(db:Session,data:ApplicationCreate,current_user: User):
     candidate_id = current_user.id
     job = get_job(db,data.job_id)
     if not job:
          raise HTTPException(status_code=404,detail="job not found")
     existing_app = get_application_by_candidate(db,candidate_id,data.job_id)
     if existing_app:
          raise HTTPException(status_code=400,detail=f"application allready exists for the job ${job}")
     
     application_data ={
          "candidate_id":candidate_id,
          "job_id":data.job_id
     }
     try:
          new_app = create_application(db,application_data)
          db.flush()
          create_status_history(db,{
               "application_id":new_app.id,
               "old_status":None,
               "new_status":"applied",
               "changed_by":candidate_id
          })
          db.commit()
          db.refresh(new_app)
     except Exception as e:
          db.rollback()
          raise e
     
     return new_app        