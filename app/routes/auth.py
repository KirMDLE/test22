###(регистрация и авторизация)

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_toket, get_password_hash, verify_password
from app.dependencies import get_db


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/register')
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    not_new_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not_new_user:
        raise HTTPException(status_code=400, detail="Email уже используется")
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),        
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'message':  "Пользователь успешно зарегистрирован", "user_id": new_user.id}


@router.post('/login', response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    refresh_token = create_refresh_toket(data={"sub": db_user.email})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires
    )

    return {
        "message": "Вход успешен",
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
        }