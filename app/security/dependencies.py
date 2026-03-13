


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt
from app.security.jwt import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_current_user(credentials=Depends(security)):
    """
    Decodes JWT and returns the full payload dict.
    Raises 401 if token is missing, expired, or tampered.
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        # Ensure both sub and role are present in the token
        if payload.get("sub") is None or payload.get("role") is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing required claims"
            )
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def require_role(*allowed_roles: str):
    """
    Returns a FastAPI dependency that enforces role membership.
    Usage: Depends(require_role("admin"))
    """
    def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required: {list(allowed_roles)}, "
                       f"Your role: {current_user.get('role')}"
            )
        return current_user
    return role_checker


# ── Ready-to-use guards — import these directly into routes ──
require_admin    = require_role("admin")
require_user     = require_role("admin", "user")
require_readonly = require_role("admin", "user", "readonly")
