"""
Adds more trivia facts to reach ~100 total. Idempotent - checks exact fact
text before inserting, safe to re-run.
RUN: python seed_more_trivia.py
"""
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

def movie(title):
    return db.query(models.Movie).filter(models.Movie.title == title).first()

TRIVIA = [
    ("Awaara's dream sequence, with its elaborate sets and choreography, was one of the most expensive single scenes shot in Hindi cinema at the time.", "Production", "Awaara"),
    ("Pyaasa's story of a struggling poet was loosely inspired by director Guru Dutt's own frustrations with the film industry.", "Historical", "Pyaasa"),
    ("Mughal-E-Azam was originally shot in black and white; only the song 'Pyar Kiya To Darna Kya' was filmed in colour due to budget constraints at the time.", "Production", "Mughal-E-Azam"),
    ("Sangam was one of the first major Hindi films shot extensively in Europe, a novelty for Indian audiences in 1964.", "Production", "Sangam"),
    ("Madhumati's reincarnation storyline became a template that countless Bollywood films would revisit for decades.", "Historical", "Madhumati"),
    ("Sahib Bibi Aur Ghulam was based on a Bengali novel and is considered one of the most literary adaptations of its era.", "Production", "Sahib Bibi Aur Ghulam"),
    ("Teesri Kasam was a critical success but a commercial failure on release, financially ruining its producer despite later being celebrated as a classic.", "Historical", "Teesri Kasam"),
    ("Aradhana made Rajesh Khanna a nationwide phenomenon, sparking what is often called Indian cinema's first true fan mania.", "Historical", "Aradhana"),
    ("Anand's screenplay, co-written by Hrishikesh Mukherjee and Gulzar, was reportedly inspired by the real illness of a close friend of the writers.", "Production", "Anand"),
    ("Zanjeer was rejected by several leading actors before Amitabh Bachchan took the role that made him a star.", "Casting", "Zanjeer"),
    ("Trishul featured three generations of a fractured family and is considered a blueprint for the multi-star family drama.", "Historical", "Trishul"),
    ("Kabhi Kabhie was unusual for its time in following its central romance across decades rather than a single timeline.", "Production", "Kabhi Kabhie"),
    ("Karz's reincarnation-revenge plot has been remade multiple times in Indian cinema, most notably decades later.", "Historical", "Karz"),
    ("Namak Haraam paired Amitabh Bachchan and Rajesh Khanna, two of the era's biggest stars, in a story about class and friendship.", "Casting", "Namak Haraam"),
    ("Chupke Chupke is built almost entirely around a single elaborate prank, sustained across the whole film.", "Production", "Chupke Chupke"),
    ("Golmaal's plot about a man maintaining two identities to keep two different jobs became one of Hindi comedy's most referenced setups.", "Historical", "Golmaal"),
    ("Jaane Bhi Do Yaaro's chaotic climax, involving a body and a Mahabharata stage play, is frequently cited as one of Indian cinema's best comic sequences.", "Trivia", "Jaane Bhi Do Yaaro"),
    ("Arth was inspired by real events in director Mahesh Bhatt's own life, giving it an unusually personal, confessional tone for its time.", "Production", "Arth"),
    ("Masoom dealt with themes of infidelity and an illegitimate child with a sensitivity uncommon in mainstream Hindi cinema of the 1980s.", "Historical", "Masoom"),
    ("Umrao Jaan required Rekha to train extensively in classical Kathak dance for her portrayal of a courtesan-poet.", "Production", "Umrao Jaan"),
    ("Mr. India's villain Mogambo, played by Amrish Puri, became one of Indian cinema's most quoted characters despite limited screen time.", "Trivia", "Mr. India"),
    ("Maine Pyar Kiya launched Salman Khan's career and became one of the highest-grossing Hindi films of its decade.", "Casting", "Maine Pyar Kiya"),
    ("Qayamat Se Qayamat Tak revived the doomed-lovers genre in Hindi cinema and launched Aamir Khan as a leading star.", "Historical", "Qayamat Se Qayamat Tak"),
    ("Hum Aapke Hain Koun revived single-screen cinema attendance in India, with some theatres running it for over a year.", "Historical", "Hum Aapke Hain Koun"),
    ("Rangeela was one of the first mainstream Hindi films to prominently feature background score by A. R. Rahman, helping establish his Bollywood career.", "Production", "Rangeela"),
    ("Satya is widely credited with launching the 'Mumbai noir' subgenre of Hindi crime cinema that influenced films for the next two decades.", "Historical", "Satya"),
    ("Darr and Baazigar both cast Shah Rukh Khan as a morally ambiguous or villainous lead, an unusual choice that reshaped his early image.", "Casting", "Darr"),
    ("Border was based on the real Battle of Longewala during the 1971 India-Pakistan war.", "Historical", "Border"),
    ("Dil Se's unconventional, tragic ending was considered a bold departure from typical Bollywood romance conventions.", "Production", "Dil Se"),
    ("Lagaan's cricket match climax was shot with extras trained specifically for the sport over several months.", "Production", "Lagaan"),
    ("Dil Chahta Hai is frequently credited with popularizing a more urban, dialogue-driven style of Hindi cinema in the 2000s.", "Historical", "Dil Chahta Hai"),
    ("Munna Bhai MBBS was originally conceived with a different lead before Sanjay Dutt was cast in the role that became iconic for him.", "Casting", "Munna Bhai MBBS"),
    ("Rang De Basanti intercut a contemporary story with dramatized scenes of India's freedom struggle.", "Production", "Rang De Basanti"),
    ("Taare Zameen Par was Aamir Khan's directorial debut and dealt with dyslexia at a time few Hindi films addressed learning disabilities.", "Historical", "Taare Zameen Par"),
    ("Om Shanti Om's plot revolves around reincarnation and a murder mystery set against the backdrop of the Hindi film industry itself.", "Trivia", "Om Shanti Om"),
    ("Chak De! India was inspired partly by the real story of the Indian women's national hockey team.", "Historical", "Chak De! India"),
    ("3 Idiots became one of the highest-grossing Indian films of its time and sparked debate about India's engineering education system.", "Historical", "3 Idiots"),
    ("Kahaani was shot almost entirely on location in Kolkata's real streets rather than sets, giving it a documentary-like texture.", "Production", "Kahaani"),
    ("Barfi! told its story largely through visual comedy reminiscent of silent-era cinema, with minimal dialogue for its lead character.", "Production", "Barfi!"),
    ("Gangs of Wasseypur was shot as a single long film but released in two parts due to its five-hour runtime.", "Production", "Gangs of Wasseypur"),
    ("Queen followed a jilted bride on a solo honeymoon trip, a premise considered unconventional for a mainstream Hindi heroine at the time.", "Historical", "Queen"),
    ("PK used a fish-out-of-water alien premise to satirize organized religion, drawing both major box office success and controversy.", "Trivia", "PK"),
    ("Bajrangi Bhaijaan became one of the highest-grossing Indian films in Pakistan despite being a Hindi production.", "Historical", "Bajrangi Bhaijaan"),
    ("Piku built its entire narrative around a father's digestive health, an unusually mundane premise for a mainstream release.", "Trivia", "Piku"),
    ("Neerja dramatized the real 1986 hijacking of Pan Am Flight 73 and the actions of flight attendant Neerja Bhanot.", "Historical", "Neerja"),
    ("Pink centered its courtroom drama on questions of consent, sparking wide social discussion on its release.", "Historical", "Pink"),
    ("Newton was India's official submission for the Academy Award for Best Foreign Language Film in 2017.", "Awards", "Newton"),
    ("Gully Boy drew directly from the real underground rap scene of Mumbai, with several real rappers contributing to its soundtrack.", "Production", "Gully Boy"),
    ("Uri: The Surgical Strike's dialogue 'How's the josh?' became a widely repeated catchphrase across India after release.", "Trivia", "Uri: The Surgical Strike"),
    ("Article 15 was inspired by real caste-based atrocity cases reported in India.", "Historical", "Article 15"),
    ("Badhaai Ho built its comedy around an unplanned pregnancy of a middle-aged couple, a subject rarely centered in mainstream Hindi film.", "Trivia", "Badhaai Ho"),
    ("Raazi was based on a novel inspired by the real story of an Indian intelligence operative during the 1971 war.", "Historical", "Raazi"),
    ("Stree drew on real folklore from Karnataka about a spirit that would not enter homes with a specific phrase written outside.", "Historical", "Stree"),
    ("Tanhaji: The Unsung Warrior dramatized the 1670 Battle of Sinhagad from Maratha history.", "Historical", "Tanhaji: The Unsung Warrior"),
    ("Shershaah dramatized the life of Captain Vikram Batra, a soldier awarded India's highest military honour posthumously.", "Historical", "Shershaah"),
    ("83 recreated India's historic 1983 Cricket World Cup victory, with the cast undergoing months of cricket training.", "Production", "83"),
    ("Gangubai Kathiawadi was based on a chapter from a book about real figures in Mumbai's Kamathipura red-light district.", "Historical", "Gangubai Kathiawadi"),
    ("12th Fail dramatized the real story of an IPS officer who overcame extreme poverty to pass India's civil services exam.", "Historical", "12th Fail"),
    ("Animal's runtime of over three hours made it one of the longest mainstream Hindi releases in recent years.", "Trivia", "Animal"),
    ("Jawan featured Shah Rukh Khan in a dual role, a format Hindi cinema has periodically returned to across decades.", "Casting", "Jawan"),
    ("Pathaan marked Shah Rukh Khan's return to the screen after a four-year gap and became one of Hindi cinema's biggest openings.", "Historical", "Pathaan"),
    ("Dabangg introduced the character of Chulbul Pandey, whose mannerisms and dialogue spawned a long-running franchise.", "Historical", "Dabangg"),
    ("Tere Naam is remembered in part for its lead's distinctive half-shaved hairstyle, which became a pop-culture reference point.", "Trivia", "Tere Naam"),
    ("Lanka Dahan was reportedly screened with coins thrown at the screen by audiences as an offering during Hanuman's appearance.", "Historical", "Lanka Dahan"),
    ("Bhakta Vidur used its mythological story as a thinly veiled allegory for the Indian independence movement, leading to its ban by colonial authorities.", "Historical", "Bhakta Vidur"),
    ("A Throw of Dice was shot on location in India with a large cast of extras and real elephants, a scale unusual for silent-era productions.", "Production", "A Throw of Dice"),
    ("Kaliya Mardan cast Dadasaheb Phalke's own daughter, Mandakini, in the role of young Krishna.", "Casting", "Kaliya Mardan"),
    ("Mayura dramatized the life of a legendary king from Karnataka's history and remains one of Rajkumar's most celebrated performances.", "Historical", "Mayura"),
    ("Nagarahavu's storyline, involving a rebellious anti-hero, was considered a bold departure from typical Kannada cinema heroes of its time.", "Historical", "Nagarahavu"),
    ("Bandhana became known for its emotionally intense performances and remains a frequently cited classic of 1980s Kannada cinema.", "Trivia", "Bandhana"),
    ("Lucia was partly crowdfunded, an unusual production model for Kannada cinema at the time of its release.", "Production", "Lucia"),
    ("U-Turn's plot, involving a curse tied to a specific flyover in Bangalore, drew on local urban legend.", "Historical", "U-Turn"),
    ("777 Charlie followed a man and his dog on a road trip and became notable for its emotional depiction of the human-animal bond.", "Trivia", "777 Charlie"),
    ("KGF: Chapter 1 was made on a comparatively modest budget but its success reshaped perceptions of Kannada cinema's national reach.", "Historical", "KGF: Chapter 1"),
    ("Aparajito, the second film in the Apu Trilogy, continued the story from Pather Panchali and further established Satyajit Ray internationally.", "Historical", "Aparajito"),
    ("Apur Sansar completed the Apu Trilogy and is frequently ranked among the greatest films in world cinema history.", "Historical", "Apur Sansar"),
    ("Jalsaghar centered on a declining aristocrat's obsession with music and status, using classical Indian music extensively in its soundtrack.", "Production", "Jalsaghar"),
    ("Meghe Dhaka Tara dealt with the aftermath of Partition through the story of a refugee family, a recurring theme in Ritwik Ghatak's work.", "Historical", "Meghe Dhaka Tara"),
    ("Subarnarekha took several years to complete due to funding difficulties, despite being one of Ritwik Ghatak's most acclaimed films.", "Production", "Subarnarekha"),
    ("Goopy Gyne Bagha Byne remains one of the most beloved Bengali family films, blending fantasy and music for a multigenerational audience.", "Trivia", "Goopy Gyne Bagha Byne"),
    ("Ghare Baire was adapted from a novel by Rabindranath Tagore, exploring nationalism and personal freedom in colonial Bengal.", "Historical", "Ghare Baire"),
    ("Missamma's plot of mistaken identities and disguised marriage was popular enough to be remade in multiple other Indian languages.", "Historical", "Missamma"),
    ("Pathala Bhairavi was among the first Telugu films to use elaborate trick photography for its fantasy sequences.", "Production", "Pathala Bhairavi"),
    ("Devadasu is based on a Bengali novel that has been adapted into Indian cinema more times than almost any other literary work.", "Historical", "Devadasu"),
    ("Lava Kusa was one of the first Telugu films widely released in colour, drawing enormous crowds on release.", "Historical", "Lava Kusa"),
    ("Sankarabharanam is credited with reviving interest in Carnatic classical music among mainstream Telugu audiences.", "Historical", "Sankarabharanam"),
    ("Sagara Sangamam centered on classical dance and is remembered for its lead's extensive training in Kuchipudi for the role.", "Production", "Sagara Sangamam"),
    ("Pushpaka Vimana told its entire story without a single line of dialogue, relying purely on visual comedy.", "Trivia", "Pushpaka Vimana"),
    ("Magadheera's reincarnation storyline and large-scale action sequences made it one of the highest-grossing Telugu films of its era.", "Historical", "Magadheera"),
    ("Baahubali 2: The Conclusion answered the cliffhanger question 'Why Kattappa killed Baahubali,' which had become a nationwide talking point after the first film.", "Trivia", "Baahubali 2: The Conclusion"),
]

count = 0
for fact, category, movie_title in TRIVIA:
    if db.query(models.TriviaCard).filter(models.TriviaCard.fact == fact).first():
        continue
    m = movie(movie_title)
    db.add(models.TriviaCard(fact=fact, category=category, movie_id=m.id if m else None))
    count += 1

db.commit()
total = db.query(models.TriviaCard).count()
db.close()
print(f"Added {count} new trivia cards. Total trivia in database: {total}.")