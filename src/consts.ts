// Τα στοιχεία του Σωματείου. Ό,τι αλλάζει εδώ, αλλάζει σε όλο το site.

export const UNION = {
  name: 'Σωματείο Μισθωτών Τεχνικών Μακεδονίας',
  short: 'ΣΜΤΜ',
  // Το όνομα όπως γράφεται στο σήμα, σε δύο γραμμές
  lines: ['ΣΩΜΑΤΕΙΟ ΜΙΣΘΩΤΩΝ', 'ΤΕΧΝΙΚΩΝ ΜΑΚΕΔΟΝΙΑΣ'],
  tagline: 'Μηχανικοί · Τεχνολόγοι · Γεωλόγοι · Σχεδιαστές',
  description:
    'Το σωματείο των μηχανικών, τεχνολόγων, γεωλόγων, σχεδιαστών και κάθε τεχνικού που δουλεύει για μισθό ή με «μπλοκάκι» στη Μακεδονία.',

  // Όταν στηθεί το info@smtm.gr, αλλάζει μόνο αυτή η γραμμή
  email: 'somtechnik.thes@gmail.com',
  phones: ['694 834 9644', '697 459 2442'],

  place: 'Εργατικό Κέντρο Θεσσαλονίκης',
  street: 'Αριστοτέλους 32, 5ος όροφος',
  city: 'Θεσσαλονίκη',
  mapUrl:
    'https://www.google.com/maps/search/?api=1&query=%CE%91%CF%81%CE%B9%CF%83%CF%84%CE%BF%CF%84%CE%AD%CE%BB%CE%BF%CF%85%CF%82+32+%CE%98%CE%B5%CF%83%CF%83%CE%B1%CE%BB%CE%BF%CE%BD%CE%AF%CE%BA%CE%B7',

  // Ο σύνδεσμος του καναλιού Viber, όταν φτιαχτεί. Κενό = δεν εμφανίζεται.
  viber: '',

  oldSite: 'https://somtechnik.wordpress.com/',
  // Έγγραφα που μένουν ακόμα στο παλιό site
  sseDraftPdf:
    'https://somtechnik.wordpress.com/wp-content/uploads/2022/06/cea3ce9ccea4ce9c_cea3cf87ceadceb4ceb9cebf_cea3cf85cebbcebbcebfceb3ceb9cebaceaecf82_cea3cf8dcebcceb2ceb1cf83ceb7cf82_2022-1.pdf',
  applicationDoc: 'https://somtechnik.wordpress.com/wp-content/uploads/2012/11/aithsh.doc',
};

// Χρόνια χωρίς Κλαδική Συλλογική Σύμβαση: από το 2012, όταν οι νόμοι των
// μνημονίων τελείωσαν τις κλαδικές συμβάσεις. Μεγαλώνει μόνο του κάθε χρόνο.
export const YEARS_WITHOUT_SSE = new Date().getFullYear() - 2012;

// Ο πρώτος μισθός που διεκδικούμε, καθαρά, και η προσαύξηση κάθε δύο χρόνια
export const WAGES = [
  { amount: '1.295', who: 'Απόφοιτοι Πολυτεχνείων και 5ετών σχολών' },
  { amount: '1.205', who: 'Απόφοιτοι 4ετών πανεπιστημιακών σχολών' },
  { amount: '1.090', who: 'Απόφοιτοι ΙΕΚ και τεχνικών σχολών' },
];
export const WAGE_STEP = 'Από εκεί και πέρα, θεσμοθετημένη προσαύξηση κάθε δύο χρόνια.';

// Το κύριο μενού
export const NAV = [
  { href: '/anakoinoseis/', label: 'Ανακοινώσεις', key: 'anakoinoseis' },
  { href: '/sse/', label: 'Κλαδική ΣΣΕ', key: 'sse' },
  { href: '/poioi-eimaste/', label: 'Ποιοι είμαστε', key: 'poioi' },
  { href: '/grapse/', label: 'Γράψε μας', key: 'grapse' },
];

// Τα είδη των κειμένων στο αρχείο
export const CATS = {
  anak: 'Ανακοινώσεις',
  apof: 'Αποφάσεις',
  dt: 'Δελτία τύπου',
  drasi: 'Δράσεις',
} as const;
export type Cat = keyof typeof CATS;
