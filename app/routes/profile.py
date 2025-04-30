# profile.py

from fastapi import APIRouter, Depends
from ..security import get_current_user
from .. import models

router = APIRouter()

@router.get("/profile")
def read_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }
