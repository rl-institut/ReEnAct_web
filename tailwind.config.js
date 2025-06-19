/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./reenact/templates/**/*.html', "./reenact/static/js/*.js"],
  theme: {
    extend: {
      keyframes: {
        popIn: {
          '0%': { opacity: '0', transform: 'scale(0.9)' },
          '60%': { opacity: '1', transform: 'scale(1.05)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
      animation: {
        popIn: 'popIn 500ms ease-out',
      },
    }
  },
  plugins: [],
}
