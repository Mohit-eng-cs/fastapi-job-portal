from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate,LoginRequest, UpdateUser
from app.core.security import hash_password, create_access_token, verify_password


class UserService:
    @staticmethod
    def register_user(data: UserCreate, db: Session):
        # Normalize email
        email = data.email.strip().lower()
        # Check if user already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password
        hashed_pw = hash_password(data.password)

        # Create user object
        user = User(
            email=email,
            password=hashed_pw,
            name=data.name,
            phone=data.phone,
            location=data.location,
            exp=data.exp,
            role=data.role
        )

        # Save to DB
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        # Create JWT token
        token = create_access_token({"sub": str(user.id), "role": user.role})

        # Return safe response (NO password)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "location": user.location,
                "exp": user.exp
            }
        }

    # ---------------- LOGIN USER ---------------- #
    @staticmethod
    def login_user(user_data: LoginRequest, db: Session):
        email = user_data.email.strip().lower()
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id), "role": user.role})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role
            }
        }

    # ---------------- UPDATE USER ---------------- #
    @staticmethod
    def update_user(db: Session, current_user: User, payload: UpdateUser):
        data = payload.model_dump(exclude_unset=True)

        for key, value in data.items():
            # If password is updated → hash it
            if key == "password":
                value = hash_password(value)

            setattr(current_user, key, value)

        db.commit()
        db.refresh(current_user)

        return {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "role": current_user.role,
            "location": current_user.location,
            "exp": current_user.exp
        }
    


