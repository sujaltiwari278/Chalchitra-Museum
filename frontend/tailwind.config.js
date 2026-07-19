/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx}", "./components/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        maroon: "#5c1a1b",
        gold: "#c9a24b",
        ivory: "#f6efe1",
        brown: "#3a2317",
        bronze: "#8a6d3b",
        sandstone: "#d8c39a",
      },
      fontFamily: {
        display: ["var(--font-playfair)", "serif"],
        body: ["var(--font-cormorant)", "serif"],
        cinzel: ["var(--font-cinzel)", "serif"],
      },
    },
  },
  plugins: [],
};
