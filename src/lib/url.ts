// Σύνδεσμοι μέσα στο site. Το site μπορεί να ζει σε υποφάκελο (π.χ. στο GitHub
// πριν μπει το smtm.gr), γι' αυτό κάθε εσωτερικός σύνδεσμος περνά από εδώ.
const BASE = import.meta.env.BASE_URL.replace(/\/+$/, '');

export function u(path = '/'): string {
  if (/^([a-z]+:|#|\/\/)/i.test(path)) return path;
  return BASE + (path.startsWith('/') ? path : '/' + path);
}

// Πλήρης διεύθυνση, για κοινοποίηση και εικόνες προεπισκόπησης
export function abs(path: string, site: URL | undefined): string {
  return new URL(u(path), site ?? 'https://smtm.gr').href;
}
