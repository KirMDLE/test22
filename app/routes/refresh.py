from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel

from app.security import ALGORITHM, SECRET_KEY, create_access_token

router = APIRouter()

class TokenRefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh_token(token_data: TokenRefreshRequest):
    try:
        payload = jwt.decode(token_data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Недопустимый токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Недопустимый токен")

    new_access_token = create_access_token(data={"sub": email})
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
