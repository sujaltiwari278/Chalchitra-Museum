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