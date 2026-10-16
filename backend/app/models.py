from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey,String, Text,UniqueConstraint, Boolean
from sqlalchemy.orm import relationship,Mapped,mapped_column
from .database import Base

def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    synopsis: Mapped[str] = mapped_column(Text, default="")
    genre: Mapped[str] = mapped_column(String(100), default="")
    duration_minutes: Mapped[int] = mapped_column(default=100)
    rating: Mapped[str] = mapped_column(String(10), default="SU")
    poster_url: Mapped[str] = mapped_column(String(500), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    showtimes: Mapped[list["Showtime"]] = relationship(back_populates="movie")

class Studio(Base):
    __tablename__ = "studios"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    total_rows: Mapped[int]
    seats_per_row: Mapped[int]
    seats: Mapped[list["Seat"]] = relationship(back_populates="studio")

class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (UniqueConstraint("studio_id", "row_label", "seat_number"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    studio_id: Mapped[int] = mapped_column(ForeignKey("studios.id", ondelete="CASCADE"))
    row_label: Mapped[str] = mapped_column(String(2))
    seat_number: Mapped[int]
    studio: Mapped["Studio"] = relationship(back_populates="seats")

class Showtime(Base):
    __tablename__ = "showtimes"
    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))
    studio_id: Mapped[int] = mapped_column(ForeignKey("studios.id", ondelete="CASCADE"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    price: Mapped[int]
    movie: Mapped["Movie"] = relationship(back_populates="showtimes")
    studio: Mapped["Studio"] = relationship()

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_code: Mapped[str] = mapped_column(String(20), unique=True)
    showtime_id: Mapped[int] = mapped_column(ForeignKey("showtimes.id"))
    customer_name: Mapped[str] = mapped_column(String(100))
    customer_email: Mapped[str] = mapped_column(String(150))
    customer_phone: Mapped[str] = mapped_column(String(30))
    total_price: Mapped[int]
    status: Mapped[str] = mapped_column(String(20), default="pending") 
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    showtime: Mapped["Showtime"] = relationship()
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    payment: Mapped["Payment"] = relationship(back_populates="order", uselist=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (UniqueConstraint("showtime_id", "seat_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    showtime_id: Mapped[int] = mapped_column(ForeignKey("showtimes.id"))
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"))
    price: Mapped[int]
    order: Mapped["Order"] = relationship(back_populates="items")
    seat: Mapped["Seat"] = relationship()

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), unique=True)
    method: Mapped[str] = mapped_column(String(20))
    amount: Mapped[int]
    status: Mapped[str] = mapped_column(String(20), default="success")
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    order: Mapped["Order"] = relationship(back_populates="payment") 