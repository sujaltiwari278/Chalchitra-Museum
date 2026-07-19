from database import SessionLocal, engine
import models
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

def movie(t): return db.query(models.Movie).filter(models.Movie.title == t).first()
def studio(n): return db.query(models.Studio).filter(models.Studio.name == n).first()
def fest(n): return db.query(models.FilmFestival).filter(models.FilmFestival.name == n).first()

STUDIOS = [
    ("Hombale Films", 2016, "Bangalore-based studio behind KGF and Kantara, central to Kannada cinema's national rise."),
    ("Eros International", 1977, "One of India's largest film distributors and producers, active across multiple languages."),
    ("Prasad Studios", 1956, "Legendary Chennai-based studio and post-production house serving South Indian cinema for decades."),
    ("Reliance Entertainment", 2005, "Major producer and financier behind large-scale Hindi productions."),
    ("Geetha Arts", 1968, "Telugu production house behind several major blockbusters including Baahubali's collaborators."),
    ("Rockline Entertainment", 1990, "Prominent Kannada and multi-language production and distribution house."),
]
for n, y, b in STUDIOS:
    if not studio(n):
        db.add(models.Studio(name=n, founded_year=y, bio=b))
db.commit()

LINKS = [
    ("Kantara", "Hombale Films"), ("KGF: Chapter 1", "Hombale Films"),
    ("Baahubali 2: The Conclusion", "Arka Media Works"),
]
for t, sn in LINKS:
    m, s = movie(t), studio(sn)
    if m and s and not m.studio_id:
        m.studio_id = s.id
db.commit()

FESTIVALS = [
    ("Berlin International Film Festival", 1951, "Berlin, Germany", "One of the 'Big Three' European festivals, alongside Cannes and Venice."),
    ("Venice Film Festival", 1932, "Venice, Italy", "The world's oldest film festival, showcasing global and Indian arthouse cinema."),
    ("Toronto International Film Festival", 1976, "Toronto, Canada", "A major launchpad for award-season and international cinema, including Indian films."),
]
for n, y, loc, b in FESTIVALS:
    if not fest(n):
        db.add(models.FilmFestival(name=n, founded_year=y, location=loc, bio=b))
db.commit()

# Fuller descriptions for existing festivals
updates = {
    "International Film Festival of India": "India's oldest and most prestigious film festival, held annually in Goa since 1952, showcasing Indian and international cinema across genres and languages.",
    "Cannes Film Festival": "Founded in 1946, Cannes is the most prestigious film festival in the world; Indian films have appeared in its official selection, competition, and sidebars for decades.",
}
for name, bio in updates.items():
    f = fest(name)
    if f:
        f.bio = bio
db.commit()

SELECTIONS = [
    ("Baahubali 2: The Conclusion", "Toronto International Film Festival", "Special Presentation"),
    ("Newton", "Berlin International Film Festival", "Forum Section"),
    ("The Lunchbox", "Cannes Film Festival", "Critics' Week"),
    ("Kantara", "Toronto International Film Festival", "Midnight Madness"),
]
count = 0
for t, fn, sel in SELECTIONS:
    m, f = movie(t), fest(fn)
    if m and f:
        exists = db.execute(models.festival_selection.select().where(
            (models.festival_selection.c.festival_id == f.id) & (models.festival_selection.c.movie_id == m.id)
        )).first()
        if not exists:
            db.execute(models.festival_selection.insert().values(festival_id=f.id, movie_id=m.id, selection_type=sel))
            count += 1
db.commit()
db.close()
print(f"Added {len(STUDIOS)} studios, {len(FESTIVALS)} festivals, {count} new selections.")
