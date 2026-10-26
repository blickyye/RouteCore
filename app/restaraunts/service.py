from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.database.models import Restaraunt
from app.restaraunts import repository as rest_repository

def check_exists_restaraunt(db: Session, rest_id: int) -> Restaraunt:
    restaraunt = rest_repository.get_restaraunt_by_id(db, rest_id)
    
    if not restaraunt:
        raise HTTPException(
            status_code=404,
            detail=f'Restaraunt with id {rest_id} does not exists or restaraunt is not active'
        )

    return restaraunt

def show_restaraunt_menu(db: Session, rest_id: int):
    restaraunt = check_exists_restaraunt(db, rest_id)

    menu = rest_repository.get_restaraunt_menu(db, rest_id)

    return menu