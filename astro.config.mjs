// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { LINKS } from './src/data/links.ts';

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
  // οι σύντομοι σύνδεσμοι (src/data/links.ts) δεν μπαίνουν στο sitemap
  integrations: [sitemap({ filter: (p) => !Object.keys(LINKS).some((l) => p.endsWith(`/${l}/`)) })],
  devToolbar: { enabled: false },
});
