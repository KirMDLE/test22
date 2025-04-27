###(создание заказов для мастеров)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas


router = APIRouter(prefix='/orders', tags=['orders'])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create_order')
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    client = db.query(models.User).filter(models.User.id == order.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    
    master = db.query(models.MasterProfile).filter(models.MasterProfile.user_id == order.master_id).first()
    if not master:
        raise HTTPException(status_code=404, detail="Мастер не найден")

    new_order = models.Order(
        client_id = client.id,
        master_id = master.id,
        description = order.description
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {'message':  "Заказ успешно создан"}
