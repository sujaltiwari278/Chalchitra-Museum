import { getWikipediaSummary } from "@/lib/wikipedia";

const ERAS = [
  {
    title: "The Silent Era",
    range: "1913 – 1931",
    wikiTopic: "Dadasaheb Phalke",
    body: [
      "Indian cinema was born out of one man's obsession. Dadasaheb Phalke, a photographer and printer by trade, is said to have watched a silent film about the life of Christ in a Bombay theatre in 1910 and walked out convinced that if the West could put its gods on screen, India could put its own there too. He sold his wife's jewelry, learned filmmaking largely by trial and error, and in 1913 released Raja Harishchandra — a mythological drama that is now recognized as India's first feature film.",
      "The films of this era were shot without synchronized sound, accompanied instead by live musicians, narrators, and sometimes entire orchestras in the theatre itself. Female roles were frequently played by men, since acting was considered disreputable work for women at the time. Despite the primitive tools, studios sprang up in Bombay, Calcutta, and Madras through the 1920s, producing dozens of silent features a year and establishing cinema as a genuinely national pastime rather than a novelty import.",
    ],
  },
  {
    title: "The Talkies Arrive",
    range: "1931",
    wikiTopic: "Ardeshir Irani",
    body: [
      "For eighteen years, Indian audiences watched their stories unfold in silence. That changed in March 1931, when Ardeshir Irani's Alam Ara premiered in Bombay with fully synchronized dialogue and song. Crowds were reportedly so large that police had to be called in to manage them. The film's success was immediate and total — within a few years, silent cinema in India was effectively extinct.",
      "The talkies did something the silent era never could: they gave Indian cinema its voice, quite literally, and with that voice came music. The song sequence — performers breaking into full musical numbers mid-narrative — became a structural feature of Indian film almost overnight, and remains one of the defining traits of the industry a century later.",
    ],
  },
  {
    title: "The Golden Age",
    range: "1940s – 1960s",
    wikiTopic: "Mehboob Studios",
    body: [
      "The decades following independence are often remembered as Indian cinema's Golden Age, and for good reason. This was the era of Raj Kapoor's Awaara, whose title song became so popular in the Soviet Union that Kapoor was mobbed on the streets of Moscow; of Guru Dutt's Pyaasa, a meditation on artistic failure so personal it now reads almost as prophecy; of Mehboob Khan's Mother India, an epic of rural sacrifice that became India's first-ever Academy Award submission.",
      "This was also the era of the studio system giving way to independent, star-driven production, and of technical ambition on a scale India had never attempted — Mughal-E-Azam alone took roughly sixteen years to complete, with its most famous sequence hand-tinted in colour frame by frame because full colour stock was still a luxury. The Golden Age didn't just make films; it built the visual and emotional vocabulary that Indian cinema still speaks today.",
    ],
  },
  {
    title: "Parallel Cinema",
    range: "1950s – 1980s",
    wikiTopic: "Satyajit Ray",
    body: [
      "Alongside the song-and-dance spectacle of mainstream cinema, a quieter, harder-edged movement was taking shape. Satyajit Ray, a graphic designer with no formal filmmaking training, mortgaged his wife's jewelry and sold his own record collection to finish Pather Panchali in 1955 — a film about rural poverty in Bengal, shot with non-professional actors and almost no budget for retakes. It went on to win the prize for Best Human Document at Cannes and put Indian cinema on the map for audiences who had never seen a song-and-dance number in their lives.",
      "Ray, Ritwik Ghatak, and the filmmakers who followed them rejected escapism entirely. Ghatak's Meghe Dhaka Tara turned the trauma of Partition into cinema; Ray's later work moved from rural Bengal to the drawing rooms of the Bengali aristocracy without ever losing its humanist eye. Parallel Cinema proved, film after film, that Indian audiences — and the world — would watch stories that offered no easy comfort.",
    ],
  },
  {
    title: "Regional Cinema Comes Into Its Own",
    range: "1950s – 2000s",
    wikiTopic: "Rajkumar (actor)",
    body: [
      "While Bombay's Hindi-language industry became internationally synonymous with 'Indian cinema,' equally rich film cultures were thriving in Tamil, Telugu, Kannada, Malayalam, and Bengali. Telugu cinema's Vijaya Vauhini Studios produced Mayabazar in 1957, still routinely voted the greatest Telugu film ever made. In Karnataka, actor Rajkumar became a cultural institution across a five-decade career, starring in historical epics and rebellious anti-hero dramas that shaped Kannada film identity as much as any single director.",
      "These industries developed their own stars, their own studio systems, and their own storytelling instincts — often with less money and less national attention than Bombay, but no less craft. Their audiences were fiercely loyal, and the films they produced would eventually prove, decades later, that regional cinema had never been the periphery. It had simply been waiting for the rest of the country to notice.",
    ],
  },
  {
    title: "Liberalization, Multiplexes & the NRI Audience",
    range: "1990s – 2010s",
    wikiTopic: "Shah Rukh Khan",
    body: [
      "India's economic liberalization in 1991 didn't just open up the economy — it reshaped what Indian cinema looked like on screen. As satellite television and foreign brands entered Indian homes, Hindi cinema's imagination expanded with them. Films like Dilwale Dulhania Le Jayenge (1995) and Kabhi Kabhie sequels built entire narratives around the Non-Resident Indian, staging love stories across European train stations and London streets while still insisting, at their core, on the pull of home and family. Shah Rukh Khan, more than any other star, became the face of this era — an industry built increasingly for a diaspora audience as much as a domestic one.",
      "The single-screen theatre, meanwhile, was quietly dying. Multiplexes arrived through the late 1990s and 2000s, and with them came room for films that single-screen economics could never have supported — smaller, urban, dialogue-driven stories like Dil Chahta Hai (2001), which spoke directly to a young, English-educated, city-dwelling audience the industry had barely acknowledged before. By the 2010s, Hindi cinema had effectively split into two parallel tracks: the enormous star-driven blockbuster, and the mid-budget, multiplex-friendly film that could turn a profit on a fraction of the audience — a split the industry still navigates today.",
    ],
  },
  {
    title: "The Pan-India Era",
    range: "2010s – present",
    wikiTopic: "S. S. Rajamouli",
    body: [
      "For most of a century, a film's language determined its audience. Director S. S. Rajamouli helped dismantle that assumption. His 2015 film Baahubali: The Beginning was conceived from the outset to travel — shot with a scale and visual ambition designed to work regardless of which language track a viewer chose. Its sequel answered the cliffhanger question 'Why did Kattappa kill Baahubali?' to a nationwide audience that had been debating it for two years.",
      "RRR went further still, becoming the first song from an Indian production — 'Naatu Naatu' — to win the Academy Award for Best Original Song. What Rajamouli's films proved, and what KGF, Kantara, and a wave of Kannada and Telugu productions have since confirmed, is that Indian cinema's biggest stories no longer need to ask permission of any single language industry.",
    ],
  },
  {
    title: "The OTT Revolution",
    range: "2016 – present",
    wikiTopic: "Rishab Shetty",
    body: [
      "The rise of streaming platforms did something Indian cinema's century of studio systems and single-screen theatres never fully achieved: it let a film succeed on its own terms, without a wide theatrical release or a major-language backing. Kantara, a Kannada-language film rooted in Tulu Nadu folklore, reached national and international audiences largely on the strength of what streaming made possible.",
      "For independent filmmakers and regional industries that had spent decades working around the gravitational pull of Bombay, streaming offered something close to a level playing field. The story of Indian cinema's next chapter is still being written — but for the first time in over a hundred years, it's being written in every language at once.",
    ],
  },
];

export default async function HistoryPage() {
  const eraData = await Promise.all(
    ERAS.map(async (era) => ({
      ...era,
      wiki: await getWikipediaSummary([era.wikiTopic]),
    }))
  );

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <div className="font-cinzel text-gold text-xs tracking-widest mb-3">1913 – PRESENT</div>
      <h1 className="font-display text-5xl mb-4">History of Indian Cinema</h1>
      <p className="text-xl text-bronze mb-14 leading-relaxed">
        A century of gods on screen, songs that outlived their films, and an industry
        that kept reinventing what it meant to tell a story in India.
      </p>

      <div className="space-y-16">
        {eraData.map((era) => (
          <div key={era.title}>
            <div className="font-cinzel text-gold text-xs tracking-widest mb-2">{era.range}</div>
            <h2 className="font-display text-3xl mb-6">{era.title}</h2>

            {era.wiki?.thumbnail?.source && (
              <div className="float-right ml-8 mb-4 w-64">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={era.wiki.thumbnail.source}
                  alt={era.wikiTopic}
                  className="w-full h-72 object-cover border border-sandstone"
                />
                <p className="text-xs text-bronze mt-1">{era.wikiTopic} — Wikipedia, CC BY-SA</p>
              </div>
            )}

            {era.body.map((p, i) => (
              <p key={i} className="text-lg leading-relaxed mb-4">
                {p}
              </p>
            ))}
            <div className="clear-both" />
          </div>
        ))}
      </div>

      <p className="mt-4 text-bronze italic">
        See the Timeline for a chronological, film-linked view of these milestones.
      </p>
    </div>
  );
}