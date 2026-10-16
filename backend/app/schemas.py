from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal

class OrderCreate(BaseModel):
    showtime_id: int
    seat_ids: List[int] = Field(..., min_length=1,max_length=6)
    customer_name: str = Field(...,min_length=1,max_length=100)
    customer_email: EmailStr
    customer_phone: str = Field(...,min_length=7,max_length=13)

class PayRequest(BaseModel):
    method: Literal["transfer","card","ewallet"]