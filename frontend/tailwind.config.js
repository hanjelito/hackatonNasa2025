/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nasa: {
          blue: '#288bff',
          'dark-blue': '#0b3d91',
          red: '#af1108',
          black: '#000000',
          'gray-dark': '#1a1a1a',
          'gray-medium': '#2a2a2a',
          'gray-light': '#959599',
          'gray-lighter': '#d1d1d1',
        }
      },
      fontFamily: {
        sans: ['system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['dm-mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
