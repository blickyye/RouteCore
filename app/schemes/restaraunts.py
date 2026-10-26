from pydantic import BaseModel

class RestarauntResponse(BaseModel):
    model_config = {'from_attributes': True}

    id: int
    name: str
    description: str
    address: str
    image_url: str | None
    is_active: bool

class MenuItemResponse(BaseModel):
    model_config = {'from_attributes': True}

    id: int
    name: str
    price: float