import Link from "next/link";
import { getStudios } from "@/lib/api";

export default async function StudiosPage() {
  const studios = await getStudios();

  return (
    <div className="max-w-4xl mx-auto px-6 py-16">
      <h1 className="font-display text-4xl mb-2">Studios & Production Houses</h1>
      <p className="text-bronze mb-10">The studios that built Indian cinema.</p>

      {studios.length === 0 ? (
        <p className="text-bronze">No studios recorded yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {studios.map((s) => (
            <Link
              key={s.id}
              href={`/studios/${s.id}`}
              className="bg-[#fffdf8] border border-sandstone p-6 hover:border-gold transition"
            >
              <div className="font-display text-2xl">{s.name}</div>
              <div className="text-bronze">Founded {s.founded_year}</div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
