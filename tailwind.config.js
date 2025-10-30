/**
 * Tailwind configuration prepared for future build setup.
 * Using CDN in development; switch to a proper build pipeline later.
 */
module.exports = {
  content: [
    './core/templates/**/*.html',
    './projects/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        accent: {
          primary: '#ff6b35',
          secondary: '#f7931e',
          hover: '#ff8555',
        },
        bg: {
          primary: '#0f0f0f',
          secondary: '#1a1a1a',
          tertiary: '#242424',
        },
        textc: {
          primary: '#ffffff',
          secondary: '#b8b8b8',
          muted: '#808080',
        },
      },
      fontFamily: {
        sans: [
          'Saira',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'Noto Sans',
          'sans-serif',
        ],
        mono: ['IBM Plex Mono', 'Fira Code', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
    },
  },
  plugins: [],
};


