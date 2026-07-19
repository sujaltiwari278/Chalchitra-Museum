"""
Import real Indian movies from TMDb (The Movie Database) into cinema.db.

SETUP:
1. Get a free API key: themoviedb.org -> Settings -> API -> request Developer key
2. Set it below or as an environment variable TMDB_API_KEY
3. Run:  python import_tmdb.py --pages 5
   (each page = ~20 movies, so --pages 5 imports ~100 movies)

This is separate from seed.py - it ADDS to whatever is already in the database
rather than replacing it. Safe to re-run; it skips movies already imported.
"""

import os
import sys
import time
import argparse
import requests

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

API_KEY = os.environ.get("TMDB_API_KEY", "PASTE_YOUR_KEY_HERE")
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"

# Approximate USD -> INR for display purposes only (TMDb budget/revenue are in USD)
USD_TO_INR = 83

LANGUAGE_MAP = {
    "hi": "Hindi", "ta": "Tamil", "te": "Telugu", "ml": "Malayalam",
    "kn": "Kannada", "bn": "Bengali", "mr": "Marathi", "pa": "Punjabi",
    "gu": "Gujarati", "ur": "Urdu", "or": "Odia", "as": "Assamese",
}

def era_for_year(year):
    if not year:
        return None
    if year < 1931:
        return "Silent Era"
    if year < 1947:
        return "Talkies"
    if year < 1990:
        return "Golden Age"
    if year < 2010:
        return "Modern Cinema"
    if year < 2020:
        return "Pan India Cinema"
    return "OTT Revolution"

def api_get(path, params=None):
    params = params or {}
    params["api_key"] = API_KEY
    last_error = None
    for attempt in range(4):
        try:
            r = requests.get(f"{BASE_URL}{path}", params=params, timeout=15)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            last_error = e
            time.sleep(1.5 * (attempt + 1))
    raise last_error

def get_genre_map():
    data = api_get("/genre/movie/list")
    return {g["id"]: g["name"] for g in data.get("genres", [])}

def discover_movies(page):
    data = api_get("/discover/movie", {
        "with_origin_country": "IN",
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "page": page,
    })
    return data.get("results", [])

def get_movie_details(movie_id):
    return api_get(f"/movie/{movie_id}", {"append_to_response": "credits"})

def get_or_create_person(db, name, gender_hint=None, photo_url=None):
    person = db.query(models.Person).filter(models.Person.name == name).first()
    if person:
        if photo_url and not person.photo_url:
            person.photo_url = photo_url
        return person
    person = models.Person(name=name, gender=gender_hint, photo_url=photo_url)
    db.add(person)
    db.flush()
    return person

def link_credit(db, movie, person, role):
    exists = db.execute(
        models.movie_cast.select().where(
            (models.movie_cast.c.movie_id == movie.id)
            & (models.movie_cast.c.person_id == person.id)
            & (models.movie_cast.c.role == role)
        )
    ).first()
    if not exists:
        db.execute(models.movie_cast.insert().values(
            movie_id=movie.id, person_id=person.id, role=role
        ))

def import_movie(db, tmdb_data, genre_map):
    title = tmdb_data.get("title") or tmdb_data.get("original_title")
    if not title:
        return False

    existing = db.query(models.Movie).filter(models.Movie.title == title).first()
    if existing:
        return False  # already imported, skip

    release_date = tmdb_data.get("release_date") or None
    release_year = int(release_date[:4]) if release_date else None
    lang_code = tmdb_data.get("original_language")
    genre_ids = tmdb_data.get("genre_ids") or [g["id"] for g in tmdb_data.get("genres", [])]
    genre_name = genre_map.get(genre_ids[0]) if genre_ids else None

    budget = tmdb_data.get("budget") or 0
    revenue = tmdb_data.get("revenue") or 0

    movie = models.Movie(
        title=title,
        original_title=tmdb_data.get("original_title"),
        language=LANGUAGE_MAP.get(lang_code, lang_code),
        release_year=release_year,
        era=era_for_year(release_year),
        genre=genre_name,
        runtime_minutes=tmdb_data.get("runtime"),
        synopsis=tmdb_data.get("overview"),
        poster_url=f"{IMG_BASE}{tmdb_data['poster_path']}" if tmdb_data.get("poster_path") else None,
        backdrop_url=f"{BACKDROP_BASE}{tmdb_data['backdrop_path']}" if tmdb_data.get("backdrop_path") else None,
        budget_inr=budget * USD_TO_INR if budget else None,
        box_office_inr=revenue * USD_TO_INR if revenue else None,
    )
    db.add(movie)
    db.flush()

    credits = tmdb_data.get("credits", {})
    for cast_member in credits.get("cast", [])[:6]:
        photo = f"{IMG_BASE}{cast_member['profile_path']}" if cast_member.get("profile_path") else None
        person = get_or_create_person(db, cast_member["name"], gender_hint=(
            "F" if cast_member.get("gender") == 1 else "M" if cast_member.get("gender") == 2 else None
        ), photo_url=photo)
        link_credit(db, movie, person, "actor")

    for crew_member in credits.get("crew", []):
        job = crew_member.get("job")
        role = {
            "Director": "director",
            "Writer": "writer",
            "Screenplay": "writer",
            "Original Music Composer": "music",
            "Director of Photography": "cinematographer",
        }.get(job)
        if role:
            photo = f"{IMG_BASE}{crew_member['profile_path']}" if crew_member.get("profile_path") else None
            person = get_or_create_person(db, crew_member["name"], photo_url=photo)
            link_credit(db, movie, person, role)

    return True

def main():
    if API_KEY == "PASTE_YOUR_KEY_HERE":
        print("ERROR: Set your TMDb API key at the top of this file, or via TMDB_API_KEY env var.")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=3, help="Number of discover pages (~20 movies each)")
    args = parser.parse_args()

    db = SessionLocal()
    genre_map = get_genre_map()

    imported = 0
    for page in range(1, args.pages + 1):
        print(f"Fetching page {page}...")
        results = discover_movies(page)
        for r in results:
            try:
                details = get_movie_details(r["id"])
                if import_movie(db, details, genre_map):
                    imported += 1
                    print(f"  + {details.get('title')}")
            except Exception as e:
                print(f"  ! movie id {r['id']} - failed after retries: {e}")
                db.rollback()
            db.commit()
            time.sleep(0.25)  # be polite to the API

    db.close()
    print(f"\nDone. Imported {imported} new movies.")

if __name__ == "__main__":
    main()
