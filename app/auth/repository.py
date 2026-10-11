from sqlalchemy.orm import Session

from app.database.models import User

def create_user(db: Session, login, email, password_hash) -> User:
    user = User(
        login=login, 
        email=email,
        hashed_password=password_hash
    )

    db.add(user)
    db.flush()

    return user

def get_user_by_login(db: Session, login) -> User | None:
    return db.query(User).filter(User.login==login).scalar()
