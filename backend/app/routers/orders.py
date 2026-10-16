from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import OrderCreate, PayRequest
from ..services import order_service as svc

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("/", status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    order = svc.create_order(db, data)
    return {"id": order.id, "booking_code": order.booking_code, "status": order.status, "expires_at": order.expires_at}

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(svc.Order, order_id)
    return {
        "id": order.id, "booking_code": order.booking_code, "status": order.status,
        "total_price": order.total_price, "movie": order.showtime.movie.title,
        "customer_name": order.customer_name, "customer_email": order.customer_email,
        "seats": [f"{item.seat.row_label}{item.seat.seat_number}" for item in order.items]
    }

@router.post("/{order_id}/pay")
def pay_order(order_id: int, body: PayRequest, db: Session = Depends(get_db)):
    order = svc.pay_order(db, order_id, body.method)
    return {"message": "Pembayaran berhasil", "status": order.status, "booking_code": order.booking_code}