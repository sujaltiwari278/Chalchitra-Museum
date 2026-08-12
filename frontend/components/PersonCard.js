export default function PersonCard({ person }) {
  return (
    <a
      href={`/people/${person.id}`}
      className="group block bg-[#fffdf8] border border-sandstone hover:border-marquee shadow-sm hover:shadow-[0_0_24px_rgba(242,167,27,0.35)] hover:-translate-y-1.5 transition-all duration-300"
    >
      <div className="relative aspect-square bg-gradient-to-br from-sandstone to-bronze/40 flex items-center justify-center text-center p-2 font-body text-brown overflow-hidden">
        {person.photo_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={person.photo_url}
            alt={person.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        ) : (
          person.name
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
      <div className="p-4 border-t border-sandstone/60 group-hover:border-marquee/40 transition-colors">
        <h3 className="font-display text-xl group-hover:text-crimson transition-colors">
          {person.name}
        </h3>
      </div>
    </a>
  );
}
