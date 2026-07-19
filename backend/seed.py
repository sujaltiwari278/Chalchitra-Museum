from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(models.Movie).first():
    print("Database already contains movies - seed.py has likely already been run.")
    print("Skipping to avoid creating duplicates. Delete cinema.db first if you want to reset.")
    db.close()
    exit()

movies = [
    dict(title="Raja Harishchandra", release_year=1913, language="Hindi (Silent)",
         era="Silent Era", genre="Mythological", runtime_minutes=40,
         synopsis="India's first full-length feature film, directed by Dadasaheb Phalke.",
         trivia="Considered the birth of Indian cinema."),
    dict(title="Alam Ara", release_year=1931, language="Hindi",
         era="Talkies", genre="Drama", runtime_minutes=124,
         synopsis="India's first sound film (talkie), directed by Ardeshir Irani."),
    dict(title="Mother India", release_year=1957, language="Hindi",
         era="Golden Age", genre="Drama", runtime_minutes=172,
         synopsis="An epic tale of a poor village woman's resilience and sacrifice.",
         box_office_inr=40000000),
    dict(title="Pather Panchali", release_year=1955, language="Bengali",
         era="Parallel Cinema", genre="Drama", runtime_minutes=125,
         synopsis="Satyajit Ray's landmark debut chronicling a poor family in rural Bengal."),
    dict(title="Sholay", release_year=1975, language="Hindi",
         era="Golden Age", genre="Action", runtime_minutes=204,
         synopsis="Two criminals hired to catch a ruthless dacoit, a defining blockbuster.",
         box_office_inr=350000000),
    dict(title="Baahubali: The Beginning", release_year=2015, language="Telugu",
         era="Pan India Cinema", genre="Epic Action", runtime_minutes=159,
         synopsis="An epic saga of an amnesiac warrior uncovering his royal destiny.",
         box_office_inr=6500000000),
    dict(title="RRR", release_year=2022, language="Telugu",
         era="Pan India Cinema", genre="Period Action", runtime_minutes=187,
         synopsis="A fictional tale of two real revolutionaries in pre-independence India.",
         box_office_inr=12000000000),
    dict(title="The Lunchbox", release_year=2013, language="Hindi",
         era="Modern Cinema", genre="Romance", runtime_minutes=104,
         synopsis="A mistaken lunchbox delivery connects two lonely strangers in Mumbai."),
    dict(title="Kantara", release_year=2022, language="Kannada",
         era="OTT Revolution", genre="Action Thriller", runtime_minutes=150,
         synopsis="A folklore-rooted tale of man, nature, and divine justice in coastal Karnataka."),
]

for m in movies:
    db.add(models.Movie(**m))
db.commit()

# ---------- PEOPLE ----------

def movie_by_title(title):
    return db.query(models.Movie).filter(models.Movie.title == title).first()

people = [
    dict(name="Dadasaheb Phalke", gender="M", bio="Pioneer of Indian cinema, directed the first Indian feature film."),
    dict(name="Ardeshir Irani", gender="M", bio="Produced and directed Alam Ara, India's first talkie."),
    dict(name="Mehboob Khan", gender="M", bio="Acclaimed director known for epic social dramas like Mother India."),
    dict(name="Nargis", gender="F", bio="Legendary actress, iconic for her role in Mother India."),
    dict(name="Satyajit Ray", gender="M", bio="Pioneer of Parallel Cinema and one of the greatest filmmakers in world cinema."),
    dict(name="Ramesh Sippy", gender="M", bio="Director of Sholay, one of Indian cinema's biggest blockbusters."),
    dict(name="Amitabh Bachchan", gender="M", bio="Iconic actor known for his roles in Sholay and countless classics."),
    dict(name="S. S. Rajamouli", gender="M", bio="Director behind the Baahubali and RRR franchises, pioneer of Pan India cinema."),
    dict(name="Prabhas", gender="M", bio="Lead actor of the Baahubali franchise."),
    dict(name="N. T. Rama Rao Jr.", gender="M", bio="Lead actor in RRR, known for his intense on-screen presence."),
    dict(name="Ritesh Batra", gender="M", bio="Director of The Lunchbox, known for intimate character-driven stories."),
    dict(name="Rishab Shetty", gender="M", bio="Director and lead actor of Kantara, rooted in Karnataka folklore."),
    dict(name="M. M. Keeravani", gender="M", bio="Music director known for the Oscar-winning song 'Naatu Naatu' from RRR."),
]

for p in people:
    db.add(models.Person(**p))
db.commit()

def link(movie_title, person_name, role):
    movie = movie_by_title(movie_title)
    person = db.query(models.Person).filter(models.Person.name == person_name).first()
    if movie and person:
        db.execute(models.movie_cast.insert().values(movie_id=movie.id, person_id=person.id, role=role))

credits = [
    ("Raja Harishchandra", "Dadasaheb Phalke", "director"),
    ("Alam Ara", "Ardeshir Irani", "director"),
    ("Mother India", "Mehboob Khan", "director"),
    ("Mother India", "Nargis", "actor"),
    ("Pather Panchali", "Satyajit Ray", "director"),
    ("Sholay", "Ramesh Sippy", "director"),
    ("Sholay", "Amitabh Bachchan", "actor"),
    ("Baahubali: The Beginning", "S. S. Rajamouli", "director"),
    ("Baahubali: The Beginning", "Prabhas", "actor"),
    ("RRR", "S. S. Rajamouli", "director"),
    ("RRR", "N. T. Rama Rao Jr.", "actor"),
    ("RRR", "M. M. Keeravani", "music"),
    ("The Lunchbox", "Ritesh Batra", "director"),
    ("Kantara", "Rishab Shetty", "director"),
    ("Kantara", "Rishab Shetty", "actor"),
]

for movie_title, person_name, role in credits:
    link(movie_title, person_name, role)

db.commit()
db.close()
print(f"Seeded {len(movies)} movies, {len(people)} people, {len(credits)} credits.")

# ---------- STUDIOS, AWARDS, FILM FESTIVALS ----------

db = SessionLocal()

studios = [
    dict(name="Phalke Films", founded_year=1913, bio="Founded by Dadasaheb Phalke, producer of India's earliest features."),
    dict(name="Mehboob Productions", founded_year=1943, bio="Studio behind classics of Indian cinema's Golden Age."),
    dict(name="Arka Media Works", founded_year=2002, bio="Telugu production house behind the Baahubali and RRR franchises."),
]
for s in studios:
    db.add(models.Studio(**s))
db.commit()

def studio_by_name(name):
    return db.query(models.Studio).filter(models.Studio.name == name).first()

studio_links = [
    ("Raja Harishchandra", "Phalke Films"),
    ("Mother India", "Mehboob Productions"),
    ("Baahubali: The Beginning", "Arka Media Works"),
    ("RRR", "Arka Media Works"),
]
for movie_title, studio_name in studio_links:
    movie = movie_by_title(movie_title)
    studio = studio_by_name(studio_name)
    if movie and studio:
        movie.studio_id = studio.id
db.commit()

festivals = [
    dict(name="International Film Festival of India", founded_year=1952, location="Goa",
         bio="India's premier international film festival, held annually in Goa."),
    dict(name="Cannes Film Festival", founded_year=1946, location="Cannes, France",
         bio="One of the most prestigious film festivals in the world."),
]
for f in festivals:
    db.add(models.FilmFestival(**f))
db.commit()

def festival_by_name(name):
    return db.query(models.FilmFestival).filter(models.FilmFestival.name == name).first()

festival_links = [
    ("Pather Panchali", "Cannes Film Festival", "Official Selection"),
    ("RRR", "International Film Festival of India", "Winner"),
]
for movie_title, festival_name, selection_type in festival_links:
    movie = movie_by_title(movie_title)
    festival = festival_by_name(festival_name)
    if movie and festival:
        db.execute(models.festival_selection.insert().values(
            festival_id=festival.id, movie_id=movie.id, selection_type=selection_type
        ))
db.commit()

def person_by_name(name):
    return db.query(models.Person).filter(models.Person.name == name).first()

awards = [
    dict(name="National Film Award", category="Best Feature Film", year=1955, winner="Yes",
         movie_id=movie_by_title("Pather Panchali").id),
    dict(name="National Film Award", category="Best Director", year=1957, winner="Yes",
         movie_id=movie_by_title("Mother India").id),
    dict(name="Academy Award", category="Best Original Song", year=2023, winner="Yes",
         movie_id=movie_by_title("RRR").id, person_id=person_by_name("M. M. Keeravani").id),
    dict(name="Filmfare Award", category="Best Actor", year=1976, winner="Nominated",
         movie_id=movie_by_title("Sholay").id, person_id=person_by_name("Amitabh Bachchan").id),
]
for a in awards:
    db.add(models.Award(**a))
db.commit()

print(f"Seeded {len(studios)} studios, {len(festivals)} festivals, {len(awards)} awards.")

# ---------- TRIVIA & ARCHIVES ----------

trivia_cards = [
    dict(fact="Raja Harishchandra had no actresses at all — female roles were played by men, since acting was considered unsuitable for women in 1913.",
         category="Historical", movie_id=movie_by_title("Raja Harishchandra").id),
    dict(fact="Alam Ara's original prints are completely lost today — no known copy of India's first talkie survives.",
         category="Historical", movie_id=movie_by_title("Alam Ara").id),
    dict(fact="Sholay was initially a box office disappointment on its opening week before word-of-mouth turned it into a phenomenon.",
         category="Production", movie_id=movie_by_title("Sholay").id),
    dict(fact="RRR's 'Naatu Naatu' became the first song from an Indian production to win the Academy Award for Best Original Song.",
         category="Awards", movie_id=movie_by_title("RRR").id),
    dict(fact="Pather Panchali was funded partly by Satyajit Ray selling his personal insurance policies and record collection.",
         category="Production", movie_id=movie_by_title("Pather Panchali").id),
    dict(fact="Baahubali: The Beginning ends on a cliffhanger that was originally meant to be revealed as a single film before the studio split it into two parts.",
         category="Production", movie_id=movie_by_title("Baahubali: The Beginning").id),
]
for t in trivia_cards:
    db.add(models.TriviaCard(**t))
db.commit()

archive_items = [
    dict(title="Dadasaheb Phalke on set, 1913", category="Photograph", year=1913,
         description="One of the earliest surviving photographs from an Indian film production."),
    dict(title="Original Alam Ara release poster", category="Poster", year=1931,
         description="Promotional artwork for India's first sound film."),
    dict(title="Satyajit Ray's handwritten script notes", category="Document", year=1955,
         description="Preserved notes from the making of Pather Panchali."),
    dict(title="RRR premiere press interview", category="Interview", year=2022,
         description="Cast and crew discussing the film's cross-cultural reception ahead of release."),
]
for item in archive_items:
    db.add(models.ArchiveItem(**item))
db.commit()

print(f"Seeded {len(trivia_cards)} trivia cards, {len(archive_items)} archive items.")
db.close()

