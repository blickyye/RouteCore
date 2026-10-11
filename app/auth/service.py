from app.database.models import User
from app.schemes.user_auth import TokenResponse
from app.auth import security as auth_security
from app.auth import repository as auth_repository
from app.auth.config import security as security_config

from sqlalchemy.orm import Session

from fastapi import HTTPException

def create_user(db: Session, login, email, password) -> User:
    if not auth_repository.get_user_by_login(db, login):
        raise HTTPException(
            status_code=400,
            detail=f'User with login {login} already exists'
        )
    
    password_hash = auth_security.hash_the_password(password)
    new_user = auth_repository.create_user(db, login, email, password_hash)
    db.commit()
    db.refresh(new_user)

    return new_user

def login(db: Session, login, password) -> TokenResponse:
    current_user = auth_repository.get_user_by_login(db, login)
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail='Invalid login or password'
        )

    if not auth_security.check_the_password(current_user.hashed_password, password):
        raise HTTPException(
            status_code=401,
            detail='Invalid login or password'
        )

    token = security_config.create_access_token(uid=str(current_user.id))

    return TokenResponse(access_token=token)