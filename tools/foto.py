#!/usr/bin/env python3
"""Ετοιμάζει φωτογραφίες για ένα κείμενο του site (π.χ. ρεπορτάζ από απεργία).

Παράδειγμα:
  python3 tools/foto.py 2026-11-25-i-apergia-mas ~/Λήψεις/IMG_01.jpg ~/Λήψεις/IMG_02.jpg

Για κάθε φωτογραφία:
- τη γυρίζει όπως την τράβηξε το κινητό,
- τη μικραίνει ως 2400 pixel στη μεγάλη πλευρά,
- σβήνει ό,τι γράφει μέσα της το κινητό (τοποθεσία, ώρα, συσκευή),
- τη γράφει στο src/content/anakoinoseis/foto/<όνομα κειμένου>/01.jpg, 02.jpg, ...

Το repository είναι δημόσιο, γι' αυτό καμία φωτογραφία δεν μπαίνει χωρίς να περάσει από εδώ.
Στο τέλος τυπώνει τις γραμμές για το frontmatter του κειμένου. Στο alt γράφεις με λίγα
λόγια τι δείχνει η φωτογραφία (το διαβάζουν όσοι δεν βλέπουν την εικόνα).
"""
import argparse, os, sys
from PIL import Image, ImageOps

MAX = 2400
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'content', 'anakoinoseis')

ap = argparse.ArgumentParser()
ap.add_argument('text', help='το όνομα του κειμένου χωρίς .md, π.χ. 2026-11-25-i-apergia-mas')
ap.add_argument('photos', nargs='+', help='οι φωτογραφίες, με τη σειρά που θα μπουν (η πρώτη πάει και στην αρχική)')
ap.add_argument('--start', type=int, default=1, help='από ποιον αριθμό αρχίζει η αρίθμηση')
a = ap.parse_args()

out = os.path.join(ROOT, 'foto', a.text)
os.makedirs(out, exist_ok=True)
lines = ['photos:']
for i, src in enumerate(a.photos, start=a.start):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert('RGB')
        im.thumbnail((MAX, MAX), Image.LANCZOS)
        name = f'{i:02d}.jpg'
        # Νέα εικόνα χωρίς exif, icc ή σχόλια: μόνο τα pixel
        clean = Image.new('RGB', im.size)
        clean.paste(im)
        clean.save(os.path.join(out, name), 'JPEG', quality=86, optimize=True, progressive=True)
        print(f'{src} -> foto/{a.text}/{name} ({clean.width}x{clean.height})', file=sys.stderr)
    lines += [f'  - src: ./foto/{a.text}/{name}', '    alt: "…"']
print('\n'.join(lines))
