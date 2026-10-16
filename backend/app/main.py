import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import movies, showtimes, orders

app = FastAPI(title="Cinema Booking API")

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(showtimes.router)
app.include_router(orders.router)

@app.get("/")
def health():
    return {"status":"ok"}