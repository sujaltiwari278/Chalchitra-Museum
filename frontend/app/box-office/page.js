import { getBoxOffice } from "@/lib/api";

// Source: Wikipedia, "List of highest-grossing Indian films" (CC BY-SA 4.0).
const TOP_GROSSING = [
  { rank: 1, title: "Dangal", gross: "₹1,968–2,054 crore", language: "Hindi", year: 2016 },
  { rank: 2, title: "Dhurandhar: The Revenge", gross: "₹1,852.44 crore", language: "Hindi", year: 2026 },
  { rank: 3, title: "Baahubali 2: The Conclusion", gross: "₹1,810.43 crore", language: "Telugu", year: 2017 },
  { rank: 4, title: "Pushpa 2: The Rule", gross: "₹1,642–1,800 crore", language: "Telugu", year: 2024 },
  { rank: 5, title: "Dhurandhar", gross: "₹1,350.83–1,428 crore", language: "Hindi", year: 2025 },
  { rank: 6, title: "RRR", gross: "₹1,300–1,387 crore", language: "Telugu", year: 2022 },
  { rank: 7, title: "KGF: Chapter 2", gross: "₹1,200–1,250 crore", language: "Kannada", year: 2022 },
  { rank: 8, title: "Jawan", gross: "₹1,148.32 crore", language: "Hindi", year: 2023 },
  { rank: 9, title: "Pathaan", gross: "₹1,050.30 crore", language: "Hindi", year: 2023 },
  { rank: 10, title: "Kalki 2898 AD", gross: "₹1,042–1,100 crore", language: "Telugu", year: 2024 },
  { rank: 11, title: "Animal", gross: "₹917.82 crore", language: "Hindi", year: 2023 },
  { rank: 12, title: "Bajrangi Bhaijaan", gross: "₹900.90–969.06 crore", language: "Hindi", year: 2015 },
  { rank: 13, title: "Stree 2", gross: "₹874.58 crore", language: "Hindi", year: 2024 },
  { rank: 14, title: "Secret Superstar", gross: "₹858.43–966 crore", language: "Hindi", year: 2017 },
  { rank: 15, title: "Kantara: Chapter 1", gross: "₹850–852 crore", language: "Kannada", year: 2025 },
  { rank: 16, title: "Chhaava", gross: "₹797.34–809 crore", language: "Hindi", year: 2025 },
  { rank: 17, title: "PK", gross: "₹750.60–769.89 crore", language: "Hindi", year: 2014 },
  { rank: 18, title: "2.0", gross: "₹699.89–800 crore", language: "Tamil", year: 2018 },
  { rank: 19, title: "Gadar 2", gross: "₹691.08 crore", language: "Hindi", year: 2023 },
  { rank: 20, title: "Sultan", gross: "₹615.71–623.33 crore", language: "Hindi", year: 2016 },
  { rank: 21, title: "Salaar: Part 1 – Ceasefire", gross: "₹614–702 crore", language: "Telugu", year: 2023 },
  { rank: 22, title: "Jailer", gross: "₹605–650 crore", language: "Tamil", year: 2023 },
  { rank: 23, title: "Baahubali: The Beginning", gross: "₹599.72–650 crore", language: "Telugu/Tamil", year: 2015 },
  { rank: 24, title: "Leo", gross: "₹595–615 crore", language: "Tamil", year: 2023 },
  { rank: 25, title: "Sanju", gross: "₹586.85 crore", language: "Hindi", year: 2018 },
  { rank: 26, title: "Saiyaara", gross: "₹579.23 crore", language: "Hindi", year: 2025 },
  { rank: 27, title: "Tiger Zinda Hai", gross: "₹565.19 crore", language: "Hindi", year: 2017 },
  { rank: 28, title: "Padmaavat", gross: "₹563.55–571.98 crore", language: "Hindi", year: 2018 },
  { rank: 29, title: "Dhoom 3", gross: "₹556.74–558.42 crore", language: "Hindi", year: 2013 },
  { rank: 30, title: "Coolie", gross: "₹514–675 crore", language: "Tamil", year: 2025 },
  { rank: 31, title: "Ponniyin Selvan: I", gross: "₹500 crore", language: "Tamil", year: 2022 },
  { rank: 32, title: "War", gross: "₹474.79–475.62 crore", language: "Hindi", year: 2019 },
  { rank: 33, title: "Dunki", gross: "₹470.60 crore", language: "Hindi", year: 2023 },
  { rank: 34, title: "Tiger 3", gross: "₹466.63 crore", language: "Hindi", year: 2023 },
  { rank: 35, title: "Border 2", gross: "₹464.50 crore", language: "Hindi", year: 2026 },
  { rank: 36, title: "Andhadhun", gross: "₹444.48–456.89 crore", language: "Hindi", year: 2018 },
  { rank: 37, title: "The Greatest of All Time", gross: "₹440–460 crore", language: "Tamil", year: 2024 },
  { rank: 38, title: "Saaho", gross: "₹434–439 crore", language: "Telugu/Hindi", year: 2019 },
  { rank: 39, title: "Vikram", gross: "₹424–500 crore", language: "Tamil", year: 2022 },
  { rank: 40, title: "Bhool Bhulaiyaa 3", gross: "₹423.85 crore", language: "Hindi", year: 2024 },
  { rank: 41, title: "Brahmāstra: Part One – Shiva", gross: "₹418.80–430.77 crore", language: "Hindi", year: 2022 },
  { rank: 42, title: "Kantara", gross: "₹400–450 crore", language: "Kannada", year: 2022 },
  { rank: 43, title: "3 Idiots", gross: "₹400.61–460 crore", language: "Hindi", year: 2009 },
  { rank: 44, title: "Chennai Express", gross: "₹395.92–424.54 crore", language: "Hindi", year: 2013 },
  { rank: 45, title: "Krrish 3", gross: "₹393.37 crore", language: "Hindi", year: 2013 },
  { rank: 46, title: "Adipurush", gross: "₹392.70 crore", language: "Hindi/Telugu", year: 2023 },
  { rank: 47, title: "Simmba", gross: "₹391.68–400.19 crore", language: "Hindi", year: 2018 },
  { rank: 48, title: "Singham Again", gross: "₹389.64 crore", language: "Hindi", year: 2024 },
  { rank: 49, title: "Devara: Part 1", gross: "₹380–521 crore", language: "Telugu", year: 2024 },
  { rank: 50, title: "Pushpa: The Rise", gross: "₹360 crore", language: "Telugu", year: 2021 },
];

export default async function BoxOfficePage() {
  let movies = [];

  try {
    movies = await getBoxOffice();
  } catch (error) {
    console.error("Failed to fetch archive box office:", error);
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <h1 className="font-display text-4xl mb-2">Box Office</h1>
      <p className="text-bronze mb-10">
        All-time highest-grossing Indian films, worldwide gross.
      </p>

      <table className="w-full bg-[#fffdf8] border border-sandstone mb-3">
        <thead>
          <tr className="font-cinzel text-sm text-bronze border-b border-sandstone">
            <th className="text-left p-4">Rank</th>
            <th className="text-left p-4">Title</th>
            <th className="text-left p-4">Worldwide Gross</th>
            <th className="text-left p-4">Language</th>
            <th className="text-left p-4">Year</th>
          </tr>
        </thead>

        <tbody>
          {TOP_GROSSING.map((movie) => (
            <tr
              key={movie.rank}
              className="border-b border-sandstone/50 hover:bg-amber-50 transition"
            >
              <td className="p-4">{movie.rank}</td>
              <td className="p-4 font-display text-lg">{movie.title}</td>
              <td className="p-4">{movie.gross}</td>
              <td className="p-4">{movie.language}</td>
              <td className="p-4">{movie.year}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <a
        href="https://en.wikipedia.org/wiki/List_of_highest-grossing_Indian_films"
        target="_blank"
        rel="noopener noreferrer"
        className="text-xs text-bronze underline hover:text-gold"
      >
        Source: Wikipedia — CC BY-SA 4.0
      </a>

      
         
      
    </div>
  );
}