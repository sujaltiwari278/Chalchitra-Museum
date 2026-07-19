import Link from "next/link";

export default function PersonCard({ person }) {
  return (
    <Link
      href={`/people/${person.id}`}
      className="block bg-[#fffdf8] border border-sandstone shadow-sm hover:-translate-y-1 transition-transform"
    >
      <div className="aspect-square bg-sandstone flex items-center justify-center text-center p-2 font-body text-brown">
        {person.photo_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={person.photo_url} alt={person.name} className="w-full h-full object-cover" />
        ) : (
          person.name
        )}
      </div>
      <div className="p-4">
        <h3 className="font-display text-xl">{person.name}</h3>
      </div>
    </Link>
  );
}
