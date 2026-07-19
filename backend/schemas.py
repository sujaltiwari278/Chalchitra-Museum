from pydantic import BaseModel
from typing import Optional, List

class PersonOut(BaseModel):
    id: int
    name: str
    photo_url: Optional[str] = None
    class Config:
        from_attributes = True

class FilmCredit(BaseModel):
    id: int
    title: str
    release_year: Optional[int]
    poster_url: Optional[str]
    role: str

class PersonDetail(BaseModel):
    id: int
    name: str
    gender: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    filmography: List[FilmCredit] = []
    class Config:
        from_attributes = True

class StudioCard(BaseModel):
    id: int
    name: str
    founded_year: Optional[int]
    logo_url: Optional[str] = None
    class Config:
        from_attributes = True

class StudioDetail(StudioCard):
    bio: Optional[str] = None
    movies: List[MovieCard] = []
    class Config:
        from_attributes = True

class AwardOut(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    year: Optional[int] = None
    winner: Optional[str] = None
    movie_title: Optional[str] = None
    movie_id: Optional[int] = None
    person_name: Optional[str] = None
    person_id: Optional[int] = None

class FestivalCredit(BaseModel):
    id: int
    title: str
    release_year: Optional[int]
    selection_type: str

class FilmFestivalCard(BaseModel):
    id: int
    name: str
    founded_year: Optional[int]
    location: Optional[str] = None
    class Config:
        from_attributes = True

class FilmFestivalDetail(FilmFestivalCard):
    bio: Optional[str] = None
    selections: List[FestivalCredit] = []
    class Config:
        from_attributes = True

class TriviaOut(BaseModel):
    id: int
    fact: str
    category: Optional[str] = None
    movie_title: Optional[str] = None
    movie_id: Optional[int] = None

class ArchiveItemOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    year: Optional[int] = None
    class Config:
        from_attributes = True

class MovieCard(BaseModel):
    id: int
    title: str
    release_year: Optional[int]
    language: Optional[str]
    era: Optional[str]
    genre: Optional[str]
    poster_url: Optional[str]
    class Config:
        from_attributes = True

class MovieDetail(MovieCard):
    original_title: Optional[str]
    runtime_minutes: Optional[int]
    synopsis: Optional[str]
    backdrop_url: Optional[str]
    budget_inr: Optional[float]
    box_office_inr: Optional[float]
    trivia: Optional[str]
    people: List[PersonOut] = []
    class Config:
        from_attributes = True
