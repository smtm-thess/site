import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Κάθε κείμενο του Σωματείου είναι ένα αρχείο .md στο src/content/anakoinoseis/,
// με όνομα ΕΕΕΕ-ΜΜ-ΗΗ-λέξεις-με-παύλες.md. Το όνομα γίνεται και η διεύθυνση.
const anakoinoseis = defineCollection({
  loader: glob({ base: './src/content/anakoinoseis', pattern: '**/*.md' }),
  schema: ({ image }) => z.object({
    title: z.string(),
    sub: z.array(z.string()).default([]),
    date: z.coerce.date(),
    kind: z.string().default('Ανακοίνωση'),
    cat: z.enum(['anak', 'apof', 'dt', 'drasi']).default('anak'),
    summary: z.string().optional(),
    pdf: z.string().optional(),
    event: z
      .object({ label: z.string(), when: z.string(), where: z.string() })
      .optional(),
    // Βίντεο του κειμένου: αρχεία στο public/video/
    video: z
      .object({ src: z.string(), poster: z.string(), length: z.string().optional() })
      .optional(),
    og: z.object({ title: z.string().optional(), line: z.string().optional() }).optional(),
    // Φωτογραφίες (π.χ. ρεπορτάζ από απεργία): αρχεία στο foto/<όνομα κειμένου>/,
    // περασμένα πρώτα από το tools/foto.py. Η πρώτη μπαίνει και στην αρχική.
    photos: z.array(z.object({ src: image(), alt: z.string() })).default([]),
    // Ποια φωτογραφία μπαίνει στην κορυφή της αρχικής (από 0). Χρήσιμο όταν η πρώτη
    // είναι γραφικό με γράμματα (εξώφυλλο), που κόβεται άσχημα στο πλαίσιο της αρχικής.
    homePhoto: z.number().int().min(0).default(0),
    // Παλιά κείμενα που μένουν στο παλιό site: η λίστα δείχνει εκεί
    external: z.string().url().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { anakoinoseis };
