from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.applications_schema import *
from app.services.applications_service import *
from app.schemas.applications_schema import*
from app.db.sessions import SessionLocal,get_db
from app.schemas.user import *
from app.core.security import get_current_user
from app.models.job import *
from app.services.jobs_service import *
router = APIRouter()


@router.post("/create_appliction",response_model=ApplicationResponse)
def crete_application(data:ApplicationCreate,db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    return create_application_ser(db,data,current_user)