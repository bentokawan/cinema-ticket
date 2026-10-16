from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models as m
from ..database import get_db
from ..services.order_service import expire_pending

router = APIRouter(prefix="/api/showtimes", tags=["Showtimes"])

@router.get("/{showtime_id}/seats")
def get_seats(showtime_id: int, db: Session = Depends(get_db)):
    st = db.get(m.Showtime, showtime_id)
    if not st:
        raise HTTPException(404, "Showtime not found")
    
    taken_seats = {row.seat_id for row in db.query(m.OrderItem.seat_id).filter(m.OrderItem.showtime_id == showtime_id)}
    seats = db.query(m.Seat).filter(m.Seat.studio_id == st.studio_id).order_by(m.Seat.row_label, m.Seat.seat_number).all()
    
    return [
        {
            "id": s.id, 
            "row": s.row_label, 
            "number": s.seat_number,
            "status": "taken" if s.id in taken_seats else "available"
        }
        for s in seats
    ]