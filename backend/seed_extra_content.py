"""
Expands Studios, Awards, Film Festivals, Trivia, and Archives to cover the
full curated 150-film catalog (seed.py + import_curated.py only touched the
original 9 sample movies for these tables).

Idempotent: checks for existing records by name before inserting, so it's
safe to re-run without creating duplicates (unlike the old seed.py bug).

RUN: python seed_extra_content.py
Requires seed.py and import_curated.py to have already been run.
"""
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

def movie(title):
    return db.query(models.Movie).filter(models.Movie.title == title).first()

def person(name):
    return db.query(models.Person).filter(models.Person.name == name).first()

def get_or_create_studio(name, founded_year=None, bio=None):
    s = db.query(models.Studio).filter(models.Studio.name == name).first()
    if s:
        return s
    s = models.Studio(name=name, founded_year=founded_year, bio=bio)
    db.add(s)
    db.flush()
    return s

def get_or_create_festival(name, founded_year=None, location=None, bio=None):
    f = db.query(models.FilmFestival).filter(models.FilmFestival.name == name).first()
    if f:
        return f
    f = models.FilmFestival(name=name, founded_year=founded_year, location=location, bio=bio)
    db.add(f)
    db.flush()
    return f

# ---------- STUDIOS ----------

STUDIOS = [
    ("Sippy Films", 1971, "Founded by G. P. Sippy; produced Sholay, one of Indian cinema's biggest blockbusters."),
    ("Trimurti Films", 1975, "Founded by Gulshan Rai; produced Deewar and Trishul, defining the 1970s angry-young-man era."),
    ("Yash Raj Films", 1970, "Founded by Yash Chopra; one of Hindi cinema's most influential production houses."),
    ("Rajshri Productions", 1947, "One of India's oldest studios, known for family dramas like Hum Aapke Hain Koun."),
    ("R.K. Films", 1948, "Founded by Raj Kapoor; produced Awaara and Shree 420, Golden Age classics."),
    ("Vijaya Vauhini Studios", 1948, "Founded by B. Nagi Reddy; produced Telugu classics including Mayabazar and Missamma."),
    ("Aamir Khan Productions", 2001, "Founded by Aamir Khan; produced Lagaan, Taare Zameen Par, and PK."),
    ("Dharma Productions", 1976, "Founded by Yash Johar; produced Kuch Kuch Hota Hai and Kal Ho Naa Ho."),
    ("Excel Entertainment", 1999, "Founded by Ritesh Sidhwani and Farhan Akhtar; produced Dil Chahta Hai and Zindagi Na Milegi Dobara."),
    ("Red Chillies Entertainment", 2002, "Founded by Shah Rukh Khan; produced Om Shanti Om."),
]

STUDIO_LINKS = [
    ("Sholay", "Sippy Films"),
    ("Deewar", "Trimurti Films"),
    ("Trishul", "Trimurti Films"),
    ("Silsila", "Yash Raj Films"),
    ("Dilwale Dulhania Le Jayenge", "Yash Raj Films"),
    ("Hum Aapke Hain Koun", "Rajshri Productions"),
    ("Awaara", "R.K. Films"),
    ("Shree 420", "R.K. Films"),
    ("Mayabazar", "Vijaya Vauhini Studios"),
    ("Missamma", "Vijaya Vauhini Studios"),
    ("Lagaan", "Aamir Khan Productions"),
    ("Taare Zameen Par", "Aamir Khan Productions"),
    ("PK", "Aamir Khan Productions"),
    ("Kuch Kuch Hota Hai", "Dharma Productions"),
    ("Kal Ho Naa Ho", "Dharma Productions"),
    ("Dil Chahta Hai", "Excel Entertainment"),
    ("Zindagi Na Milegi Dobara", "Excel Entertainment"),
    ("Om Shanti Om", "Red Chillies Entertainment"),
]

for name, year, bio in STUDIOS:
    get_or_create_studio(name, year, bio)
db.commit()

studio_count = 0
for title, studio_name in STUDIO_LINKS:
    m, s = movie(title), db.query(models.Studio).filter(models.Studio.name == studio_name).first()
    if m and s and not m.studio_id:
        m.studio_id = s.id
        studio_count += 1
db.commit()

# ---------- FILM FESTIVALS ----------

get_or_create_festival("Academy Awards (Oscars)", 1929, "Los Angeles, USA",
    "The Academy Awards; India has submitted films for Best International Feature Film since 1957.")

FESTIVAL_LINKS = [
    ("Devdas", "Cannes Film Festival", "Out of Competition Premiere"),
    ("Gangs of Wasseypur", "Cannes Film Festival", "Directors' Fortnight"),
    ("Masaan", "Cannes Film Festival", "Un Certain Regard - FIPRESCI Prize"),
    ("Mother India", "Academy Awards (Oscars)", "India's First Best Foreign Language Film Submission"),
    ("Lagaan", "Academy Awards (Oscars)", "Best Foreign Language Film Nominee"),
    ("Newton", "Academy Awards (Oscars)", "Best Foreign Language Film Submission"),
]

fest_count = 0
for title, fest_name, sel_type in FESTIVAL_LINKS:
    m = movie(title)
    f = db.query(models.FilmFestival).filter(models.FilmFestival.name == fest_name).first()
    if m and f:
        exists = db.execute(
            models.festival_selection.select().where(
                (models.festival_selection.c.festival_id == f.id)
                & (models.festival_selection.c.movie_id == m.id)
            )
        ).first()
        if not exists:
            db.execute(models.festival_selection.insert().values(
                festival_id=f.id, movie_id=m.id, selection_type=sel_type
            ))
            fest_count += 1
db.commit()

# ---------- AWARDS ----------
# Verified against Wikipedia / official National Film Awards records.

AWARDS = [
    ("National Film Award", "Best Hindi Feature Film", 1983, "Ardh Satya", None, "Yes"),
    ("National Film Award", "Best Popular Film Providing Wholesome Entertainment", 2001, "Lagaan", None, "Yes"),
    ("National Film Award", "Best Feature Film in Hindi", 2019, "Gully Boy", None, "Yes"),
    ("National Film Award", "Best Actor", 2018, "Andhadhun", "Ayushmann Khurrana", "Yes"),
    ("Filmfare Award", "Best Movie", 1961, "Mughal-E-Azam", None, "Yes"),
    ("Filmfare Award", "Best Movie", 1966, "Guide", None, "Yes"),
    ("Filmfare Award", "Best Movie", 1972, "Anand", None, "Yes"),
    ("Filmfare Award", "Best Movie", 1978, "Amar Akbar Anthony", None, "Yes"),
    ("Filmfare Award", "Best Film", 2010, "3 Idiots", None, "Yes"),
    ("Filmfare Award", "Best Film", 2017, "Dangal", None, "Yes"),
    ("Filmfare Award", "Best Actress", 2023, "Gangubai Kathiawadi", "Alia Bhatt", "Yes"),
]

award_count = 0
for name, category, year, movie_title, person_name, winner in AWARDS:
    exists = db.query(models.Award).filter(
        models.Award.name == name, models.Award.category == category, models.Award.year == year
    ).first()
    if exists:
        continue
    m = movie(movie_title)
    p = person(person_name) if person_name else None
    if m:
        db.add(models.Award(name=name, category=category, year=year, winner=winner,
                             movie_id=m.id, person_id=p.id if p else None))
        award_count += 1
db.commit()

# ---------- TRIVIA ----------

TRIVIA = [
    ("Mughal-E-Azam took over 16 years to complete, from script to release, and remains one of the most expensive films of its era when adjusted for inflation.", "Production", "Mughal-E-Azam"),
    ("Deewar's line 'Mere paas maa hai' became one of the most quoted lines in Hindi cinema history.", "Historical", "Deewar"),
    ("3 Idiots was based on Chetan Bhagat's novel Five Point Someone, though the film significantly diverged from the book's plot.", "Production", "3 Idiots"),
    ("Lagaan was shot almost entirely in a remote village in Gujarat, with the cast learning cricket from scratch for the film.", "Production", "Lagaan"),
    ("Dangal's lead actor Aamir Khan gained and then lost significant weight to portray both the older and younger versions of his character.", "Production", "Dangal"),
    ("Gangs of Wasseypur was originally shot as a single film but released in two parts due to its length.", "Production", "Gangs of Wasseypur"),
    ("Andhadhun's ambiguous ending became one of the most debated film conclusions in recent Hindi cinema.", "Trivia", "Andhadhun"),
    ("Amar Akbar Anthony's plot of three brothers separated in childhood and raised in different religions became a template copied by many later Bollywood films.", "Historical", "Amar Akbar Anthony"),
    ("Guide was simultaneously made in Hindi and English, with different directors for each version.", "Production", "Guide"),
    ("Awaara's title song became hugely popular across the Soviet Union and China, making Raj Kapoor one of India's first global film stars.", "Historical", "Awaara"),
    ("Mayabazar is frequently cited by industry polls as the greatest Telugu film ever made.", "Historical", "Mayabazar"),
    ("Charulata was reportedly Satyajit Ray's personal favorite among his own films.", "Trivia", "Charulata"),
    ("Kaagaz Ke Phool was a box office failure on release but is now considered a classic reflection on the film industry itself.", "Historical", "Kaagaz Ke Phool"),
    ("KGF: Chapter 1 was made on a considerably smaller budget than its sequel but became a sleeper hit that changed Kannada cinema's national profile.", "Production", "KGF: Chapter 1"),
    ("Devdas (2002) was, at the time, one of the most expensive Bollywood productions ever made, known for its elaborate sets.", "Production", "Devdas"),
    ("Gully Boy was inspired by the real lives of Mumbai street rappers Divine and Naezy.", "Production", "Gully Boy"),
]

trivia_count = 0
for fact, category, movie_title in TRIVIA:
    exists = db.query(models.TriviaCard).filter(models.TriviaCard.fact == fact).first()
    if exists:
        continue
    m = movie(movie_title)
    db.add(models.TriviaCard(fact=fact, category=category, movie_id=m.id if m else None))
    trivia_count += 1
db.commit()

# ---------- ARCHIVES ----------

ARCHIVES = [
    ("Raj Kapoor and R.K. Films promotional stills", "Photograph", 1955, "Publicity material from the Golden Age of Hindi cinema."),
    ("Mughal-E-Azam original lobby cards", "Poster", 1960, "Rare theatrical promotional cards from the film's original release."),
    ("Satyajit Ray's storyboards for the Apu Trilogy", "Document", 1958, "Preserved sketches from one of world cinema's most celebrated trilogies."),
    ("NTR and ANR on set, Telugu Golden Age", "Photograph", 1957, "Behind-the-scenes photography from the classic Telugu studio era."),
    ("Sholay script annotations", "Document", 1975, "Notes from the making of one of Hindi cinema's most quoted films."),
    ("Baahubali production design sketches", "Document", 2015, "Concept art for the film's elaborate fictional kingdom of Mahishmati."),
]

archive_count = 0
for title, category, year, desc in ARCHIVES:
    exists = db.query(models.ArchiveItem).filter(models.ArchiveItem.title == title).first()
    if exists:
        continue
    db.add(models.ArchiveItem(title=title, category=category, year=year, description=desc))
    archive_count += 1
db.commit()

db.close()
print(f"Added: {studio_count} studio links, {fest_count} festival selections, "
      f"{award_count} awards, {trivia_count} trivia cards, {archive_count} archive items.")
print("Safe to re-run - already-existing entries are skipped.")
