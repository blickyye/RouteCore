from app.database.database import Base
from app.enums.order_status_enum import OrderStatus
from app.enums.user_role_enum import UserRole

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from datetime import datetime

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True)
    is_available: Mapped[bool] = mapped_column(default=True)

class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    courier_id: Mapped[int | None] = mapped_column(default=None)
    pickup_address: Mapped[str]
    delivery_address: Mapped[str]
    description: Mapped[str]
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)