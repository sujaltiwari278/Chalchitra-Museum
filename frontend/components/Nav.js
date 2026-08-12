"use client";
import Link from "next/link";
import { useState } from "react";
import GlobalSearch from "@/components/GlobalSearch";

const groups = [
  {
    label: "Cinema",
    links: [
      ["History", "/history"],
      ["Timeline", "/timeline"],
    ],
  },
  {
    label: "People",
    links: [
      ["Actors", "/actors"],
      ["Actresses", "/actresses"],
      ["Directors", "/directors"],
      ["Music Directors", "/music-directors"],
    ],
  },
  {
    label: "Industry",
    links: [
      ["Studios", "/studios"],
      ["Film Festivals", "/film-festivals"],
      ["Box Office", "/box-office"],
    ],
  },
  {
    label: "Explore",
    links: [
      ["Trivia", "/trivia"],
      ["Collections", "/collections"],
    ],
  },
];

export default function Nav() {
  const [open, setOpen] = useState(false);

  return (
    <div className="marquee-lights relative bg-gradient-to-r from-midnight via-maroon to-midnight text-ivory sticky top-0 z-50 shadow-[0_4px_24px_rgba(0,0,0,0.4)]">
      <nav className="flex items-center justify-between gap-4 px-6 md:px-12 py-4 flex-wrap">
        <Link href="/" className="font-display text-2xl text-marquee flex items-center gap-2">
          <span className="inline-block animate-spin-slow">🎞</span>
          Chalchitra Museum
        </Link>
        <div className="flex-1 max-w-md min-w-[180px]">
          <GlobalSearch />
        </div>
        <div className="flex items-center gap-6">
          <Link href="/movies" className="hidden sm:inline hover:text-marquee transition">
            Movies
          </Link>
          <Link href="/about" className="hidden sm:inline hover:text-marquee transition">
            About
          </Link>
          <button
            onClick={() => setOpen(!open)}
            className="marquee-chip font-cinzel text-sm border border-gold px-4 py-2 hover:bg-gold hover:text-maroon transition rounded-sm"
          >
            {open ? "Close" : "Explore"}
          </button>
        </div>
      </nav>

      {open && (
        <div className="curtain-gradient text-ivory px-6 md:px-12 py-8 grid grid-cols-2 md:grid-cols-4 gap-8 border-t border-gold/30">
          {groups.map((g) => (
            <div key={g.label}>
              <div className="font-cinzel text-marquee text-xs mb-3 tracking-widest">
                {g.label.toUpperCase()}
              </div>
              <ul className="space-y-2">
                {g.links.map(([label, href]) => (
                  <li key={href}>
                    <Link
                      href={href}
                      onClick={() => setOpen(false)}
                      className="font-body text-lg hover:text-marquee transition"
                    >
                      {label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}