export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8001/api";

async function safeFetch(url, fallback) {
  try {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) return fallback;
    return await res.json();
  } catch {
    return fallback;
  }
}

export const getMovies = (params = "") =>
  safeFetch(`${API_BASE}/movies${params}`, []);

export const getMovie = (id) => safeFetch(`${API_BASE}/movies/${id}`, null);

export const searchMovies = (q) =>
  safeFetch(`${API_BASE}/search?q=${encodeURIComponent(q)}`, []);

export const searchAll = (q) =>
  safeFetch(`${API_BASE}/search/all?q=${encodeURIComponent(q)}`, { movies: [], people: [] });

export const getLanguages = () => safeFetch(`${API_BASE}/meta/languages`, []);

export const getEras = () => safeFetch(`${API_BASE}/meta/eras`, []);

export const getGenres = () => safeFetch(`${API_BASE}/meta/genres`, []);

export const getBoxOffice = () => safeFetch(`${API_BASE}/box-office`, []);

export const getPeople = (role, gender) => {
  const params = new URLSearchParams();
  if (role) params.set("role", role);
  if (gender) params.set("gender", gender);
  return safeFetch(`${API_BASE}/people?${params.toString()}`, []);
};

export const getPerson = (id) => safeFetch(`${API_BASE}/people/${id}`, null);

export const getStudios = () => safeFetch(`${API_BASE}/studios`, []);
export const getStudio = (id) => safeFetch(`${API_BASE}/studios/${id}`, null);

export const getAwards = () => safeFetch(`${API_BASE}/awards`, []);

export const getFestivals = () => safeFetch(`${API_BASE}/film-festivals`, []);
export const getFestival = (id) => safeFetch(`${API_BASE}/film-festivals/${id}`, null);

export const getTrivia = (category) => {
  const params = category ? `?category=${encodeURIComponent(category)}` : "";
  return safeFetch(`${API_BASE}/trivia${params}`, []);
};
export const getTriviaCategories = () => safeFetch(`${API_BASE}/meta/trivia-categories`, []);

export const getArchives = () => safeFetch(`${API_BASE}/archives`, []);
