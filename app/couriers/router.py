from fastapi import APIRouter, Depends

from app.auth.dependency import get_current_user
from app.database.dependency import get_db
from app.database.database import User
from app.couriers import service as couriers_service

from sqlalchemy.orm import Session


router = APIRouter()

@router.post('/apply')
def create_courier(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return couriers_service.create_courier(db, current_user.id)