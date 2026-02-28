from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.sessions import SessionLocal,get_db
from app.schemas.user import *
from app.core.security import get_current_user
from app.models.user import User
from app.services.users import UserService
router = APIRouter()


@router.post("/login")
def login(data:LoginRequest, db: Session = Depends(get_db)):
    return UserService.login_user(data,db)

@router.post("/register")
def register(data:UserCreate,db:Session = Depends(get_db)):
    return UserService.register_user(data,db)

@router.put("/update")
def update_user_endpoint(
    update_data: UpdateUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserService.update_user(db, current_user, update_data)