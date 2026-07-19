import { getMovies } from "@/lib/api";
import MovieCard from "@/components/MovieCard";

export default async function CollectionsPage() {
  const movies = await getMovies("?limit=1000");

  const byEra = (era) => movies.filter((m) => m.era === era).slice(0, 12);
  const byLanguage = (lang) => movies.filter((m) => m.language === lang).slice(0, 12);

  const collections = [
    {
      title: "The Golden Age",
      description: "Classic-era Hindi cinema from the 1940s through the 1980s.",
      movies: byEra("Golden Age"),
    },
    {
      title: "Parallel Cinema & Bengali Realism",
      description: "Humanist storytelling that put Indian cinema on the world stage.",
      movies: byLanguage("Bengali"),
    },
    {
      title: "Modern & Pan-India Cinema",
      description: "2000s-2010s films that redefined Hindi and multi-language cinema.",
      movies: [...byEra("Modern Cinema"), ...byEra("Pan India Cinema")].slice(0, 12),
    },
    {
      title: "The OTT & Regional Spotlight",
      description: "Regional stories reaching national and global audiences.",
      movies: byEra("OTT Revolution"),
    },
    {
      title: "Kannada Cinema",
      description: "From classic Rajkumar-era films to modern national hits.",
      movies: byLanguage("Kannada"),
    },
    {
      title: "Telugu Cinema",
      description: "Studio-era classics through the Pan-India blockbuster era.",
      movies: byLanguage("Telugu"),
    },
  ].filter((c) => c.movies.length > 0);

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <h1 className="font-display text-4xl mb-2">Collections</h1>
      <p className="text-bronze mb-12">
        Curated groupings through Indian cinema's eras, languages, and movements.
      </p>

      <div className="space-y-14">
        {collections.map((c) => (
          <div key={c.title}>
            <h2 className="font-display text-2xl mb-1">{c.title}</h2>
            <p className="text-bronze mb-5">{c.description}</p>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
              {c.movies.map((m) => (
                <MovieCard key={m.id} movie={m} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
