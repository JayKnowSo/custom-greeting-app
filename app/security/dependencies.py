


from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from app.security.jwt import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_current_user(credentials=Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")