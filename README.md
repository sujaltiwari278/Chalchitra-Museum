# Chalchitra Museum (चलचित्र संग्रहालय)
### A Digital Museum of Indian Cinema — 1913 to Present

Chalchitra Museum is a full-stack digital archive celebrating over a century of
Indian filmmaking — from Dadasaheb Phalke's silent-era debut to the OTT
revolution. It combines a curated 150-film canon across Hindi, Kannada,
Bengali, and Telugu cinema with real, live-fetched context from TMDb and
Wikipedia, presented through a themed, museum-inspired interface rather than
a typical movie database UI.

---

## Tech Stack

**Frontend:** Next.js 14 (App Router), React, Tailwind CSS
**Backend:** FastAPI, Python, SQLAlchemy, SQLite
**External APIs:** TMDb (movie/cast/crew data + posters), Wikipedia (live biographical & historical context, CC BY-SA)

---

## Features

- **150 curated films** — 110 influential Hindi films, 9 hand-entered silent-era films (pre-dating TMDb), 10 Kannada, 10 Bengali, and 10 Telugu films, each researched rather than pulled by popularity
- **People, Studios, Awards & Film Festivals** — real cast/crew with photos, production houses, and festival selections, all cross-linked to films
- **Live Wikipedia integration** — movie, person, and studio pages pull real biographical/historical summaries at request time, with proper CC BY-SA attribution
- **Global search** — live dropdown search across movies and people from any page
- **Box Office page** — the real all-time highest-grossing Indian films table, plus archive-specific rankings
- **Daily-rotating trivia** — 100 trivia cards, 10 shown per day, deterministic rotation (not random)
- **Timeline** — a curated, captioned, photo-illustrated walk through cinema milestones
- **History page** — long-form narrative across 8 eras (Silent Era → OTT Revolution), each with a real photo
- **Atmospheric homepage** — designed as a museum exhibit sequence, not a navigation dashboard

---

## Project Structure

```
cinema-museum/
├── .gitignore
├── README.md
├── backend/
│   ├── main.py                      FastAPI app & all API routes
│   ├── models.py                    SQLAlchemy models (Movie, Person, Studio, Award, FilmFestival, TriviaCard, ArchiveItem)
│   ├── schemas.py                   Pydantic response schemas
│   ├── database.py                  DB engine/session setup
│   ├── requirements.txt
│   │
│   ├── seed.py                      Base seed: 9 sample movies, people, studios, awards, trivia (idempotent)
│   ├── import_tmdb.py               Bulk-import Indian movies from TMDb by popularity
│   ├── import_curated.py            Import the curated 150-film canon (recommended)
│   ├── backfill_photos.py           Adds TMDb photos to people missing one
│   ├── seed_extra_content.py        Expands studios/awards/festivals/trivia across the full catalog
│   ├── seed_more_trivia.py          Adds trivia cards up to ~100 total
│   ├── expand_studios_festivals.py  More studios, festivals, and selections
│   ├── check_duplicates.py          Diagnostic: finds duplicate movie titles
│   └── check_foreign.py / remove_foreign.py   Diagnostic + cleanup for TMDb title-collision mismatches
│
└── frontend/
    ├── app/                         Next.js App Router pages (25+ routes)
    ├── components/                  Nav, Footer, MovieCard, PersonCard, GlobalSearch, WikipediaSummary, etc.
    └── lib/                         api.js (backend calls), wikipedia.js (live Wikipedia fetching)
```

---

## Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

# Populate the database (run once, in this order):
python seed.py
python import_curated.py
python backfill_photos.py
python seed_extra_content.py
python seed_more_trivia.py
python expand_studios_festivals.py

uvicorn main:app --reload --port 8001
```

`import_curated.py`, `backfill_photos.py`, and `expand_studios_festivals.py` require a free
TMDb API key — get one at themoviedb.org → Settings → API, then paste it into the
`API_KEY` line near the top of each script (or set the `TMDB_API_KEY` environment variable).

All seed/import scripts are idempotent — safe to re-run without creating duplicates.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`. The frontend expects the API at `http://localhost:8001/api`
(configurable via `NEXT_PUBLIC_API_BASE` in `frontend/lib/api.js`).

### 3. If something looks wrong

- **Movies page shows too few films** — check `/api/movies` directly; if it's short, an import
  script didn't finish. Re-run `import_curated.py`.
- **Duplicate movies** — run `python check_duplicates.py` to diagnose.
- **A movie shows the wrong (foreign) film** — run `python check_foreign.py`, then
  `python remove_foreign.py` to clean up, then re-import.
- **Schema errors after a fresh pull** — delete `backend/cinema.db` and re-run the full
  setup sequence above.

---

## Data Sourcing & Attribution

- Movie metadata, posters, and cast/crew: [TMDb](https://www.themoviedb.org/) API
- Biographical and historical context: [Wikipedia](https://www.wikipedia.org/), CC BY-SA 4.0, fetched live and attributed on every page it appears
- Highest-grossing films table: Wikipedia's "List of highest-grossing Indian films," CC BY-SA 4.0

This is a personal portfolio/demo project, not a commercial product.
