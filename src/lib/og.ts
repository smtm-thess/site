// Εικόνες κοινοποίησης 1200x630 (αυτό που βλέπει κανείς όταν στέλνεται
// ένας σύνδεσμος σε Viber, Messenger, Facebook). Φτιάχνονται στο χτίσιμο.
import fs from 'node:fs';
import path from 'node:path';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';

const root = process.cwd();
const font = (f: string) => fs.readFileSync(path.join(root, 'tools/og-fonts', f));
const fonts = [
  { name: 'Fira', data: font('FiraSansExtraCondensed-Black.ttf'), weight: 900 as const, style: 'normal' as const },
  { name: 'Fira', data: font('FiraSansExtraCondensed-ExtraBold.ttf'), weight: 800 as const, style: 'normal' as const },
  { name: 'Manrope', data: font('Manrope-ExtraBold.ttf'), weight: 800 as const, style: 'normal' as const },
];
const logo =
  'data:image/svg+xml;base64,' +
  fs.readFileSync(path.join(root, 'public/logo.svg')).toString('base64');

const RED = '#CC2A1E', INK = '#151515', PAPER = '#F1ECE2';

type Node = { type: string; props: Record<string, any> };
const h = (type: string, style: Record<string, any>, children?: any, extra: Record<string, any> = {}): Node =>
  ({ type, props: { style, children, ...extra } });

// Μέγεθος τίτλου ανάλογα με το μήκος, ώστε να χωράει σε 3 γραμμές
function titleSize(t: string): number {
  const n = t.length;
  if (n <= 18) return 150;
  if (n <= 30) return 128;
  if (n <= 48) return 104;
  if (n <= 70) return 86;
  return 70;
}

// Κεφαλαία χωρίς τόνους, όπως γράφονται στα ελληνικά (κρατά τα διαλυτικά)
export const upper = (s: string) => s.normalize('NFD').replace(/\u0301/g, '').toUpperCase().normalize('NFC');

export async function ogPng(opts: { title: string; line?: string; kicker?: string }): Promise<Buffer> {
  const { title, line = '', kicker = '' } = opts;
  const tree = h('div', {
    // Το satori προσθέτει το padding στις διαστάσεις: 1056 + 144 = 1200, 510 + 120 = 630
    width: 1056, height: 510, display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
    background: RED, color: PAPER, padding: '62px 72px 58px',
  }, [
    h('div', { display: 'flex', alignItems: 'center', gap: 26 }, [
      h('img', { width: 96, height: 95 }, undefined, { src: logo, width: 96, height: 95 }),
      h('div', { display: 'flex', flexDirection: 'column', fontFamily: 'Manrope', fontWeight: 800, fontSize: 27, letterSpacing: 2.2, lineHeight: 1.25, color: PAPER }, [
        h('div', {}, 'ΣΩΜΑΤΕΙΟ ΜΙΣΘΩΤΩΝ'),
        h('div', {}, 'ΤΕΧΝΙΚΩΝ ΜΑΚΕΔΟΝΙΑΣ'),
      ]),
    ]),
    h('div', { display: 'flex', flexDirection: 'column' }, [
      kicker ? h('div', { fontFamily: 'Manrope', fontWeight: 800, fontSize: 24, letterSpacing: 3, color: INK, marginBottom: 14 }, kicker) : null,
      h('div', { display: 'flex', flexDirection: 'column', fontFamily: 'Fira', fontWeight: 900, fontSize: titleSize(title.replace(/\|/g, ' ')), lineHeight: 0.88, marginLeft: -4 },
        title.split('|').map((l) => h('div', {}, l.trim()))),
    ].filter(Boolean)),
    h('div', { fontFamily: 'Fira', fontWeight: 800, fontSize: 40, color: INK, letterSpacing: 0.5 }, line || 'smtm.gr'),
  ]);
  const svg = await satori(tree as any, { width: 1200, height: 630, fonts });
  return new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng();
}

// Εικονίδιο για την αρχική οθόνη του κινητού
export function touchIcon(): Buffer {
  const inner = fs.readFileSync(path.join(root, 'public/logo.svg'), 'utf8')
    .replace(/^<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180"><rect width="180" height="180" fill="${PAPER}"/><svg x="18" y="18" width="144" height="144" viewBox="0 0 1188 1176">${inner}</svg></svg>`;
  return new Resvg(svg).render().asPng();
}
