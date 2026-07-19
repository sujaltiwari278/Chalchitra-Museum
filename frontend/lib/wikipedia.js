async function fetchSummary(title) {
  try {
    const res = await fetch(
      `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(title.replace(/ /g, "_"))}`,
      { cache: "no-store" }
    );
    if (!res.ok) return null;
    const data = await res.json();
    if (data.type === "disambiguation" || !data.extract) return null;
    return data;
  } catch {
    return null;
  }
}

async function searchFallback(query) {
  try {
    const res = await fetch(
      `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&format=json&origin=*`,
      { cache: "no-store" }
    );
    if (!res.ok) return null;
    const data = await res.json();
    const first = data?.query?.search?.[0];
    if (!first) return null;
    const normalize = (s) => s.toLowerCase().replace(/\(.*?\)/g, "").trim();
    if (!normalize(first.title).includes(normalize(query)) && !normalize(query).includes(normalize(first.title))) {
      return null; // not actually the same subject, skip rather than show wrong content
    }
    return await fetchSummary(first.title);
  } catch {
    return null;
  }
}

export async function getWikipediaFullExtract(title) {
  try {
    const res = await fetch(
      `https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=true&titles=${encodeURIComponent(title)}&format=json&origin=*`,
      { cache: "no-store" }
    );
    if (!res.ok) return null;
    const data = await res.json();
    const page = Object.values(data?.query?.pages || {})[0];
    if (!page || page.missing || !page.extract) return null;
    let text = page.extract;

    const boilerplate = /\n==+\s*(Filmography|Awards? and honours?|Awards?|References|External links|See also|Notes|Bibliography|Further reading|Discography|Notes and references)\s*==+/i;
    const cutMatch = text.match(boilerplate);
    if (cutMatch) text = text.slice(0, cutMatch.index);

    if (text.length <= 4000) return text.trim();
    const cut = text.slice(0, 4000);
    const lastPeriod = cut.lastIndexOf(". ");
    return ((lastPeriod > 500 ? cut.slice(0, lastPeriod + 1) : cut) + " …").trim();
  } catch {
    return null;
  }
}

// Tries each candidate title in order (useful for disambiguation, e.g.
// "War (2019 film)" before falling back to just "War"), then does a
// full-text search as a last resort.
export async function getWikipediaSummary(candidates) {
  for (const title of candidates) {
    const result = await fetchSummary(title);
    if (result) return result;
  }
  return await searchFallback(candidates[0]);
}