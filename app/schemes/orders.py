from pydantic import BaseModel

from app.enums.order_status_enum import OrderStatus

class CreateOrder(BaseModel):
    pickup_address: str
    delivery_address: str
    description: str | None = None

class StatusChange(BaseModel):
    new_status: OrderStatus