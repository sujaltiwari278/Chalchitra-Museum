"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { getTrivia, getTriviaCategories } from "@/lib/api";

function dailyPick(all, count) {
  if (all.length <= count) return all;
  const dayOfYear = Math.floor(
    (Date.now() - new Date(new Date().getFullYear(), 0, 0)) / 86400000
  );
  const start = dayOfYear % all.length;
  const rotated = [...all.slice(start), ...all.slice(0, start)];
  return rotated.slice(0, count);
}

export default function TriviaPage() {
  const [allCards, setAllCards] = useState([]);
  const [categories, setCategories] = useState([]);
  const [category, setCategory] = useState("");

  useEffect(() => {
    getTriviaCategories().then(setCategories);
    getTrivia().then(setAllCards);
  }, []);

  const cards = category
    ? allCards.filter((c) => c.category === category)
    : dailyPick(allCards, 10);

  return (
    <div className="max-w-4xl mx-auto px-6 py-16">
      <h1 className="font-display text-4xl mb-2">Trivia</h1>
      <p className="text-bronze mb-2">
        Rare facts, production stories, and hidden details from Indian cinema.
      </p>
      {!category && (
        <p className="text-bronze text-sm mb-8 italic">
          10 facts, refreshed daily — check back tomorrow for a new set.
        </p>
      )}
      {category && <div className="mb-8" />}

      <div className="flex gap-3 mb-10 flex-wrap">
        <button
          onClick={() => setCategory("")}
          className={`font-cinzel text-xs px-4 py-2 border ${category === "" ? "bg-maroon text-gold border-maroon" : "border-bronze text-bronze"}`}
        >
          ALL
        </button>
        {categories.map((c) => (
          <button
            key={c}
            onClick={() => setCategory(c)}
            className={`font-cinzel text-xs px-4 py-2 border ${category === c ? "bg-maroon text-gold border-maroon" : "border-bronze text-bronze"}`}
          >
            {c.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="space-y-5">
        {cards.length === 0 ? (
          <p className="text-bronze">No trivia in this category yet.</p>
        ) : (
          cards.map((c) => (
            <div key={c.id} className="bg-[#fffdf8] border border-sandstone p-6">
              <p className="text-lg leading-relaxed mb-2">{c.fact}</p>
              <div className="text-bronze text-sm">
                {c.category}
                {c.movie_title && (
                  <>
                    {" "}
                    &middot;{" "}
                    <Link href={`/movies/${c.movie_id}`} className="underline hover:text-gold">
                      {c.movie_title}
                    </Link>
                  </>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}