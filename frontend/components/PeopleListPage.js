import { getPeople } from "@/lib/api";
import PersonCard from "@/components/PersonCard";

export default async function PeopleListPage({ eyebrow, title, intro, role, gender }) {
  const people = await getPeople(role, gender);

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <div className="w-10 h-[3px] bg-crimson mb-4" />
      <div className="font-cinzel text-marquee text-xs tracking-widest mb-3">
        {eyebrow?.toUpperCase()}
      </div>
      <h1 className="font-display text-4xl mb-2 text-brown">{title}</h1>
      <p className="text-bronze mb-10">{intro}</p>

      {people.length === 0 ? (
        <p className="text-bronze">
          No entries yet — this section grows as more people are added to the archive.
        </p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
          {people.map((p) => (
            <PersonCard key={p.id} person={p} />
          ))}
        </div>
      )}
    </div>
  );
}
