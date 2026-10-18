from app.database.database import Base
from app.enums.order_status_enum import OrderStatus
from app.enums.user_role_enum import UserRole

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Enum as SQLEnum

from datetime import datetime

OrderStatusEnum = SQLEnum(
    OrderStatus,
    name='orderstatus',
    values_callable=lambda x: [e.value for e in x]
)

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.CLIENT)
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
    courier_id: Mapped[int | None] = mapped_column(ForeignKey('courier.id'), default=None)
    pickup_address: Mapped[str]
    delivery_address: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[OrderStatus] = mapped_column(OrderStatusEnum, default=OrderStatus.PENDING)

class OrderStatusHistory(Base):
    __tablename__ = 'order_status_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    old_status: Mapped[OrderStatus] = mapped_column(OrderStatusEnum)
    new_status: Mapped[OrderStatus] = mapped_column(OrderStatusEnum)
    changed_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())