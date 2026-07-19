"""
Import a curated canon of ~150 Indian films into cinema.db:
  - 110 influential Hindi films (spanning 1940s-2020s)
  - 10 Hindi silent-era films (1913-1929) - added manually, TMDb has no data this old
  - 10 Kannada films
  - 10 Bengali films (Ray/Ghatak canon)
  - 10 Telugu films (classic + modern)

Unlike import_tmdb.py (which pulls by popularity), this searches TMDb for each
SPECIFIC title+year on the curated list below, so you get exactly these films,
not whatever TMDb ranks highest.

SETUP: same as import_tmdb.py - paste your TMDb API key below or set TMDB_API_KEY.
RUN:   python import_curated.py
Safe to re-run - skips movies already in the database.
"""

import os
import sys
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

API_KEY = os.environ.get(
    "TMDB_API_KEY",
    "26d32a42fbc35ee52c2c6705c404a691"
)
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"
USD_TO_INR = 83

# ---------- HTTP Session with Automatic Retries ----------

session = requests.Session()

retry = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)

adapter = HTTPAdapter(max_retries=retry)

session.mount("https://", adapter)
session.mount("http://", adapter)

LANGUAGE_MAP = {
    "hi": "Hindi", "ta": "Tamil", "te": "Telugu", "ml": "Malayalam",
    "kn": "Kannada", "bn": "Bengali", "mr": "Marathi", "pa": "Punjabi",
    "gu": "Gujarati", "ur": "Urdu",
}

def era_for_year(year):
    if not year:
        return None
    if year < 1931: return "Silent Era"
    if year < 1947: return "Talkies"
    if year < 1990: return "Golden Age"
    if year < 2010: return "Modern Cinema"
    if year < 2020: return "Pan India Cinema"
    return "OTT Revolution"

def api_get(path, params=None):
    params = params or {}
    params["api_key"] = API_KEY

    response = session.get(
        f"{BASE_URL}{path}",
        params=params,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()

def get_genre_map():
    data = api_get("/genre/movie/list")
    return {g["id"]: g["name"] for g in data.get("genres", [])}

INDIAN_LANG_CODES = {"hi", "ta", "te", "ml", "kn", "bn", "mr", "pa", "gu", "ur"}

def search_movie(title, year):
    data = api_get("/search/movie", {"query": title, "year": year, "include_adult": "false"})
    results = data.get("results", [])
    if not results:
        return None
    for r in results:
        if r.get("original_language") in INDIAN_LANG_CODES:
            return r
    return results[0]  # fallback if no Indian-language match found

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
        db.execute(models.movie_cast.insert().values(movie_id=movie.id, person_id=person.id, role=role))

def import_from_tmdb(db, title, year, genre_map):
    if db.query(models.Movie).filter(models.Movie.title == title).first():
        print(f"  = {title} (already in DB, skipped)")
        return False

    hit = search_movie(title, year)
    if not hit:
        print(f"  ! {title} ({year}) - not found on TMDb, skipping")
        return False

    details = get_movie_details(hit["id"])
    release_date = details.get("release_date") or None
    release_year = int(release_date[:4]) if release_date else year
    lang_code = details.get("original_language")
    genres = details.get("genres", [])
    genre_name = genres[0]["name"] if genres else None
    budget = details.get("budget") or 0
    revenue = details.get("revenue") or 0

    movie = models.Movie(
        title=title,
        original_title=details.get("original_title"),
        language=LANGUAGE_MAP.get(lang_code, lang_code),
        release_year=release_year,
        era=era_for_year(release_year),
        genre=genre_name,
        runtime_minutes=details.get("runtime"),
        synopsis=details.get("overview"),
        poster_url=f"{IMG_BASE}{details['poster_path']}" if details.get("poster_path") else None,
        backdrop_url=f"{BACKDROP_BASE}{details['backdrop_path']}" if details.get("backdrop_path") else None,
        budget_inr=budget * USD_TO_INR if budget else None,
        box_office_inr=revenue * USD_TO_INR if revenue else None,
    )
    db.add(movie)
    db.flush()

    credits = details.get("credits", {})
    for cast_member in credits.get("cast", [])[:6]:
        photo = f"{IMG_BASE}{cast_member['profile_path']}" if cast_member.get("profile_path") else None
        person = get_or_create_person(db, cast_member["name"], gender_hint=(
            "F" if cast_member.get("gender") == 1 else "M" if cast_member.get("gender") == 2 else None
        ), photo_url=photo)
        link_credit(db, movie, person, "actor")
    for crew_member in credits.get("crew", []):
        role = {
            "Director": "director", "Writer": "writer", "Screenplay": "writer",
            "Original Music Composer": "music", "Director of Photography": "cinematographer",
        }.get(crew_member.get("job"))
        if role:
            photo = f"{IMG_BASE}{crew_member['profile_path']}" if crew_member.get("profile_path") else None
            person = get_or_create_person(db, crew_member["name"], photo_url=photo)
            link_credit(db, movie, person, role)

    print(f"  + {title} ({release_year})")
    return True

def import_silent_manual(db, title, year, director, synopsis):
    if db.query(models.Movie).filter(models.Movie.title == title).first():
        print(f"  = {title} (already in DB, skipped)")
        return False
    movie = models.Movie(
        title=title, language="Hindi (Silent)", release_year=year,
        era="Silent Era", genre="Mythological/Historical", synopsis=synopsis,
    )
    db.add(movie)
    db.flush()
    if director:
        person = get_or_create_person(db, director)
        link_credit(db, movie, person, "director")
    print(f"  + {title} ({year}) [manual - pre-dates TMDb coverage]")
    return True

# ============ THE CURATED LIST ============

HINDI_INFLUENTIAL = [
    ("Kismet", 1943), ("Do Bigha Zamin", 1953), ("Awaara", 1951), ("Shree 420", 1955),
    ("Pyaasa", 1957), ("Mughal-E-Azam", 1960), ("Guide", 1965), ("Waqt", 1965),
    ("Sangam", 1964), ("Bandini", 1963), ("Naya Daur", 1957), ("Madhumati", 1958),
    ("Kaagaz Ke Phool", 1959), ("Sahib Bibi Aur Ghulam", 1962), ("Anupama", 1966),
    ("Teesri Kasam", 1966), ("Aradhana", 1969), ("Padosan", 1968), ("Anand", 1971),
    ("Zanjeer", 1973), ("Deewar", 1975), ("Amar Akbar Anthony", 1977), ("Trishul", 1978),
    ("Don", 1978), ("Kabhi Kabhie", 1976), ("Silsila", 1981), ("Karz", 1980),
    ("Namak Haraam", 1973), ("Abhimaan", 1973), ("Chupke Chupke", 1975), ("Golmaal", 1979),
    ("Angoor", 1982), ("Jaane Bhi Do Yaaro", 1983), ("Ardh Satya", 1983), ("Arth", 1982),
    ("Masoom", 1983), ("Umrao Jaan", 1981), ("Mirch Masala", 1987),
    ("Ijaazat", 1987), ("Ram Lakhan", 1989), ("Maine Pyar Kiya", 1989),
    ("Qayamat Se Qayamat Tak", 1988), ("Mr. India", 1987),
    ("Dilwale Dulhania Le Jayenge", 1995), ("Hum Aapke Hain Koun", 1994),
    ("Rangeela", 1995), ("Dil To Pagal Hai", 1997), ("Kuch Kuch Hota Hai", 1998),
    ("Satya", 1998), ("Bandit Queen", 1994), ("Darr", 1993), ("Baazigar", 1993),
    ("Lamhe", 1991), ("Border", 1997), ("Dil Se", 1998),
    ("Kaho Naa Pyaar Hai", 2000), ("Lagaan", 2001), ("Dil Chahta Hai", 2001),
    ("Devdas", 2002), ("Kal Ho Naa Ho", 2003), ("Munna Bhai MBBS", 2003),
    ("Swades", 2004), ("Black", 2005), ("Rang De Basanti", 2006),
    ("Lage Raho Munna Bhai", 2006), ("Taare Zameen Par", 2007), ("Om Shanti Om", 2007),
    ("Jab We Met", 2007), ("A Wednesday", 2008), ("Chak De! India", 2007),
    ("3 Idiots", 2009),
    ("My Name Is Khan", 2010), ("Zindagi Na Milegi Dobara", 2011), ("Kahaani", 2012),
    ("Barfi!", 2012), ("Gangs of Wasseypur", 2012), ("Vicky Donor", 2012),
    ("English Vinglish", 2012), ("Queen", 2014), ("Highway", 2014), ("PK", 2014),
    ("Bajrangi Bhaijaan", 2015), ("Piku", 2015), ("Masaan", 2015),
    ("Bajirao Mastani", 2015), ("Neerja", 2016), ("Udta Punjab", 2016),
    ("Pink", 2016), ("Dangal", 2016), ("Newton", 2017), ("Andhadhun", 2018),
    ("Gully Boy", 2019), ("Article 15", 2019), ("Uri: The Surgical Strike", 2019),
    ("Kabir Singh", 2019), ("War", 2019), ("Chhichhore", 2019), ("Badhaai Ho", 2018),
    ("Raazi", 2018), ("Stree", 2018),
    ("Tanhaji: The Unsung Warrior", 2020), ("Thappad", 2020), ("Shershaah", 2021),
    ("83", 2021), ("Gangubai Kathiawadi", 2022), ("Drishyam 2", 2022),
    ("12th Fail", 2023), ("Animal", 2023), ("Jawan", 2023), ("Pathaan", 2023),
    ("Dabangg", 2010), ("Tere Naam", 2003),
    ("Dhurandhar", 2025), ("Dhurandhar: The Revenge", 2026),
]

HINDI_SILENT = [
    ("Mohini Bhasmasur", 1913, "Dadasaheb Phalke", "One of Phalke's earliest mythological silent films, following Raja Harishchandra."),
    ("Satyavan Savitri", 1914, "Dadasaheb Phalke", "An early Phalke mythological silent film based on the legend of Savitri and Satyavan."),
    ("Lanka Dahan", 1917, "Dadasaheb Phalke", "Dramatizes Hanuman burning Lanka from the Ramayana; became India's first major box-office hit."),
    ("Kaliya Mardan", 1919, "Dadasaheb Phalke", "A mythological silent film depicting young Krishna subduing the serpent Kaliya."),
    ("Shakuntala", 1920, "Suchet Singh", "A silent adaptation of Kalidasa's classic tale of King Dushyanta and Shakuntala."),
    ("Bhakta Vidur", 1921, "Kanjibhai Rathod", "Based on the Mahabharata; notable as the first Indian film to face censorship and a ban."),
    ("Savkari Pash", 1925, "Baburao Painter", "A landmark early social-realist silent film about a farmer's ruin at the hands of a moneylender."),
    ("Prem Sanyas (Light of Asia)", 1925, "Himanshu Rai", "An Indo-German co-production dramatizing the life of the Buddha."),
    ("A Throw of Dice", 1929, "Franz Osten", "An epic silent film about two rival kings gambling for a kingdom and a woman's hand."),
]

KANNADA_MOVIES = [
    ("Kantara", 2022), ("KGF: Chapter 1", 2018), ("Lucia", 2013), ("U-Turn", 2016),
    ("Godhi Banna Sadharana Mykattu", 2016), ("777 Charlie", 2022), ("Mayura", 1975),
    ("Bandhana", 1984), ("Nagarahavu", 1972), ("Rangitaranga", 2015),
]

BENGALI_MOVIES = [
    ("Pather Panchali", 1955), ("Aparajito", 1956), ("Apur Sansar", 1959),
    ("Jalsaghar", 1958), ("Charulata", 1964), ("Nayak", 1966),
    ("Meghe Dhaka Tara", 1960), ("Subarnarekha", 1965),
    ("Goopy Gyne Bagha Byne", 1969), ("Ghare Baire", 1984),
]

TELUGU_MOVIES = [
    ("Mayabazar", 1957), ("Missamma", 1955), ("Pathala Bhairavi", 1951),
    ("Devadasu", 1953), ("Lava Kusa", 1963), ("Sankarabharanam", 1980),
    ("Sagara Sangamam", 1983), ("Pushpaka Vimana", 1987), ("Magadheera", 2009),
    ("Baahubali 2: The Conclusion", 2017),
]

def main():
    if not API_KEY:
        print("ERROR: TMDB_API_KEY not set.")
        sys.exit(1)

    db = SessionLocal()
    genre_map = get_genre_map()
    imported = 0

    print(f"\n=== Hindi Silent Era ({len(HINDI_SILENT)} films, manual entry) ===")
    for title, year, director, synopsis in HINDI_SILENT:
        if import_silent_manual(db, title, year, director, synopsis):
            imported += 1
        db.commit()

    for label, movie_list in [
        ("Hindi Influential", HINDI_INFLUENTIAL),
        ("Kannada", KANNADA_MOVIES),
        ("Bengali", BENGALI_MOVIES),
        ("Telugu", TELUGU_MOVIES),
    ]:
        print(f"\n=== {label} ({len(movie_list)} films, via TMDb) ===")
        for title, year in movie_list:
            try:
                if import_from_tmdb(db, title, year, genre_map):
                    imported += 1
                db.commit()

            except Exception as e:
                db.rollback()
                print(f"FAILED: {title} ({year})")
                print(e)

            time.sleep(1)

    db.close()
    total = len(HINDI_SILENT) + len(HINDI_INFLUENTIAL) + len(KANNADA_MOVIES) + len(BENGALI_MOVIES) + len(TELUGU_MOVIES)
    print(f"\nDone. Imported {imported} new movies out of {total} on the curated list.")
    print("(Some may show as 'not found' if TMDb's title/year match differs slightly - re-run is safe.)")

if __name__ == "__main__":
    main()