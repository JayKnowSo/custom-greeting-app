


from fastapi import HTTPException
from app.security.password import verify_password
from app.security.jwt import create_access_token


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)
        
        # FIX: handle list return
        if isinstance(user, list):
            user = user[0] if user else None
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return create_access_token({"sub": user.username, "role": user.role})