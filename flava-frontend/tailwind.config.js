/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        flava: {
          pink: '#FF477E',
          dark: '#1E1E24',
          cream: '#FFF5F5'
        }
      }
    },
  },
  plugins: [],
}