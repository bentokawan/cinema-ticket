import random 
import string 
from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.orm import Session
from ..models import Order, OrderItem, Payment, Seat, Showtime, utcnow

HOLD_MINUTES = 10

def expire_pending(db: Session) -> None:
    expired = db.query(Order).filter(Order.status == "pending", Order.expires_at < utcnow()).all()

    for order in expired:
        order.status = "expired"
        for item in list(order.items):
            db.delete(item)
    if expired:
        db.commit()
                
def generate_booking_code() -> str:
    return "CNM-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))

def create_order(db: Session, data) -> Order:
    expire_pending(db)
    
    showtime = db.get(Showtime, data.showtime_id)
    if not showtime:
        raise HTTPException(404, "Showtime not found")
    
    seat_ids = set(data.seat_ids)
    seats = db.query(Seat).filter(Seat.id.in_(seat_ids),Seat.studio_id == showtime.studio_id).all()

    if len(seats) != len(seat_ids):
        raise HTTPException(422, "Invalid seat IDs")

    order = Order(
        booking_code=generate_booking_code(),
        showtime_id=showtime.id,
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=data.customer_phone,
        total_price=showtime.price * len(seats),
        status="pending",
        expires_at=utcnow() + timedelta(minutes=HOLD_MINUTES),
    )

    for seat in seats:
        order.items.append(OrderItem(
            showtime_id=showtime.id,
            seat_id=seat.id,
            price=showtime.price
        ))

    db.add(order)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Seats are already taken")
    
    db.refresh(order)
    return order

def pay_order(db: Session, order_id:int, method:str) -> Order:
    expire_pending(db)
    
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    if order.status == "expired":
        raise HTTPException(422, "Order is expired, please make a new order")
    if order.status != "pending":
        raise HTTPException(422, f"Order is {order.status}, cannot pay")
    
    db.add(Payment(order_id=order.id, method=method, amount=order.total_price))
    order.status = "paid"
    db.commit()
    db.refresh(order)
    return order
    