// Τι δείχνει η κορυφή της αρχικής. Το site ξαναχτίζεται κάθε πρωί και σε κάθε
// αλλαγή, οπότε η κορυφή αλλάζει μόνη της:
//
// 1. «agonas»: ο αγώνας της στιγμής (src/data/agonas.ts), ως και τη μέρα «until».
//    Αν ανέβει κείμενο με ημερομηνία από τη μέρα του αγώνα και μετά (π.χ. το
//    ρεπορτάζ το βράδυ της απεργίας), παίρνει αυτό αμέσως τη θέση του.
// 2. «text»: το νεότερο κείμενο, όσο είναι το πολύ FRESH_DAYS ημερών. Όταν ο
//    αγώνας περάσει, μετράνε μόνο κείμενα από τη μέρα του και μετά, για να μη
//    μένει στην κορυφή το κάλεσμα για κάτι που έγινε.
// 3. «sse»: αλλιώς, το μόνιμο μπλοκ της Κλαδικής Συλλογικής Σύμβασης.
import { agonas } from '../data/agonas';
import { todayAthens, isoDate } from './dates';
import { allTexts, type Text } from './texts';

export const FRESH_DAYS = 30;

export type Hero = { mode: 'agonas' } | { mode: 'text'; text: Text } | { mode: 'sse' };

const days = (from: string, to: string) => (Date.parse(to) - Date.parse(from)) / 86_400_000;

export async function hero(): Promise<Hero> {
  const today = todayAthens();
  // Τα κείμενα από τη μέρα του αγώνα και μετά, το νεότερο πρώτο
  const since = (await allTexts()).filter(
    (t) => t.id !== agonas.text && isoDate(t.data.date) >= agonas.countTo,
  );
  if (today <= agonas.until) return since[0] ? { mode: 'text', text: since[0] } : { mode: 'agonas' };
  const latest = since[0];
  if (latest && days(isoDate(latest.data.date), today) <= FRESH_DAYS) return { mode: 'text', text: latest };
  return { mode: 'sse' };
}
