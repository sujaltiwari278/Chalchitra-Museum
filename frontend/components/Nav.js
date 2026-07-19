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
    <div className="border-b-4 border-gold bg-maroon text-ivory sticky top-0 z-50">
      <nav className="flex items-center justify-between gap-4 px-6 md:px-12 py-4 flex-wrap">
        <Link href="/" className="font-display text-2xl text-gold">
          🎞 Chalchitra Museum
        </Link>
        <div className="flex-1 max-w-md min-w-[180px]">
          <GlobalSearch />
        </div>
        <div className="flex items-center gap-6">
          <Link href="/movies" className="hidden sm:inline hover:text-gold">
            Movies
          </Link>
          <Link href="/about" className="hidden sm:inline hover:text-gold">
            About
          </Link>
          <button
            onClick={() => setOpen(!open)}
            className="font-cinzel text-sm border border-gold px-4 py-2 hover:bg-gold hover:text-maroon transition"
          >
            {open ? "Close" : "Explore"}
          </button>
        </div>
      </nav>

      {open && (
        <div className="bg-brown text-ivory px-6 md:px-12 py-8 grid grid-cols-2 md:grid-cols-4 gap-8">
          {groups.map((g) => (
            <div key={g.label}>
              <div className="font-cinzel text-gold text-xs mb-3 tracking-widest">
                {g.label.toUpperCase()}
              </div>
              <ul className="space-y-2">
                {g.links.map(([label, href]) => (
                  <li key={href}>
                    <Link
                      href={href}
                      onClick={() => setOpen(false)}
                      className="font-body text-lg hover:text-gold"
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