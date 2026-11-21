import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { allTexts } from '../lib/texts';
import { UNION } from '../consts';
import { u } from '../lib/url';

export async function GET(context: APIContext) {
  const texts = (await allTexts()).slice(0, 30);
  return rss({
    title: `Ανακοινώσεις ${UNION.short}`,
    description: UNION.description,
    site: new URL(u('/'), context.site!).href,
    items: texts.map((t) => ({
      title: t.data.title,
      pubDate: t.data.date,
      description: t.data.summary ?? t.data.sub.join(' · '),
      link: t.data.external ?? new URL(u(`/anakoinoseis/${t.id}/`), context.site!).href,
    })),
    customData: '<language>el</language>',
  });
}
