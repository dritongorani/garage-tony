// Config Tailwind pour la compilation statique (assets/tailwind.css).
// Généré via le binaire standalone :  npx @tailwindcss/cli  ou  ./tailwindcss
// Les chemins content couvrent TOUTES les pages (racine + services/) afin que
// chaque classe utilisée soit émise dans le CSS final — aucune purge à risque.
module.exports = {
  content: [
    "./*.html",
    "./services/**/*.html",
    "./assets/*.js",
  ],
  theme: {
    extend: {
      colors: {
        racing: "#FF5733",
        racingStrong: "#D03F14",
        ink: "#0a0c0f",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
