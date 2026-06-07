import math
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.applications import Application,ApplicationStatusHistory
from app.schemas.applications_schema import *


def create_application(db:Session,data:ApplicationCreate):
    ap_data = Application(**data)
    db.add(ap_data)
    return ap_data

def get_application_by_candidate(db:Session,candidate_id:int,job_id:int):
    db.query(Application).filter(Application.candidate_id==candidate_id,Application.job_id==job_id).first()

def create_status_history(db:Session,data:Apphistcreate):
    app_hist_data=ApplicationStatusHistory(**data)
    db.add(app_hist_data)
    return app_hist_data
