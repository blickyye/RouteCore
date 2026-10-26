from pydantic import BaseModel, Field

from app.enums.order_status_enum import OrderStatus

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)

class CreateOrder(BaseModel):
    restaraunt_id: int
    items: list[OrderItemCreate] = Field(min_length=1)

class StatusChange(BaseModel):
    new_status: OrderStatus
