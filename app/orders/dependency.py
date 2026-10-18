from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.auth.config import security as security_config
from app.database.models import User
from app.enums.user_role_enum import UserRole

from fastapi import Depends, HTTPException

from authx import TokenPayload


def get_current_client(db: Session = Depends(get_db), payload: TokenPayload = Depends(security_config.access_token_required)):
    user_id = payload.sub

    client = db.query(User).filter(User.id==int(user_id), User.role==UserRole.CLIENT).first()
    if not client:
        raise HTTPException(
            status_code=403,
            detail='User is not client'
        )

    return client