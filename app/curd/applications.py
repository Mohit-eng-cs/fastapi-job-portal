import math
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.applications import Application
from app.schemas.applications_schema import ApplicationCreate


def create_application(db:Session,data:ApplicationCreate):
    ap_data = Application(**data.model_dump())
    db.add()
    db.commit
    db.refresh(ap_data)
    return ap_data