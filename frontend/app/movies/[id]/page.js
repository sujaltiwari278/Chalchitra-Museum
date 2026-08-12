import { Suspense } from "react";
import { getMovie } from "@/lib/api";
import WikiStream, { WikiSkeleton } from "@/components/WikiStream";

export default async function MovieDetail({ params }) {
  const m = await getMovie(params.id);

  if (!m) {
    return <p className="max-w-4xl mx-auto px-6 py-20 text-bronze">Movie not found.</p>;
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <div className="spotlight-glow relative flex flex-wrap gap-9 curtain-gradient border border-gold/40 p-8 marquee-lights">
        <div className="w-64 aspect-[2/3] bg-gradient-to-br from-sandstone to-bronze/40 flex-shrink-0 flex items-center justify-center text-center p-2 shadow-[0_0_30px_rgba(0,0,0,0.5)] border border-gold/30">
          {m.poster_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={m.poster_url} alt={m.title} className="w-full h-full object-contain" />
          ) : (
            <span className="text-brown">{m.title}</span>
          )}
        </div>
        <div className="relative flex-1 min-w-[280px] text-ivory">
          <div className="font-cinzel text-marquee text-xs tracking-widest mb-2">
            {m.era}
          </div>
          <h1 className="font-display text-4xl mb-2">{m.title}</h1>
          <div className="text-sandstone/80 mb-4">
            {m.release_year} &middot; {m.language} {m.runtime_minutes ? `· ${m.runtime_minutes} min` : ""}
          </div>
          {m.genre && <span className="tag">{m.genre}</span>}
          <p className="text-lg mt-4 leading-relaxed text-sandstone/95">{m.synopsis}</p>
          {m.trivia && (
            <div className="mt-2 text-sandstone/80">
              <strong className="text-marquee">Trivia:</strong> {m.trivia}
            </div>
          )}
        </div>
      </div>
      <Suspense fallback={<WikiSkeleton />}>
        <WikiStream
          candidates={[
            `${m.title} (${m.release_year} film)`,
            `${m.title} (film)`,
            m.title,
          ]}
        />
      </Suspense>
    </div>
  );
}
