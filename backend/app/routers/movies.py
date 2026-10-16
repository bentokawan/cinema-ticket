from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models as m
from ..database import get_db

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.get("/")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(m.Movie).filter(m.Movie.is_active == True).all()
    return [
        {
            "id": movie.id,
            "title": movie.title,
            "duration_minutes": movie.duration_minutes,
            "poster_url": movie.poster_url,
            "showtimes": [
                {
                    "id": s.id,
                    "start_time": s.start_time.isoformat() if s.start_time else None,
                    "price": s.price,
                    "studio": s.studio.name if s.studio else ""
                }
                for s in sorted(movie.showtimes, key=lambda x: x.start_time)
            ]
        }
        for movie in movies
    ]

@router.get("/{movie_id}")
def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(m.Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    showtimes = [{
        "id": s.id,
        "start_time": s.start_time,
        "price": s.price,
        "studio": s.studio.name
    } for s in movie.showtimes]

    return {
        "id": movie.id,
        "title": movie.title,
        "synopsis": movie.synopsis,
        "duration_minutes": movie.duration_minutes,
        "poster_url": movie.poster_url,
        "showtimes": sorted(showtimes, key=lambda x:x["start_time"])
    }