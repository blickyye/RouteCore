from sqlalchemy.orm import Session

from app.database.models import Courier

def create_courier(db: Session, user_id) -> Courier:
    courier = Courier(
        user_id=user_id
    )

    db.add(courier)
    db.flush()

    return courier

def get_courier_by_user_id(db: Session, user_id) -> Courier | None:
    return db.query(Courier).filter(Courier.user_id==user_id).first()

