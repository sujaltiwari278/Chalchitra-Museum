"use client";
import { useEffect, useState } from "react";
import { API_BASE, getLanguages, getEras, getMovies, searchMovies } from "@/lib/api";
import MovieCard from "@/components/MovieCard";

export default function MoviesPage() {
  const [movies, setMovies] = useState([]);
  const [languages, setLanguages] = useState([]);
  const [eras, setEras] = useState([]);
  const [q, setQ] = useState("");
  const [language, setLanguage] = useState("");
  const [era, setEra] = useState("");

  useEffect(() => {
    getLanguages().then(setLanguages);
    getEras().then(setEras);
    fetchMovies();
  }, []);

  async function fetchMovies() {
    if (q.trim()) {
      const results = await searchMovies(q);
      setMovies(Array.isArray(results) ? results : []);
      return;
    }
    const params = new URLSearchParams();
    params.set("limit", "1000");
    if (language) params.set("language", language);
    if (era) params.set("era", era);
    const results = await getMovies(`?${params.toString()}`);
    setMovies(Array.isArray(results) ? results : []);
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <div className="w-10 h-[3px] bg-crimson mb-4" />
      <p className="font-cinzel text-xs tracking-[4px] text-bronze mb-3">THE FULL COLLECTION</p>
      <h1 className="font-display text-4xl mb-8 text-brown">The Movie Archive</h1>

      <div className="flex flex-wrap gap-4 mb-10">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search by title..."
          className="border border-bronze bg-[#fffdf8] px-4 py-2 font-body focus:outline-none focus:border-marquee transition"
        />
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="border border-bronze bg-[#fffdf8] px-4 py-2 font-body focus:outline-none focus:border-marquee transition"
        >
          <option value="">All Languages</option>
          {languages.map((l) => (
            <option key={l} value={l}>{l}</option>
          ))}
        </select>
        <select
          value={era}
          onChange={(e) => setEra(e.target.value)}
          className="border border-bronze bg-[#fffdf8] px-4 py-2 font-body focus:outline-none focus:border-marquee transition"
        >
          <option value="">All Eras</option>
          {eras.map((e) => (
            <option key={e} value={e}>{e}</option>
          ))}
        </select>
        <button
          onClick={fetchMovies}
          className="marquee-chip bg-maroon text-marquee px-6 py-2 font-cinzel text-sm hover:bg-crimson transition"
        >
          🎬 Search
        </button>
      </div>

      {movies.length === 0 ? (
        <p className="text-bronze">No movies found.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-7">
          {movies.map((m) => (
            <MovieCard key={m.id} movie={m} />
          ))}
        </div>
      )}
    </div>
  );
}
