// Ημερομηνίες στα ελληνικά, ίδιες σε κάθε υπολογιστή (χωρίς Intl)
const GEN = ['Ιανουαρίου', 'Φεβρουαρίου', 'Μαρτίου', 'Απριλίου', 'Μαΐου', 'Ιουνίου',
  'Ιουλίου', 'Αυγούστου', 'Σεπτεμβρίου', 'Οκτωβρίου', 'Νοεμβρίου', 'Δεκεμβρίου'];
const SHORT = ['ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΪ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ'];
const pad = (n: number) => String(n).padStart(2, '0');

export const isoDate = (d: Date) => `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())}`;
export const longDate = (d: Date) => `${d.getUTCDate()} ${GEN[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
export const dayNum = (d: Date) => pad(d.getUTCDate());
export const dayMonth = (d: Date) => `${pad(d.getUTCDate())}.${pad(d.getUTCMonth() + 1)}`;
export const monthYear = (d: Date) => `${SHORT[d.getUTCMonth()]} ${d.getUTCFullYear()}`;

// Η σημερινή μέρα στη Θεσσαλονίκη, ως ΕΕΕΕ-ΜΜ-ΗΗ
export function todayAthens(): string {
  return new Date().toLocaleDateString('en-CA', { timeZone: 'Europe/Athens' });
}

// Λεπτά ανάγνωσης από το κείμενο (περίπου 200 λέξεις το λεπτό)
export function readingMinutes(body: string | undefined): number {
  const words = (body ?? '').replace(/<[^>]+>/g, ' ').replace(/[*_#>@]/g, ' ').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
}
