###(заполнение профиля мастера после регистрации)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas


router = APIRouter(prefix='/masters', tags=['masters'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create_profile')
def create_master_profile(profile: schemas.MasterProfileCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == profile.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    not_new_profile = db.query(models.MasterProfile).filter(models.MasterProfile.user_id == user.id).first()
    if not_new_profile:
        raise HTTPException(status_code=400, detail="Профиль уже создан")

    new_profile = models.MasterProfile(
        user_id=user.id,
        specialization=profile.specialization,
        description=profile.description
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {'message':  "Профиль мастера успешно создан"}
