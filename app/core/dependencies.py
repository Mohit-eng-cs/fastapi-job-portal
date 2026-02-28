from fastapi import Depends, HTTPException, status
from app.core.roles import UserRole
from app.models.user import User
from app.core.security import get_current_user  




def require_role(allowed_role:list[UserRole]):
    def role_checker(user:User=Depends(get_current_user)):
        if user.role not in allowed_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to perform this action")
        return user
    return role_checker
 