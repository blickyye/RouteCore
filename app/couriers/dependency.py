from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException

from app.database.models import Courier
from app.database.dependency import get_db
from app.auth.config import security as security_config

from authx import TokenPayload

def get_current_courier(db: Session = Depends(get_db), payload: TokenPayload = Depends(security_config.access_token_required)) -> Courier:
    user_id = payload.sub

    courier = db.query(Courier).filter(Courier.user_id==int(user_id)).first()
    if not courier:
        raise HTTPException(
            status_code=403,
            detail='User is not a courier or courier is not available'
        )

    return courier