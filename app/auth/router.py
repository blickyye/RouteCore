from fastapi import APIRouter, Depends

from app.schemes.user_auth import RegistrationRequest, RegistrationResponse, LoginRequest, TokenResponse
from app.database.dependency import get_db
from app.database.models import User
from app.auth.dependency import get_current_user
from app.auth import service as auth_service

from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/registration', response_model=RegistrationResponse)
def create_user(user: RegistrationRequest, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user.login, user.email, user.password)

@router.post('/login', response_model=TokenResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, user.login, user.password)

@router.get('/me', response_model=RegistrationResponse)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user