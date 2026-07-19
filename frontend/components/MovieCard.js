import Link from "next/link";

export default function MovieCard({ movie }) {
  return (
    <Link
      href={`/movies/${movie.id}`}
      className="block bg-[#fffdf8] border border-sandstone shadow-sm hover:-translate-y-1 transition-transform"
    >
      <div className="aspect-[2/3] bg-sandstone flex items-center justify-center text-center p-2 font-body text-brown">
        {movie.poster_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={movie.poster_url} alt={movie.title} className="w-full h-full object-cover" />
        ) : (
          movie.title
        )}
      </div>
      <div className="p-4">
        <h3 className="font-display text-xl">{movie.title}</h3>
        <span className="text-bronze text-sm">
          {movie.release_year ?? ""} &middot; {movie.era ?? ""}
        </span>
      </div>
    </Link>
  );
}
