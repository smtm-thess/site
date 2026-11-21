// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Η διεύθυνση του site. Στο GitHub Pages τη δίνει το workflow
// (SITE_URL και BASE_PATH από το actions/configure-pages). Όταν μπει το
// smtm.gr στις ρυθμίσεις του GitHub, αλλάζουν μόνες τους. Πάντα https, ακόμα κι
// αν το GitHub δίνει http όσο ετοιμάζει το πιστοποιητικό.
const site = (process.env.SITE_URL || 'https://smtm.gr').replace(/^http:/, 'https:');
const base = (process.env.BASE_PATH || '').replace(/\/+$/, '') + '/';

export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  integrations: [sitemap()],
  devToolbar: { enabled: false },
});
