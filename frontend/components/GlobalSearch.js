"use client";
import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { searchAll } from "@/lib/api";

export default function GlobalSearch() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState(null);
  const [focused, setFocused] = useState(false);
  const boxRef = useRef(null);

  useEffect(() => {
    if (!q.trim()) {
      setResults(null);
      return;
    }
    const t = setTimeout(() => searchAll(q).then(setResults), 300);
    return () => clearTimeout(t);
  }, [q]);

  useEffect(() => {
    function onClickOutside(e) {
      if (boxRef.current && !boxRef.current.contains(e.target)) setFocused(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  const hasResults = results && (results.movies.length > 0 || results.people.length > 0);

  return (
    <div ref={boxRef} className="relative">
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        onFocus={() => setFocused(true)}
        placeholder="Search movies, actors, directors..."
        className="w-full bg-brown/40 border border-gold/40 text-ivory placeholder-ivory/50 px-4 py-2 font-body focus:outline-none focus:border-gold"
      />
      {focused && q.trim() && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-[#fffdf8] border border-sandstone text-brown shadow-lg max-h-96 overflow-y-auto z-50">
          {!hasResults && <div className="p-4 text-bronze">No results.</div>}
          {results?.movies?.length > 0 && (
            <div>
              <div className="font-cinzel text-xs text-bronze px-4 pt-3 pb-1 tracking-widest">MOVIES</div>
              {results.movies.map((m) => (
                <Link
                  key={m.id}
                  href={`/movies/${m.id}`}
                  onClick={() => setFocused(false)}
                  className="block px-4 py-2 hover:bg-sandstone/40"
                >
                  {m.title} <span className="text-bronze text-sm">{m.release_year}</span>
                </Link>
              ))}
            </div>
          )}
          {results?.people?.length > 0 && (
            <div>
              <div className="font-cinzel text-xs text-bronze px-4 pt-3 pb-1 tracking-widest">PEOPLE</div>
              {results.people.map((p) => (
                <Link
                  key={p.id}
                  href={`/people/${p.id}`}
                  onClick={() => setFocused(false)}
                  className="block px-4 py-2 hover:bg-sandstone/40"
                >
                  {p.name}
                </Link>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
