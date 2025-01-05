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
            colors:{
                'danger': '#ff0000',
                'item-dark-bg': '#1f2937',
                'item-light-bg': '#f9fafb',
                'primary-dark': '#ffffff',
                'primary-light': '#1f2937',
                'secondary-dark': '#d1d5db',
                'secondary-light': '#4b5563',
                'item-secondary-dark': '#374151',
                'item-secondary-light': '#f3f4f6',
                'indigo-t': '#6366f1',
                'app-dark-bg': '#111827',
                'app-light-bg': '#e5e7eb',
                'navbar-dark-bg': '#1f2937',
                'navbar-light-bg': '#ffffff',
                'navbar-dark-text': '#ffffff',
                'navbar-light-text': '#1f2937',
            },
        },
    },
    plugins: [],
};
