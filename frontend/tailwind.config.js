/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    dark: '#0B0C10',
                    panel: '#13141C',
                    purple: '#5D5CDE',
                    cyan: '#4AB7C3',
                    input: '#1E202B',
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'], // Ensure a nice font is used if available, or fallback
            }
        },
    },
    plugins: [],
}
