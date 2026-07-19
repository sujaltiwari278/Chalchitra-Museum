"""
Finds movies in the database whose language isn't a recognized Indian language -
these are almost always TMDb title-collision mismatches (e.g. searching "War" (2019)
matched an unrelated foreign film also titled "War").

Run: python check_foreign.py
This only REPORTS - it doesn't delete anything. Review the list, then tell me
which ids to remove and I'll write the exact delete script.
"""
from database import SessionLocal
import models

INDIAN_LANGUAGES = {
    "Hindi", "Hindi (Silent)", "Tamil", "Telugu", "Malayalam", "Kannada",
    "Bengali", "Marathi", "Punjabi", "Gujarati", "Urdu", "Odia", "Assamese",
}

db = SessionLocal()
movies = db.query(models.Movie).order_by(models.Movie.title).all()

suspects = [m for m in movies if m.language not in INDIAN_LANGUAGES]

if not suspects:
    print(f"No suspicious entries found. All {len(movies)} movies have recognized Indian languages.")
else:
    print(f"Found {len(suspects)} movies with an unrecognized language (likely TMDb mismatches):\n")
    for m in suspects:
        print(f'  id={m.id}  title="{m.title}"  year={m.release_year}  language="{m.language}"  genre={m.genre}')
    print("\nReview this list. If any are genuinely wrong (e.g. a foreign film matched")
    print("by title collision), tell me the ids and I'll remove them cleanly.")

db.close()
