from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.database.models import Restaraunt
from app.schemes.restaraunts import RestarauntResponse, MenuItemResponse
from app.restaraunts import service as rest_service

router = APIRouter()

@router.get('/', response_model=list[RestarauntResponse])
def show_list_of_restaraunts(db: Session = Depends(get_db)):
    return db.query(Restaraunt).all()

@router.get('/{restaraunt_id}', response_model=RestarauntResponse)
def show_restaraunt(restaraunt_id: int, db: Session = Depends(get_db)):
    return db.query(Restaraunt).filter(Restaraunt.id==restaraunt_id).first()

@router.get('/{restaraunt_id}/menu', response_model=MenuItemResponse)
def show_restaraunt_menu(restaraunt_id: int, db: Session = Depends(get_db)):
    return rest_service.show_restaraunt_menu(db, restaraunt_id)