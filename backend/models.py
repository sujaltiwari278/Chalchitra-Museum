from sqlalchemy import Column, Integer, String, Text, Float, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Many-to-many: movies <-> people (cast/crew) with a role
movie_cast = Table(
    "movie_cast", Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("person_id", ForeignKey("people.id"), primary_key=True),
    Column("role", String, primary_key=True),  # actor, director, writer, music, cinematographer
)

# Many-to-many: movies <-> film festivals, with selection type
festival_selection = Table(
    "festival_selection", Base.metadata,
    Column("festival_id", ForeignKey("film_festivals.id"), primary_key=True),
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("selection_type", String),  # In Competition, Official Selection, Winner
)

class Studio(Base):
    __tablename__ = "studios"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    founded_year = Column(Integer)
    bio = Column(Text)
    logo_url = Column(String)

    movies = relationship("Movie", back_populates="studio")

class FilmFestival(Base):
    __tablename__ = "film_festivals"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    founded_year = Column(Integer)
    location = Column(String)
    bio = Column(Text)

    movies = relationship("Movie", secondary=festival_selection, back_populates="festivals")


class TriviaCard(Base):
    __tablename__ = "trivia_cards"
    id = Column(Integer, primary_key=True)
    fact = Column(Text, nullable=False)
    category = Column(String, index=True)  # Casting, Production, Awards, Historical, Censorship
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=True)

    movie = relationship("Movie")

class ArchiveItem(Base):
    __tablename__ = "archive_items"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    image_url = Column(String)
    category = Column(String, index=True)  # Photograph, Document, Interview, Poster
    year = Column(Integer)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    original_title = Column(String)
    language = Column(String, index=True)
    release_year = Column(Integer, index=True)
    release_date = Column(Date)
    era = Column(String, index=True)  # Silent Era, Golden Age, Parallel Cinema, etc
    genre = Column(String, index=True)
    runtime_minutes = Column(Integer)
    synopsis = Column(Text)
    poster_url = Column(String)
    backdrop_url = Column(String)
    budget_inr = Column(Float)
    box_office_inr = Column(Float)
    trivia = Column(Text)
    studio_id = Column(Integer, ForeignKey("studios.id"), nullable=True)

    people = relationship("Person", secondary=movie_cast, back_populates="movies")
    studio = relationship("Studio", back_populates="movies")
    festivals = relationship("FilmFestival", secondary=festival_selection, back_populates="movies")
    

class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    gender = Column(String, index=True)  # M, F, Other - used to split actor/actress listings
    bio = Column(Text)
    photo_url = Column(String)
    birth_date = Column(Date)

    movies = relationship("Movie", secondary=movie_cast, back_populates="people")
    
