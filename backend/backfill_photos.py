"""
One-time backfill: adds a TMDb profile photo for any Person already in the
database who doesn't have one yet (e.g. the 13 people from seed.py, which
predates photo support). Safe to re-run - only touches people missing a photo.

SETUP: same API key as the other import scripts.
RUN:   python backfill_photos.py
"""
import os
import sys
import time
import requests

from database import SessionLocal
import models

API_KEY = os.environ.get("TMDB_API_KEY", "PASTE_YOUR_KEY_HERE")
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

def search_person_photo(name):
    last_error = None
    for attempt in range(4):
        try:
            r = requests.get(f"{BASE_URL}/search/person", params={"api_key": API_KEY, "query": name}, timeout=15)
            r.raise_for_status()
            results = r.json().get("results", [])
            if results and results[0].get("profile_path"):
                return f"{IMG_BASE}{results[0]['profile_path']}"
            return None
        except requests.exceptions.RequestException as e:
            last_error = e
            time.sleep(1.5 * (attempt + 1))
    print(f"    (network error after retries: {last_error})")
    return None

def main():
    if API_KEY == "PASTE_YOUR_KEY_HERE":
        print("ERROR: Set your TMDb API key at the top of this file, or via TMDB_API_KEY env var.")
        sys.exit(1)

    db = SessionLocal()
    people = db.query(models.Person).filter(models.Person.photo_url.is_(None)).all()
    print(f"Found {len(people)} people without a photo.")

    updated = 0
    for p in people:
        photo = search_person_photo(p.name)
        if photo:
            p.photo_url = photo
            updated += 1
            print(f"  + {p.name}")
        else:
            print(f"  ! {p.name} - no TMDb photo found")
        db.commit()
        time.sleep(0.25)

    db.close()
    print(f"\nDone. Added photos for {updated} of {len(people)} people.")

if __name__ == "__main__":
    main()