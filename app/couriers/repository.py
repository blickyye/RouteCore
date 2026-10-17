from sqlalchemy.orm import Session

from app.database.models import Courier, User
from app.enums.user_role_enum import UserRole

def create_courier(db: Session, user_id) -> Courier:
    courier = Courier(
        user_id=user_id
    )
    user = db.query(User).filter(User.id==user_id).first()
    user.role = UserRole.COURIER
    db.add(courier)
    db.flush()

    return courier

def get_courier_by_user_id(db: Session, user_id) -> Courier | None:
    return db.query(Courier).filter(Courier.user_id==user_id).first()

