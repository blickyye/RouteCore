from fastapi import APIRouter, Depends

from app.schemes.orders import CreateOrder
from app.database.dependency import get_db
from app.database.models import User, Courier
from app.orders.dependency import get_current_client
from app.orders import service as orders_service
from app.couriers.dependency import get_current_courier
from app.schemes.orders import StatusChange

from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/')
def create_order(order: CreateOrder, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    return orders_service.create_order(db, current_user.id, order.pickup_address, order.delivery_address, order.description)

@router.post('/courier/{order_id}/accept')
def accept_order(order_id: int, db: Session = Depends(get_db), current_courier: Courier = Depends(get_current_courier)):
    return orders_service.accept_order(db, current_courier, order_id)

@router.get('/my')
def show_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    return orders_service.show_my_orders(db, current_user.id)

@router.get('/courier/available')
def show_available_orders(db: Session = Depends(get_db), current_courier: Courier = Depends(get_current_courier)):
    return orders_service.show_available_orders(db)

@router.get('/courier/my')
def show_accepted_by_me_orders(db: Session = Depends(get_db), current_courier: Courier = Depends(get_current_courier)):
    return orders_service.show_accepted_by_me_orders(db, current_courier.id)

@router.patch('/courier/{order_id}/status')
def change_order_status(order_id: int, change_data: StatusChange, db: Session = Depends(get_db), current_courier: Courier = Depends(get_current_courier)):
    return orders_service.change_order_status(db, current_courier, order_id, change_data.new_status)

@router.patch('/{order_id}/cancel')
def cancel_order(order_id: int, db: Session = Depends(get_db), current_client: User = Depends(get_current_client)):
    return orders_service.cancel_order(db, current_client.id, order_id)