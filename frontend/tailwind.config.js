/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx}", "./components/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        maroon: "#7a1220",
        gold: "#d99a1b",
        ivory: "#f5ecd8",
        brown: "#2e1f12",
        bronze: "#9c6b2e",
        sandstone: "#e3c98f",
        crimson: "#c1272d",
        marquee: "#f2a71b",
        spotlight: "#ffdd8a",
        magenta: "#d63384",
        midnight: "#14163a",
        teal: "#0f7b7b",
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
