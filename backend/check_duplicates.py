"""
Find duplicate movie titles in cinema.db.
Run: python check_duplicates.py
"""
from database import SessionLocal
import models

db = SessionLocal()
movies = db.query(models.Movie).order_by(models.Movie.title).all()

seen = {}
for m in movies:
    seen.setdefault(m.title, []).append(m)

duplicates = {title: rows for title, rows in seen.items() if len(rows) > 1}

if not duplicates:
    print(f"No duplicate titles found. Total movies: {len(movies)}")
else:
    print(f"Found {len(duplicates)} duplicated titles out of {len(movies)} total movies:\n")
    for title, rows in duplicates.items():
        print(f'"{title}" appears {len(rows)} times:')
        for r in rows:
            print(f"  id={r.id}  year={r.release_year}  language={r.language}  poster={'yes' if r.poster_url else 'no'}")
        print()

db.close()