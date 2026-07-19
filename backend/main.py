from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chalchitra Museum API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Chalchitra Museum API"}

# ---------- MOVIES ----------

@app.get("/api/movies", response_model=List[schemas.MovieCard])
def list_movies(
    db: Session = Depends(get_db),
    language: Optional[str] = None,
    era: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    skip: int = 0,
    limit: int = 1000,
):
    q = db.query(models.Movie)
    if language:
        q = q.filter(models.Movie.language == language)
    if era:
        q = q.filter(models.Movie.era == era)
    if genre:
        q = q.filter(models.Movie.genre == genre)
    if year:
        q = q.filter(models.Movie.release_year == year)
    return q.order_by(models.Movie.release_year.desc()).offset(skip).limit(limit).all()

@app.get("/api/search/all")
def search_all(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    like = f"%{q}%"
    movies = db.query(models.Movie).filter(
        or_(models.Movie.title.ilike(like), models.Movie.original_title.ilike(like))
    ).limit(6).all()
    people = db.query(models.Person).filter(models.Person.name.ilike(like)).limit(6).all()
    return {
        "movies": [{"id": m.id, "title": m.title, "release_year": m.release_year} for m in movies],
        "people": [{"id": p.id, "name": p.name} for p in people],
    }
@app.get("/api/movies/{movie_id}", response_model=schemas.MovieDetail)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# ---------- SEARCH (Phase 3) ----------

@app.get("/api/search", response_model=List[schemas.MovieCard])
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    like = f"%{q}%"
    return db.query(models.Movie).filter(
        or_(models.Movie.title.ilike(like), models.Movie.original_title.ilike(like))
    ).limit(30).all()

# ---------- PEOPLE ----------

VALID_ROLES = {"actor", "director", "writer", "music", "cinematographer"}

@app.get("/api/people", response_model=List[schemas.PersonOut])
def list_people(
    db: Session = Depends(get_db),
    role: Optional[str] = None,
    gender: Optional[str] = None,
):
    q = db.query(models.Person)
    if role:
        if role not in VALID_ROLES:
            raise HTTPException(status_code=400, detail=f"role must be one of {sorted(VALID_ROLES)}")
        q = q.join(models.movie_cast).filter(models.movie_cast.c.role == role).distinct()
    if gender:
        q = q.filter(models.Person.gender == gender)
    return q.order_by(models.Person.name).all()

@app.get("/api/people/{person_id}", response_model=schemas.PersonDetail)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    credits = (
        db.query(models.Movie, models.movie_cast.c.role)
        .join(models.movie_cast, models.Movie.id == models.movie_cast.c.movie_id)
        .filter(models.movie_cast.c.person_id == person_id)
        .all()
    )
    filmography = [
        {"id": m.id, "title": m.title, "release_year": m.release_year,
         "poster_url": m.poster_url, "role": role}
        for m, role in credits
    ]
    return {
        "id": person.id, "name": person.name, "gender": person.gender,
        "bio": person.bio, "photo_url": person.photo_url, "filmography": filmography,
    }

# ---------- STUDIOS ----------

@app.get("/api/studios", response_model=List[schemas.StudioCard])
def list_studios(db: Session = Depends(get_db)):
    return db.query(models.Studio).order_by(models.Studio.name).all()

@app.get("/api/studios/{studio_id}", response_model=schemas.StudioDetail)
def get_studio(studio_id: int, db: Session = Depends(get_db)):
    studio = db.query(models.Studio).filter(models.Studio.id == studio_id).first()
    if not studio:
        raise HTTPException(status_code=404, detail="Studio not found")
    return studio


# ---------- FILM FESTIVALS ----------

@app.get("/api/film-festivals", response_model=List[schemas.FilmFestivalCard])
def list_festivals(db: Session = Depends(get_db)):
    return db.query(models.FilmFestival).order_by(models.FilmFestival.name).all()

@app.get("/api/film-festivals/{festival_id}", response_model=schemas.FilmFestivalDetail)
def get_festival(festival_id: int, db: Session = Depends(get_db)):
    festival = db.query(models.FilmFestival).filter(models.FilmFestival.id == festival_id).first()
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")

    rows = (
        db.query(models.Movie, models.festival_selection.c.selection_type)
        .join(models.festival_selection, models.Movie.id == models.festival_selection.c.movie_id)
        .filter(models.festival_selection.c.festival_id == festival_id)
        .all()
    )
    selections = [
        {"id": m.id, "title": m.title, "release_year": m.release_year, "selection_type": sel}
        for m, sel in rows
    ]
    return {
        "id": festival.id, "name": festival.name, "founded_year": festival.founded_year,
        "location": festival.location, "bio": festival.bio, "selections": selections,
    }

# ---------- TRIVIA ----------

@app.get("/api/trivia", response_model=List[schemas.TriviaOut])
def list_trivia(db: Session = Depends(get_db), category: Optional[str] = None):
    q = db.query(models.TriviaCard)
    if category:
        q = q.filter(models.TriviaCard.category == category)
    cards = q.all()
    return [
        {"id": c.id, "fact": c.fact, "category": c.category,
         "movie_title": c.movie.title if c.movie else None, "movie_id": c.movie_id}
        for c in cards
    ]

@app.get("/api/meta/trivia-categories")
def trivia_categories(db: Session = Depends(get_db)):
    rows = db.query(models.TriviaCard.category).distinct().all()
    return sorted({r[0] for r in rows if r[0]})

# ---------- ARCHIVES ----------

@app.get("/api/archives", response_model=List[schemas.ArchiveItemOut])
def list_archives(db: Session = Depends(get_db), category: Optional[str] = None):
    q = db.query(models.ArchiveItem)
    if category:
        q = q.filter(models.ArchiveItem.category == category)
    return q.order_by(models.ArchiveItem.year).all()

@app.get("/api/meta/languages")
def languages(db: Session = Depends(get_db)):
    rows = db.query(models.Movie.language).distinct().all()
    return sorted({r[0] for r in rows if r[0]})

@app.get("/api/meta/eras")
def eras(db: Session = Depends(get_db)):
    rows = db.query(models.Movie.era).distinct().all()
    return sorted({r[0] for r in rows if r[0]})

@app.get("/api/meta/genres")
def genres(db: Session = Depends(get_db)):
    rows = db.query(models.Movie.genre).distinct().all()
    return sorted({r[0] for r in rows if r[0]})

@app.get("/api/box-office")
def box_office(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).filter(models.Movie.box_office_inr.isnot(None)).order_by(models.Movie.box_office_inr.desc()).all()
    return [
        {"id": m.id, "title": m.title, "release_year": m.release_year,
         "budget_inr": m.budget_inr, "box_office_inr": m.box_office_inr}
        for m in movies
    ]