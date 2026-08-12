import Link from "next/link";
import { getFestivals } from "@/lib/api";

export default async function FestivalsPage() {
  const festivals = await getFestivals();

  return (
    <div className="max-w-4xl mx-auto px-6 py-16">
      <div className="w-10 h-[3px] bg-crimson mb-4" />
      <h1 className="font-display text-4xl mb-2 text-brown">Film Festivals</h1>
      <p className="text-bronze mb-10">
        Indian and international festivals that showcase Indian cinema.
      </p>

      {festivals.length === 0 ? (
        <p className="text-bronze">No festivals recorded yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {festivals.map((f) => (
            <Link
              key={f.id}
              href={`/film-festivals/${f.id}`}
              className="group bg-[#fffdf8] border border-sandstone hover:border-marquee hover:shadow-[0_0_18px_rgba(242,167,27,0.3)] p-6 transition-all"
            >
              <div className="font-display text-2xl group-hover:text-crimson transition-colors">{f.name}</div>
              <div className="text-bronze">{f.location} &middot; Founded {f.founded_year}</div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
