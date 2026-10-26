from sqlalchemy.orm import Session

from app.database.models import Restaraunt, MenuItem

def get_restaraunt_by_id(db: Session, rest_id: int) -> Restaraunt | None:
    return db.query(Restaraunt).filter(Restaraunt.id==rest_id, Restaraunt.is_active==True).scalar()

def get_restaraunt_menu(db: Session, rest_id: int) -> list[MenuItem]:
    return db.query(MenuItem).filter(MenuItem.restaraunt_id==rest_id).all()