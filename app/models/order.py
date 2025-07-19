from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    productId: str
    qty: int

class Order(BaseModel):
    userId: str
    items: List[OrderItem]
