from app.database.database import Base
from app.enums.order_status_enum import OrderStatus
from app.enums.user_role_enum import UserRole

from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    courier: Mapped['Courier | None'] = relationship('Courier', back_populates='user')
    orders: Mapped[list['Order'] | None] = relationship('Order', back_populates='user')

class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True)
    is_available: Mapped[bool] = mapped_column(default=True)

    user: Mapped['User'] = relationship('User', back_populates='courier')
    taked_orders: Mapped[list['Order'] | None] = relationship('Order', back_populates='courier')

class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    courier_id: Mapped[int | None] = mapped_column(ForeignKey('courier.id'), default=None)
    restaraunt_id: Mapped[int] = mapped_column(ForeignKey('restaraunt.id'))
    items: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='order')
    status: Mapped[OrderStatus] = mapped_column(OrderStatusEnum, default=OrderStatus.PENDING)

    user: Mapped['User'] = relationship('User', back_populates='orders')
    courier: Mapped['Courier'] = relationship('Courier', back_populates='taked_orders')

class OrderStatusHistory(Base):
    __tablename__ = 'order_status_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    old_status: Mapped[OrderStatus] = mapped_column(OrderStatusEnum)
    new_status: Mapped[OrderStatus] = mapped_column(OrderStatusEnum)
    changed_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

class Restaraunt(Base):
    __tablename__ = 'restaraunt'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    address: Mapped[str]
    image_url: Mapped[str | None] = mapped_column(default=None)
    is_active: Mapped[bool] = mapped_column(default=True)

    menu_items: Mapped[list['MenuItem']] = relationship('MenuItem', back_populates='restaraunt')

class MenuItem(Base):
    __tablename__ = 'menu_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    restaraunt_id: Mapped[int] = mapped_column(ForeignKey('restaraunt.id'))

    restaraunt: Mapped['Restaraunt'] = relationship('Restaraunt', back_populates='menu_items')

class OrderItem(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey('menu_item.id'))
    quantity: Mapped[int] = mapped_column(default=1)
    curr_price: Mapped[float]
    order: Mapped['Order'] = relationship('Order', back_populates='items')
    order_id: Mapped[int | None] = mapped_column(ForeignKey('order.id'), default=None)