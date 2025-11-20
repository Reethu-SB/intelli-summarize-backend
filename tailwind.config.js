/** @type {import('tailwindcss').Config} */
import themeVariants from "tailwindcss-theme-variants";
import animate from "tailwindcss-animate";

export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    themeVariants(),
    animate(),
  ],
};
