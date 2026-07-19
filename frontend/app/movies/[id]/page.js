import { getMovie } from "@/lib/api";
import { getWikipediaSummary, getWikipediaFullExtract } from "@/lib/wikipedia";
import WikipediaFullCard from "@/components/WikipediaFullCard";

export default async function MovieDetail({ params }) {
  const m = await getMovie(params.id);

  if (!m) {
    return <p className="max-w-4xl mx-auto px-6 py-20 text-bronze">Movie not found.</p>;
  }

  const wiki = await getWikipediaSummary([
    `${m.title} (${m.release_year} film)`,
    `${m.title} (film)`,
    m.title,
  ]);
  const fullText = wiki ? await getWikipediaFullExtract(wiki.title) : null;

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <div className="flex flex-wrap gap-9 bg-[#fffdf8] border border-sandstone p-8">
        <div className="w-64 aspect-[2/3] bg-sandstone flex-shrink-0 flex items-center justify-center text-center p-2">
          {m.poster_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={m.poster_url} alt={m.title} className="w-full h-full object-contain" />
          ) : (
            m.title
          )}
        </div>
        <div className="flex-1 min-w-[280px]">
          <div className="font-cinzel text-gold text-xs tracking-widest mb-2">
            {m.era}
          </div>
          <h1 className="font-display text-4xl mb-2">{m.title}</h1>
          <div className="text-bronze mb-4">
            {m.release_year} &middot; {m.language} {m.runtime_minutes ? `· ${m.runtime_minutes} min` : ""}
          </div>
          {m.genre && <span className="tag">{m.genre}</span>}
          <p className="text-lg mt-4 leading-relaxed">{m.synopsis}</p>
          {m.trivia && (
            <div className="mt-2 text-bronze">
              <strong className="text-brown">Trivia:</strong> {m.trivia}
            </div>
          )}
        </div>
      </div>
      <WikipediaFullCard text={fullText} url={wiki?.content_urls?.desktop?.page} />
    </div>
  );
}
