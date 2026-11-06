/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["IBM Plex Sans", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
      colors: {
        graphite: "#202124",
        secondary: "#5F6368",
        signal: "#D9480F",
        surface: "#FFFFFF",
        border: "#D5D7DA",
      },
      borderRadius: {
        control: "6px",
      },
    },
  },
  plugins: [],
};
