/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class', // Enable class-based dark mode
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}"
    ],
    theme: {
        extend: {
            screens: {
                '3xl': '1921px',  // Custom breakpoint for screens wider than 1920px
            },
        },
    },
    plugins: [],
};
