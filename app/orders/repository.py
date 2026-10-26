from sqlalchemy.orm import Session

from app.database.models import Order, Courier, OrderStatusHistory, MenuItem, OrderItem
from app.enums.order_status_enum import OrderStatus
from app.schemes.orders import OrderItemCreate

def create_order(db: Session, user_id: int, restaraunt_id: int, items: list[OrderItem]) -> Order:

    order = Order(
        user_id=user_id,
        restaraunt_id=restaraunt_id,
        items=items
    )

    db.add(order)
    db.flush()

    return order

def show_my_orders(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id==user_id).all()

def show_available_orders(db: Session) -> list[Order]:
    return db.query(Order).filter(Order.status==OrderStatus.PENDING).all()

def get_order_by_id(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id==order_id).first()

def accept_order(db: Session, courier: Courier, order: Order) -> Order:
    old_order_status = order.status
    order.status, order.courier_id, courier.is_available = OrderStatus.ACCEPTED, courier.id, False

    logging_change_status(db, order.id, old_order_status, order.status)

    return order

def show_accepted_by_me_orders(db: Session, courier_id: int) -> list[Order]:
    return db.query(Order).filter(Order.courier_id==courier_id).all()

def change_order_status(db: Session, courier: Courier, order: Order, new_status: OrderStatus) -> Order:
    old_order_status = order.status
    order.status = new_status

    logging_change_status(db, order.id, old_order_status, order.status)

    if order.status in (OrderStatus.CANCELLED, OrderStatus.DELIVERED):
        courier.is_available = True

    return order

def cancel_order(db: Session, order: Order) -> Order:
    old_order_status = order.status
    order.status = OrderStatus.CANCELLED

    logging_change_status(db, order.id, old_order_status, order.status)

    return order

def logging_change_status(db: Session, order_id: int, old_status: OrderStatus, new_status: OrderStatus):
    log = OrderStatusHistory(
        order_id=order_id,
        old_status=old_status,
        new_status=new_status
    )

    db.add(log)
    db.flush()

def parsing_item_to_order_item(db: Session, item: OrderItemCreate, rest_id: int):
    item_model = check_menu_item_exists(db, item.menu_item_id, rest_id)

    order_item = OrderItem(
        menu_item_id=item.menu_item_id,
        quantity=item.quantity,
        curr_price=item_model.price
    )

    return order_item

def check_menu_item_exists(db: Session, item_id: int, restaraunt_id: int) -> MenuItem | None:
    return db.query(MenuItem).filter(MenuItem.id==item_id, MenuItem.restaraunt_id==restaraunt_id).first()