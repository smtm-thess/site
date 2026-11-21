import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Κάθε κείμενο του Σωματείου είναι ένα αρχείο .md στο src/content/anakoinoseis/,
// με όνομα ΕΕΕΕ-ΜΜ-ΗΗ-λέξεις-με-παύλες.md. Το όνομα γίνεται και η διεύθυνση.
const anakoinoseis = defineCollection({
  loader: glob({ base: './src/content/anakoinoseis', pattern: '**/*.md' }),
  schema: z.object({
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
    // Παλιά κείμενα που μένουν στο παλιό site: η λίστα δείχνει εκεί
    external: z.string().url().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { anakoinoseis };
