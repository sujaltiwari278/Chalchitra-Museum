import Link from "next/link";
import { getFestival } from "@/lib/api";

export default async function FestivalDetail({ params }) {
  const f = await getFestival(params.id);

  if (!f) {
    return <p className="max-w-4xl mx-auto px-6 py-20 text-bronze">Festival not found.</p>;
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-16">
      <div className="w-10 h-[3px] bg-crimson mb-4" />
      <h1 className="font-display text-4xl mb-2 text-brown">{f.name}</h1>
      <div className="text-bronze mb-6">{f.location} &middot; Founded {f.founded_year}</div>
      <p className="text-lg leading-relaxed mb-10">{f.bio}</p>

      <h2 className="font-display text-2xl mb-6 text-brown">Films Featured</h2>
      {f.selections.length === 0 ? (
        <p className="text-bronze">No selections recorded yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {f.selections.map((s) => (
            <Link
              key={s.id}
              href={`/movies/${s.id}`}
              className="group bg-[#fffdf8] border border-sandstone hover:border-marquee hover:shadow-[0_0_18px_rgba(242,167,27,0.3)] p-5 transition-all"
            >
              <div className="font-display text-xl group-hover:text-crimson transition-colors">{s.title}</div>
              <div className="text-bronze text-sm">
                {s.release_year} &middot; {s.selection_type}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
