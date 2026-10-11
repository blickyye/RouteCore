from sqlalchemy.orm import Session

from app.database.models import Courier
from app.couriers import repository as couriers_repository

from fastapi import HTTPException

def create_courier(db: Session, user_id) -> Courier:
    if couriers_repository.get_courier_by_user_id(db, user_id):
        raise HTTPException(
            status_code=400,
            detail='This user is already courier'
        )

    courier = couriers_repository.create_courier(db, user_id)
    db.commit()
    db.refresh(courier)

    return courier