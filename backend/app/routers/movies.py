from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models as m
from ..database import get_db

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.get("/")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(m.Movie).filter(m.Movie.is_active == True).all()
    result = []
    for movie in movies:
        st = None
        if movie.showtimes:
            sorted_st = sorted(movie.showtimes, key=lambda x: x.start_time)
            first_st = sorted_st[0]
            st = {
                "id": first_st.id,
                "start_time": first_st.start_time.isoformat() if first_st.start_time else None,
                "price": first_st.price,
                "studio": first_st.studio.name if first_st.studio else "Studio 1"
            }
        result.append({
            "id": movie.id,
            "title": movie.title,
            "genre": movie.genre,
            "duration_minutes": movie.duration_minutes,
            "poster_url": movie.poster_url,
            "showtime": st
        })
    return result

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