from app.logger import logger
from settings import fetch_settings

from fastapi import Header, HTTPException

def authenticate(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        logger.error("Missing or invalid token format in Authorization header.")
        raise HTTPException(
            status_code=401, detail="Unauthorized: Invalid token format"
        )

    token = authorization[len("Bearer ") :]

    if token != fetch_settings().auth_token:
        logger.error("Unauthorized access attempt with token: %s", token)
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

    return token
