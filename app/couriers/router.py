from fastapi import APIRouter, Depends

from app.auth.dependency import get_current_user
from app.database.dependency import get_db
from app.database.models import User, Courier
from app.couriers import service as couriers_service
from app.couriers.dependency import get_current_courier

from sqlalchemy.orm import Session


router = APIRouter()

@router.post('/')
def create_courier(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return couriers_service.create_courier(db, current_user.id)

@router.get('/me')
def get_me(db: Session = Depends(get_db), current_courier: Courier = Depends(get_current_courier)):
    return current_courier