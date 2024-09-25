from enum import Enum
from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    quantity_on_hand: int


class CreateOrder(BaseModel):
    product_id: int
    quantity: int


class OrderStatusEnum(Enum):
    in_progress = 'В процессе'
    sent = 'Отправлен'
    delivered = 'Доставлен'

