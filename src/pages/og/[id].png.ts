import type { APIRoute } from 'astro';
import { allTexts, type Text } from '../../lib/texts';
import { ogPng, upper } from '../../lib/og';
import { longDate } from '../../lib/dates';

export async function getStaticPaths() {
  const texts = (await allTexts()).filter((t) => !t.data.external);
  return [
    ...texts.map((t) => ({ params: { id: t.id }, props: { t } })),
    { params: { id: 'default' }, props: { t: null } },
  ];
}

export const GET: APIRoute = async ({ props }) => {
  const t = (props as { t: Text | null }).t;
  const png = t
    ? await ogPng({
        title: t.data.og?.title ?? t.data.title,
        kicker: upper(t.data.kind),
        line: t.data.og?.line ?? upper(longDate(t.data.date)),
      })
    : await ogPng({ title: 'ΕΜΕΙΣ ΠΑΡΑΓΟΥΜΕ|ΤΟΝ ΠΛΟΥΤΟ', line: 'ΜΗΧΑΝΙΚΟΙ · ΤΕΧΝΟΛΟΓΟΙ · ΓΕΩΛΟΓΟΙ · ΣΧΕΔΙΑΣΤΕΣ' });
  return new Response(new Uint8Array(png), { headers: { 'Content-Type': 'image/png' } });
};
