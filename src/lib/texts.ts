import { getCollection, type CollectionEntry } from 'astro:content';
import { u } from './url';

export type Text = CollectionEntry<'anakoinoseis'>;

// Όλα τα δημοσιευμένα κείμενα, το νεότερο πρώτο
export async function allTexts(): Promise<Text[]> {
  const list = await getCollection('anakoinoseis', (e) => !e.data.draft);
  return list.sort((a, b) => b.data.date.getTime() - a.data.date.getTime() || b.id.localeCompare(a.id));
}

export const textHref = (t: Text) => t.data.external ?? u(`/anakoinoseis/${t.id}/`);
export const ogHref = (t: Text) => `/og/${t.id}.png`;
