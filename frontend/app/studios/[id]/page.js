import { Suspense } from "react";
import { getStudio } from "@/lib/api";
import { getWikipediaSummary } from "@/lib/wikipedia";
import MovieCard from "@/components/MovieCard";
import { WikiExtractStream, WikiSkeleton } from "@/components/WikiStream";

export default async function StudioDetail({ params }) {
  const s = await getStudio(params.id);
  if (!s) {
    return <p className="max-w-4xl mx-auto px-6 py-20 text-bronze">Studio not found.</p>;
  }
  const wiki = await getWikipediaSummary([s.name]);

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <div className="spotlight-glow relative flex flex-wrap gap-9 curtain-gradient border border-gold/40 p-8 marquee-lights">
        {wiki?.thumbnail?.source && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={wiki.thumbnail.source} alt={s.name} className="w-40 h-40 object-cover border border-gold/30 flex-shrink-0 shadow-[0_0_30px_rgba(0,0,0,0.5)]" />
        )}
        <div className="relative flex-1 min-w-[280px] text-ivory">
          <h1 className="font-display text-4xl mb-2">{s.name}</h1>
          <div className="text-marquee mb-4 font-cinzel text-xs tracking-widest">Founded {s.founded_year}</div>
          <p className="text-lg leading-relaxed text-sandstone/95">{s.bio}</p>
        </div>
      </div>
      <Suspense fallback={<WikiSkeleton />}>
        <WikiExtractStream wikiTitle={wiki?.title} url={wiki?.content_urls?.desktop?.page} />
      </Suspense>
      <div className="w-10 h-[3px] bg-crimson mt-10 mb-4" />
      <h2 className="font-display text-2xl mb-6 text-brown">Filmography</h2>
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
