"""
Removes confirmed foreign-film TMDb mismatches (found via check_foreign.py)
and cleans up any linked movie_cast, trivia, award, or festival rows so
nothing is left orphaned.
RUN: python remove_foreign.py
"""
from database import SessionLocal
import models

BAD_IDS = [75, 39, 91, 122, 106]  # Black, Don, Highway, Lucia, War (foreign mismatches)

db = SessionLocal()

for mid in BAD_IDS:
    m = db.query(models.Movie).filter(models.Movie.id == mid).first()
    if not m:
        print(f"  id={mid} - not found, skipping")
        continue
    title = m.title

    db.execute(models.movie_cast.delete().where(models.movie_cast.c.movie_id == mid))
    db.execute(models.festival_selection.delete().where(models.festival_selection.c.movie_id == mid))
    db.query(models.TriviaCard).filter(models.TriviaCard.movie_id == mid).delete()
    db.query(models.Award).filter(models.Award.movie_id == mid).delete()
    db.delete(m)
    print(f'  removed id={mid} "{title}"')

db.commit()
db.close()
print("\nDone. Re-run import_curated.py to re-fetch the correct Indian versions of these titles.")