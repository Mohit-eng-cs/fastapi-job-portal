# app/schemas/user.py
from app.core.dependencies import UserRole
from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None
    phone: str | None = None
    location: str | None = None
    exp: str | None = None
    role: UserRole 

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    name: str | None
    role: str

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    email: EmailStr |  None = None
    password: str | None = None
    name: str | None = None
    phone: str | None = None
    location: str | None = None
    exp: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
