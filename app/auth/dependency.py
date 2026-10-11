from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException

from app.auth.config import security as security_config
from app.database.dependency import get_db
from app.database.models import User

from authx import TokenPayload

def get_current_user(db: Session = Depends(get_db), payload: TokenPayload = Depends(security_config.access_token_required)):
    user_id = payload.sub

    user = db.query(User).filter(User.id==int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    return user