import { getWikipediaSummary, getWikipediaFullExtract } from "@/lib/wikipedia";
import WikipediaFullCard from "@/components/WikipediaFullCard";

export function WikiSkeleton() {
  return (
    <div className="mt-6 bg-[#fffdf8] border border-sandstone p-6 animate-pulse">
      <div className="h-3 w-40 bg-sandstone/60 mb-4" />
      <div className="h-3 w-full bg-sandstone/40 mb-2" />
      <div className="h-3 w-full bg-sandstone/40 mb-2" />
      <div className="h-3 w-2/3 bg-sandstone/40" />
    </div>
  );
}

// Streams in after the main page content, so slow external Wikipedia
// calls never block the fast, local-data hero from rendering.
export default async function WikiStream({ candidates }) {
  const wiki = await getWikipediaSummary(candidates);
  const fullText = wiki ? await getWikipediaFullExtract(wiki.title) : null;
  return <WikipediaFullCard text={fullText} url={wiki?.content_urls?.desktop?.page} />;
}

// For pages that already needed the summary (e.g. for a thumbnail) before
// render — only the heavier full-extract call gets streamed in separately.
export async function WikiExtractStream({ wikiTitle, url }) {
  const fullText = wikiTitle ? await getWikipediaFullExtract(wikiTitle) : null;
  return <WikipediaFullCard text={fullText} url={url} />;
}
