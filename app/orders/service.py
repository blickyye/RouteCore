from sqlalchemy.orm import Session

from app.database.models import Order
from app.orders import repository as orders_repository
from app.enums.order_status_enum import OrderStatus

from fastapi import HTTPException

def create_order(db: Session, user_id: int, pick_address: str, deliv_address: str, description: str | None) -> Order:
    order = orders_repository.create_order(db, user_id, pick_address, deliv_address, description)

    db.commit()
    db.refresh(order)

    return order

def show_my_orders(db: Session, user_id: int) -> list[Order]:
    return orders_repository.show_my_orders(db, user_id)

def show_available_orders(db: Session) -> list[Order]:
    orders = orders_repository.show_available_orders(db)
    if not orders:
        raise HTTPException(
            status_code=404,
            detail='Orders not found'
        )

    return orders

def accept_order(db: Session, courier_id: int, order_id: int) -> Order:
    order = orders_repository.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=404, 
            detail='Order with this id not found'
        )
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=401, 
            detail='Order with this id already in delivery'
        )

    accepted_order = orders_repository.accept_order(db, courier_id, order)
    db.commit()
    db.refresh(order)

    return accepted_order

def show_accepted_by_me_orders(db: Session, courier_id: int) -> list[Order]:
    return orders_repository.show_accepted_by_me_orders(db, courier_id)

def change_order_status(db: Session, current_courier_id: int, order_id: int, new_status: OrderStatus) -> Order:
    order = orders_repository.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail='Order with this id not found'
        )
    if order.courier_id != current_courier_id:
        raise HTTPException(
            status_code=403, 
            detail='You are not assigned to this order'
        )

    changed_order = orders_repository.change_order_status(db, order, new_status)

    db.commit()
    db.refresh(changed_order)
    return changed_order