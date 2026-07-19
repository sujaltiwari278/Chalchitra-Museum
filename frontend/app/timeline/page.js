import Link from "next/link";
import { getMovies } from "@/lib/api";

const MILESTONES = [
  ["Raja Harishchandra", "India's first feature film, made by Dadasaheb Phalke."],
  ["Alam Ara", "India's first talkie, bringing sound to Indian cinema."],
  ["Awaara", "A Raj Kapoor classic that made Indian cinema a global phenomenon."],
  ["Mother India", "India's first-ever Academy Award submission."],
  ["Pather Panchali", "Satyajit Ray's debut, launching Parallel Cinema onto the world stage."],
  ["Mughal-E-Azam", "The most expensive Hindi film of its era, a Golden Age landmark."],
  ["Sholay", "The defining blockbuster of 1970s Hindi cinema."],
  ["Deewar", "Cemented the 'angry young man' archetype in Bollywood."],
  ["Mayabazar", "Widely regarded as the greatest Telugu film ever made."],
  ["Amar Akbar Anthony", "Its lost-and-found-brothers plot became a Bollywood template."],
  ["Maine Pyar Kiya", "Launched Salman Khan and defined late-80s romance."],
  ["Dilwale Dulhania Le Jayenge", "Redefined the Bollywood romance for a new generation."],
  ["Lagaan", "An Oscar-nominated epic that redefined ambition in Hindi cinema."],
  ["3 Idiots", "One of the highest-grossing Indian films of its decade."],
  ["Gangs of Wasseypur", "Reshaped Hindi crime cinema with its two-part epic scope."],
  ["Baahubali: The Beginning", "Launched the Pan-India blockbuster era."],
  ["RRR", "Won the Academy Award for Best Original Song, a first for India."],
  ["KGF: Chapter 1", "Turned Kannada cinema into a nationwide box office force."],
  ["Kantara", "Brought Karnataka folklore to a national and global audience."],
  ["12th Fail", "A modern hit built entirely on a true, unglamorous success story."],
  ["Dhurandhar", "Among the highest-grossing Hindi films ever made on release."],
];

export default async function TimelinePage() {
  const allMovies = await getMovies("?limit=1000");
  const byTitle = (t) => allMovies.find((m) => m.title === t);

  const entries = MILESTONES
    .filter((entry) => Array.isArray(entry))
    .map(([title, note]) => ({ movie: byTitle(title), note }))
    .filter((e) => e.movie)
    .sort((a, b) => (a.movie.release_year ?? 0) - (b.movie.release_year ?? 0));

  return (
    <div className="max-w-3xl mx-auto px-6 py-16">
      <h1 className="font-display text-4xl mb-2">Timeline of Indian Cinema</h1>
      <p className="text-bronze mb-10">Generation-defining films, 1913 to present.</p>

      <div className="border-l-2 border-gold ml-3">
        {entries.map(({ movie, note }) => (
          <Link
            key={movie.id}
            href={`/movies/${movie.id}`}
            className="flex gap-5 relative pl-8 pb-10 group"
          >
            <div className="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-maroon border-2 border-gold group-hover:bg-gold" />
            {movie.poster_url && (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={movie.poster_url} alt={movie.title} className="w-16 h-24 object-cover border border-sandstone flex-shrink-0" />
            )}
            <div>
              <div className="font-cinzel text-gold text-sm">{movie.release_year}</div>
              <div className="font-display text-2xl">{movie.title}</div>
              <div className="text-bronze">{note}</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}