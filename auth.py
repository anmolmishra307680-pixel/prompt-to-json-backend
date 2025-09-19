"""JWT Authentication for API"""

import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
SECRET_KEY = os.getenv("JWT_SECRET", "bhiv-jwt-secret-2024")
ALGORITHM = "HS256"

def create_access_token(data: dict):
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Login endpoint
def authenticate_user(username: str, password: str):
    """Simple user authentication"""
    if username == "admin" and password == "bhiv2024":
        return create_access_token({"sub": username})
    raise HTTPException(status_code=401, detail="Invalid credentials")