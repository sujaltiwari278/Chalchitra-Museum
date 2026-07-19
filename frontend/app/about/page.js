export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-6 py-16">
      <p className="font-cinzel text-xs tracking-[4px] text-bronze mb-3">ABOUT THE MUSEUM</p>
      <h1 className="font-display text-5xl mb-8">Chalchitra Museum</h1>

      <p className="text-xl leading-relaxed text-brown/90 mb-10">
        Chalchitra Museum is a digital museum built to preserve and celebrate the
        artistic, cultural, historical, and technological journey of Indian
        filmmaking — from Raja Harishchandra in 1913 to the OTT era today.
      </p>

      <h2 className="font-display text-2xl mb-3 text-maroon">Who it's for</h2>
      <p className="text-lg leading-relaxed text-brown/90 mb-8">
        Film students, researchers, historians, journalists, and curious audiences
        alike — anyone who wants to move through Indian cinema's history the way
        they'd move through a museum: era by era, artifact by artifact, rather than
        as an endless scrolling feed.
      </p>

      <h2 className="font-display text-2xl mb-3 text-maroon">What's inside</h2>
      <p className="text-lg leading-relaxed text-brown/90 mb-8">
        A curated canon of 150 films across Hindi, Kannada, Bengali, and Telugu
        cinema, spanning silent-era classics to Pan-India blockbusters — alongside
        the people who made them, the studios that produced them, the festivals
        that selected them, and the trivia that surrounds them.
      </p>

      <h2 className="font-display text-2xl mb-3 text-maroon">How it's built</h2>
      <p className="text-lg leading-relaxed text-brown/90 mb-8">
        Movie and cast data is sourced from TMDb; biographical and historical
        context is pulled live from Wikipedia, with attribution, under its
        CC BY-SA license. The curated film list itself was hand-selected rather
        than algorithmically ranked, aiming for cultural and historical
        significance over pure popularity.
      </p>

      <h2 className="font-display text-2xl mb-3 text-maroon">A living archive</h2>
      <p className="text-lg leading-relaxed text-brown/90">
        This museum is a work in progress by design — new languages, deeper
        eras, and richer detail are added over time, the way any real archive
        keeps growing long after its doors first open.
      </p>
    </div>
  );
}