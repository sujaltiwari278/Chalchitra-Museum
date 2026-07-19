export default function WikipediaSummary({ data }) {
  if (!data || !data.extract) return null;

  return (
    <div className="mt-6 bg-[#fffdf8] border border-sandstone p-6">
      <div className="font-cinzel text-xs text-gold tracking-widest mb-4">FROM WIKIPEDIA</div>
      <div className="flex gap-5 flex-wrap sm:flex-nowrap">
        {data.thumbnail?.source && (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={data.thumbnail.source}
            alt={data.title}
            className="w-28 h-28 object-cover flex-shrink-0 border border-sandstone"
          />
        )}
        <div>
          <p className="leading-relaxed">{data.extract}</p>
        </div>
      </div>
      <a
        href={data.content_urls?.desktop?.page}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block mt-4 text-xs text-bronze underline hover:text-gold"
      >
        Source: Wikipedia — CC BY-SA 4.0
      </a>
    </div>
  );
}
