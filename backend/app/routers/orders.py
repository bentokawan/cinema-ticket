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

from datetime import datetime, timezone
from fastapi import HTTPException
from ..models import utcnow

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    svc.expire_pending(db)
    order = db.get(svc.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")

    expires_in = 0
    if order.expires_at:
        exp = order.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        diff = (exp - datetime.now(timezone.utc)).total_seconds()
        expires_in = max(0, int(diff))

    return {
        "id": order.id,
        "booking_code": order.booking_code,
        "status": order.status,
        "total_price": order.total_price,
        "movie": order.showtime.movie.title,
        "studio": order.showtime.studio.name if order.showtime.studio else "",
        "start_time": order.showtime.start_time.isoformat() if order.showtime.start_time else None,
        "customer_name": order.customer_name,
        "customer_email": order.customer_email,
        "poster_url": order.showtime.movie.poster_url if order.showtime and order.showtime.movie else "",
        "seats": [f"{item.seat.row_label}{item.seat.seat_number}" for item in order.items],
        "expires_in": expires_in,
        "expires_at": order.expires_at.isoformat() if order.expires_at else None,
        "payment_method": order.payment.method if order.payment else None,
        "paid_at": order.payment.paid_at.isoformat() if order.payment and order.payment.paid_at else None,
    }

@router.delete("/{order_id}")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    svc.cancel_order(db, order_id)
    return {"message": "Pesanan berhasil dibatalkan"}

@router.post("/{order_id}/pay")
def pay_order(order_id: int, body: PayRequest, db: Session = Depends(get_db)):
    order = svc.pay_order(db, order_id, body.method)
    return {"message": "Pembayaran berhasil", "status": order.status, "booking_code": order.booking_code}