#!/usr/bin/env python3
"""Φτιάχνει σελίδα ανακοίνωσης για το site από το κείμενο του builder (.txt με @tags).

Παράδειγμα:
  python3 tools/txt2md.py κείμενο.txt --date 2026-11-16 --slug apergoume-25-noemvri \
      --kind "Ανακοίνωση" --summary "Μία-δύο προτάσεις για τη λίστα" \
      --pdf /pdf/2026-11-16-apergoume-25-noemvri.pdf

Γράφει το src/content/anakoinoseis/<date>-<slug>.md (ή τυπώνει με --stdout).
Το PDF μπαίνει στο public/pdf/ με το ίδιο όνομα.
Είδη (--cat): anak (ανακοίνωση, κάλεσμα), apof (απόφαση), dt (δελτίο τύπου), drasi (ανταπόκριση).
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from announce2html import convert  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('--date', required=True, help='ΕΕΕΕ-ΜΜ-ΗΗ, η μέρα που βγήκε το κείμενο')
ap.add_argument('--slug', required=True, help='λατινικά, με παύλες, π.χ. apergoume-25-noemvri')
ap.add_argument('--kind', default='Ανακοίνωση', help='η ετικέτα πάνω από τον τίτλο')
ap.add_argument('--cat', default='anak', choices=['anak', 'apof', 'dt', 'drasi'])
ap.add_argument('--summary', default='', help='μία-δύο προτάσεις σε πεζά, για τη λίστα και την κοινοποίηση')
ap.add_argument('--pdf', default='', help='π.χ. /pdf/2026-11-16-apergoume-25-noemvri.pdf')
ap.add_argument('--og-line', default='', help='γραμμή στο κάτω μέρος της εικόνας κοινοποίησης')
ap.add_argument('--draft', action='store_true', help='δεν δημοσιεύεται ακόμα')
ap.add_argument('--stdout', action='store_true')
a = ap.parse_args()

d = convert(open(a.src, encoding='utf-8').read())
q = lambda s: json.dumps(s, ensure_ascii=False)  # YAML δέχεται JSON strings
fm = ['---', f'title: {q(d["title"])}']
if d['sub']:
    fm.append('sub:')
    fm += [f'  - {q(s.strip())}' for s in d['sub']]
fm += [f'date: {a.date}', f'kind: {q(a.kind)}', f'cat: {a.cat}']
if a.summary:
    fm.append(f'summary: {q(a.summary)}')
if a.pdf:
    fm.append(f'pdf: {q(a.pdf)}')
if a.og_line:
    fm += ['og:', f'  line: {q(a.og_line)}']
if a.draft:
    fm.append('draft: true')
fm.append('---')
body = '\n\n'.join(line for line in d['html'].split('\n') if line.strip())
out = '\n'.join(fm) + '\n\n' + body + '\n'

if a.stdout:
    sys.stdout.write(out)
else:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, 'src', 'content', 'anakoinoseis', f'{a.date}-{a.slug}.md')
    open(path, 'w', encoding='utf-8').write(out)
    print(path)
