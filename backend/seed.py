import random
from datetime import datetime, timedelta
from app import models as m
from app.database import Base, SessionLocal, engine


FILMS = [
    {"Dilan 1990","Romance, Drama", 128, "13+"},
    {"Ada Apa Dengan Cinta?","Romance, Drama", 117, "13+"},
    {"Laskar Pelangi","Drama", 124, "SU"},
    {"Ayat-Ayat Cinta","Romance", 126, "13+"},
    {"Habibie & Ainun","Biography, Drama", 123, "13+"},
    {"Koala Kumal","Comedy, Romance", 116, "13+"},
]

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(m.Movie).count:
        print("Seeding database...")
        return
    
    print("Creating Studios...")
    
    studios = []
    for i in (1,2):
        studio = m.Studio(name=f"Studio {i}", total_rows=8,seats_per_row=10)
        for row in "ABCDEFGH":
            for number in range(1,11):
                studio.seats.append(m.Seat(row_label=row,seat_number=number))
        studios.append(studio)
    db.add_all(studios)
    
    movies = []
    for idx, (title, genre, minutes, rating) in enumerate(FILMS, start=1):
        movies.append(
            m.Movie(
                title=title,
                genre=genre,
                duration_minutes=minutes,
                rating=rating,
                synopsis=f"Sinopsis film {title}",
                poster_url=f"https://picsum.photos/seed/{idx}/600/900",
            )
        )
    db.add_all(movies)
    db.flush()

    today = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)

    for idx, movie in enumerate(movies):
        for day in range(0,3):
            for hour in (13,16,19,21):
                db.add(
                    m.Showtime(
                        movie_id=movies.id,
                        studio_id=studios[idx % 2].id,
                        start_time=today + timedelta(days=day,hours=hour),
                        price=random.choice([45000,55000,65000])
                    )
                )
    db.commit()
    print("Seeding completed.")

if __name__ == "__main__":
    seed()