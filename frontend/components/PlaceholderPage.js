export default function PlaceholderPage({ eyebrow, title, intro, features, phase }) {
  return (
    <div className="max-w-4xl mx-auto px-6 py-20">
      <div className="font-cinzel text-gold text-xs tracking-widest mb-3">
        {eyebrow?.toUpperCase()}
      </div>
      <h1 className="font-display text-5xl mb-6">{title}</h1>
      <p className="text-xl text-brown/80 mb-10 leading-relaxed">{intro}</p>

      <div className="bg-[#fffdf8] border border-sandstone p-8">
        <div className="font-cinzel text-sm text-bronze mb-4 tracking-widest">
          PLANNED FOR THIS SECTION
        </div>
        <ul className="space-y-2 text-lg">
          {features.map((f) => (
            <li key={f} className="flex gap-3">
              <span className="text-gold">✦</span> {f}
            </li>
          ))}
        </ul>
      </div>

      <p className="mt-8 text-bronze italic">
        This section is part of the site structure now and will be built out with real
        data and interactivity in {phase}.
      </p>
    </div>
  );
}
