export default function MovieCard({ movie }) {
  if (!movie || movie.id == null) return null;

  return (
    <a
      href={`/movies/${movie.id}`}
      className="group block bg-[#fffdf8] border border-sandstone hover:border-marquee shadow-sm hover:shadow-[0_0_24px_rgba(242,167,27,0.35)] hover:-translate-y-1.5 transition-all duration-300"
    >
      <div className="relative aspect-[2/3] bg-gradient-to-br from-sandstone to-bronze/40 flex items-center justify-center text-center p-2 font-body text-brown overflow-hidden">
        {movie.poster_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={movie.poster_url}
            alt={movie.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        ) : (
          <>
            <span className="absolute top-2 left-2 text-lg opacity-30">🎬</span>
            {movie.title}
          </>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
      <div className="p-4 border-t border-sandstone/60 group-hover:border-marquee/40 transition-colors">
        <h3 className="font-display text-xl group-hover:text-crimson transition-colors">
          {movie.title}
        </h3>
        <span className="text-bronze text-sm">
          {movie.release_year ?? ""} &middot; {movie.era ?? ""}
        </span>
      </div>
    </a>
  );
}
