function renderExtract(text) {
  return text.split("\n").map((line, i) => {
    const h3 = line.match(/^===\s*(.+?)\s*===$/);
    const h2 = line.match(/^==\s*(.+?)\s*==$/);
    if (h3) {
      return (
        <h4 key={i} className="font-display text-lg mt-4 mb-1 text-maroon">
          {h3[1]}
        </h4>
      );
    }
    if (h2) {
      return (
        <h3 key={i} className="font-display text-xl mt-6 mb-2 text-maroon border-b border-sandstone pb-1">
          {h2[1]}
        </h3>
      );
    }
    if (!line.trim()) return null;
    return (
      <p key={i} className="leading-relaxed mb-3">
        {line}
      </p>
    );
  });
}

export default function WikipediaFullCard({ text, url }) {
  if (!text) return null;
  return (
    <div className="mt-6 bg-[#fffdf8] border border-sandstone p-6">
      <div className="font-cinzel text-xs text-gold tracking-widest mb-4">FULL DESCRIPTION — WIKIPEDIA</div>
      <div>{renderExtract(text)}</div>
      {url && (
        <a href={url} target="_blank" rel="noopener noreferrer"
           className="inline-block mt-4 text-xs text-bronze underline hover:text-gold">
          Source: Wikipedia — CC BY-SA 4.0
        </a>
      )}
    </div>
  );
}