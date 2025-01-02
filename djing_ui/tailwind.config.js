/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./src/index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          400: "rgba(var(--colors-primary-400))",
          500: "rgba(var(--colors-primary-500))",
          600: "rgba(var(--colors-primary-600))",
        },
        gray: {
          900: "rgba(15,23,42)",
          800: "rgba(30,41,59)",
        },
      },
    },
  },
  plugins: [],
};
