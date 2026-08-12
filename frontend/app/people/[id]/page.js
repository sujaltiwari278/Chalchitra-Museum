import { Suspense } from "react";
import { getPerson } from "@/lib/api";
import WikiStream, { WikiSkeleton } from "@/components/WikiStream";

export default async function PersonDetail({ params }) {
  const p = await getPerson(params.id);

  if (!p) {
    return <p className="max-w-4xl mx-auto px-6 py-20 text-bronze">Person not found.</p>;
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <div className="spotlight-glow relative flex flex-wrap gap-9 curtain-gradient border border-gold/40 p-8 marquee-lights">
        <div className="w-52 aspect-square bg-gradient-to-br from-sandstone to-bronze/40 flex-shrink-0 flex items-center justify-center text-center p-2 shadow-[0_0_30px_rgba(0,0,0,0.5)] border border-gold/30">
          {p.photo_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={p.photo_url} alt={p.name} className="w-full h-full object-cover" />
          ) : (
            <span className="text-brown">{p.name}</span>
          )}
        </div>
        <div className="relative flex-1 min-w-[280px] text-ivory">
          <h1 className="font-display text-4xl mb-3">{p.name}</h1>
          <p className="text-lg leading-relaxed text-sandstone/95">{p.bio}</p>
        </div>
      </div>
      <Suspense fallback={<WikiSkeleton />}>
        <WikiStream candidates={[p.name]} />
      </Suspense>

      <div className="w-10 h-[3px] bg-crimson mt-12 mb-4" />
      <h2 className="font-display text-2xl mb-6 text-brown">Filmography</h2>
      {p.filmography.length === 0 ? (
        <p className="text-bronze">No credits recorded yet.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          {p.filmography.map((f) => (
            <a
              key={`${f.id}-${f.role}`}
              href={`/movies/${f.id}`}
              className="group block bg-[#fffdf8] border border-sandstone hover:border-marquee hover:shadow-[0_0_18px_rgba(242,167,27,0.3)] transition-all p-4"
            >
              <div className="font-display text-lg group-hover:text-crimson transition-colors">{f.title}</div>
              <div className="text-bronze text-sm">
                {f.release_year} &middot; {f.role}
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
