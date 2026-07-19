import Link from "next/link";
import { getPerson } from "@/lib/api";
import { getWikipediaSummary, getWikipediaFullExtract } from "@/lib/wikipedia";
import WikipediaFullCard from "@/components/WikipediaFullCard";

export default async function PersonDetail({ params }) {
  const p = await getPerson(params.id);

  if (!p) {
    return <p className="max-w-4xl mx-auto px-6 py-20 text-bronze">Person not found.</p>;
  }

  const wiki = await getWikipediaSummary([p.name]);
  const fullText = wiki ? await getWikipediaFullExtract(wiki.title) : null;

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <div className="flex flex-wrap gap-9 bg-[#fffdf8] border border-sandstone p-8">
        <div className="w-52 aspect-square bg-sandstone flex-shrink-0 flex items-center justify-center text-center p-2">
          {p.photo_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={p.photo_url} alt={p.name} className="w-full h-full object-cover" />
          ) : (
            p.name
          )}
        </div>
        <div className="flex-1 min-w-[280px]">
          <h1 className="font-display text-4xl mb-3">{p.name}</h1>
          <p className="text-lg leading-relaxed">{p.bio}</p>
        </div>
      </div>
      <WikipediaFullCard text={fullText} url={wiki?.content_urls?.desktop?.page} />

      <h2 className="font-display text-2xl mt-12 mb-6">Filmography</h2>
      {p.filmography.length === 0 ? (
        <p className="text-bronze">No credits recorded yet.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          {p.filmography.map((f) => (
            <Link
              key={`${f.id}-${f.role}`}
              href={`/movies/${f.id}`}
              className="block bg-[#fffdf8] border border-sandstone p-4 hover:border-gold"
            >
              <div className="font-display text-lg">{f.title}</div>
              <div className="text-bronze text-sm">
                {f.release_year} &middot; {f.role}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
