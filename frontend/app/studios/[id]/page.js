import { getStudio } from "@/lib/api";
import { getWikipediaSummary, getWikipediaFullExtract } from "@/lib/wikipedia";
import MovieCard from "@/components/MovieCard";
import WikipediaFullCard from "@/components/WikipediaFullCard";

export default async function StudioDetail({ params }) {
  const s = await getStudio(params.id);
  if (!s) {
    return <p className="max-w-4xl mx-auto px-6 py-20 text-bronze">Studio not found.</p>;
  }
  const wiki = await getWikipediaSummary([s.name]);
  const fullText = wiki ? await getWikipediaFullExtract(wiki.title) : null;

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <div className="flex flex-wrap gap-9 bg-[#fffdf8] border border-sandstone p-8">
        {wiki?.thumbnail?.source && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={wiki.thumbnail.source} alt={s.name} className="w-40 h-40 object-cover border border-sandstone flex-shrink-0" />
        )}
        <div className="flex-1 min-w-[280px]">
          <h1 className="font-display text-4xl mb-2">{s.name}</h1>
          <div className="text-bronze mb-4">Founded {s.founded_year}</div>
          <p className="text-lg leading-relaxed">{s.bio}</p>
        </div>
      </div>
      <WikipediaFullCard text={fullText} url={wiki?.content_urls?.desktop?.page} />
      <h2 className="font-display text-2xl mb-6 mt-10">Filmography</h2>
      {s.movies.length === 0 ? (
        <p className="text-bronze">No films recorded yet.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          {s.movies.map((m) => <MovieCard key={m.id} movie={m} />)}
        </div>
      )}
    </div>
  );
}
