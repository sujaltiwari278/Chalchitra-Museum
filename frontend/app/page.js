import Link from "next/link";
import { getTrivia } from "@/lib/api";

export default async function Home() {
  const trivia = await getTrivia();
  const dayOfYear = Math.floor((Date.now() - new Date(new Date().getFullYear(), 0, 0)) / 86400000);
  const fact = trivia.length ? trivia[dayOfYear % trivia.length] : null;

  return (
    <>
      <section className="relative min-h-[50vh] flex items-center justify-center bg-[#161008] text-ivory text-center px-6 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_40%,rgba(201,162,75,0.15),transparent_65%)]" />
        <div className="relative max-w-xl">
          <div className="w-2 h-2 rounded-full bg-gold mx-auto mb-8 animate-pulse" />
          <p className="font-cinzel text-xs tracking-[8px] text-gold mb-6">CHALCHITRA MUSEUM</p>
          <p className="font-display text-3xl leading-relaxed text-sandstone mb-4">
            You are standing at the entrance of a century.
          </p>
          <p className="text-lg text-sandstone/70 leading-relaxed italic">
            Somewhere behind you, in a room you haven't entered yet, a projector is
            still running — the same reel it has run since 1913, patiently, for no
            one and for everyone.
          </p>
        </div>
      </section>

      <section className="bg-[#f6efe1] px-2 py-20">
        <div className="max-w-2xl mx-auto">
          <p className="font-cinzel text-xs tracking-[4px] text-bronze mb-3">HALL I &middot; 1913 &middot; EXHIBIT No. 001</p>
          <h2 className="font-display text-4xl mb-6 text-brown">Before there was sound</h2>
          <p className="text-lg leading-relaxed text-brown/90 mb-5">
            A photographer named Dadasaheb Phalke sold his wife's jewelry to prove that
            Indian gods could live on a screen the way they had always lived on temple
            walls — painted, worshipped, unmoving until now. He had never made a film.
            He barely knew how the camera worked. He learned by ruining reel after reel
            of borrowed stock, alone, in a country that had not yet decided cinema was
            worth the risk.
          </p>
          <p className="text-lg leading-relaxed text-brown/90 mb-6">
            The result, <em>Raja Harishchandra</em>, had no female actors — the roles
            were played by men, because acting was still considered beneath a woman's
            dignity — no dialogue, and no music track. Only a room full of strangers,
            watching light move on a wall, together, for the first time in this
            country's history. None of them knew they were witnessing the birth of
            something that would outlive every person in that theatre.
          </p>
          <Link href="/history" className="font-cinzel text-sm text-maroon border-b border-maroon/40 hover:border-maroon">
            Examine the original exhibit →
          </Link>
        </div>
      </section>


      {fact && (
        <section className="bg-maroon text-ivory px-2 py-20">
          <div className="max-w-xl mx-auto border border-gold/50 p-10 text-center">
            <p className="font-cinzel text-xs tracking-[4px] text-gold mb-4">FROM THE ARCHIVE CASE</p>
            <p className="font-display text-2xl leading-relaxed mb-4">{fact.fact}</p>
            {fact.movie_title && (
              <Link href={`/movies/${fact.movie_id}`} className="text-sandstone text-sm underline hover:text-gold">
                {fact.movie_title}
              </Link>
            )}
            <p className="text-sandstone/50 text-xs mt-6 italic">
              A different case is unlocked each day. Return tomorrow for another.
            </p>
          </div>
        </section>
      )}

      <section className="bg-[#f6efe1] px-6 py-20">
        <div className="max-w-2xl mx-auto">
          <p className="font-cinzel text-xs tracking-[4px] text-bronze mb-3">HALL II &middot; THE CUSTODIANS &middot; EXHIBIT No. 014</p>
          <h2 className="font-display text-4xl mb-6 text-brown">The faces behind the frame</h2>
          <p className="text-lg leading-relaxed text-brown/90 mb-5">
            Satyajit Ray sold his own record collection to finish a film about a starving
            village that no studio would fund. Amitabh Bachchan spoke a country's rage back
            to it so precisely that strangers began quoting his silences as much as his lines.
            Somewhere between Ray's patience and Bachchan's fury lies most of what this
            country has ever wanted cinema to say for it.
          </p>
          <p className="text-lg leading-relaxed text-brown/90 mb-6">
            Every name kept in this archive paid for its place here — in mortgaged homes,
            in years without recognition, in performances given to audiences who had never
            left their own district and would never leave it, and who needed, just once
            a week, somewhere else to be.
          </p>
          <Link href="/directors" className="font-cinzel text-sm text-maroon border-b border-maroon/40 hover:border-maroon">
            Meet the people who built this industry →
          </Link>
        </div>
      </section>

      <section className="bg-brown text-ivory px-6 py-20 text-center">
        <p className="font-cinzel text-xs tracking-[4px] text-gold mb-6">HALL III &middot; THE COLLECTION</p>
        <p className="font-display text-4xl leading-relaxed max-w-2xl mx-auto mb-6">
          Five languages. Six eras. One hundred and fifty films,
          each one somebody's entire career.
        </p>
        <p className="text-sandstone/70 max-w-xl mx-auto mb-10 italic">
          Some of these films were seen by millions on their opening weekend.
          Others were seen by almost no one, and are remembered only because
          this archive refused to let them go.
        </p>
        <Link href="/movies" className="font-cinzel text-sm border-b border-gold/60 hover:border-gold">
          Browse the full collection →
        </Link>
      </section>

      <section className="bg-[#f6efe1] px-6 py-20">
        <div className="max-w-md mx-auto text-center">
          <p className="font-cinzel text-xs tracking-[4px] text-bronze mb-6">BEFORE YOU LEAVE</p>
          <p className="text-brown/70 mb-6 italic">A few more wings, if you have the time.</p>
          <div className="flex flex-col gap-3 font-display text-xl text-brown">
            <Link href="/timeline" className="hover:text-maroon">The Timeline Room</Link>
            <Link href="/studios" className="hover:text-maroon">The Studio Archives</Link>
            <Link href="/trivia" className="hover:text-maroon">The Trivia Cabinet</Link>
            <Link href="/collections" className="hover:text-maroon">Curated Collections</Link>
          </div>
        </div>
      </section>
    </>
  );
}