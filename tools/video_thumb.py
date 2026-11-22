#!/usr/bin/env python3
"""Εικόνα για το email: τρία καρέ του βίντεο δίπλα δίπλα και κουμπί ▶ (τα email δεν παίζουν βίντεο).

Παράδειγμα:
  python3 tools/video_thumb.py public/video/2026-11-25-apergia.mp4 2 10 68 \
      public/email/2026-11-16-apergoume-25-noemvri-video.jpg
Τα νούμερα είναι τα δευτερόλεπτα των καρέ. Το όνομα πρέπει να είναι <slug ανακοίνωσης>-video.jpg.
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

video, *times, out = sys.argv[1:]
W, GAP = 368, 8                      # 2x για οθόνες υψηλής ανάλυσης: εμφανίζεται 560 πλάτος
H = round(W * 16 / 9)
INK, PAPER = (21, 21, 21), (241, 236, 226)
img = Image.new('RGB', (W * len(times) + GAP * (len(times) - 1), H), INK)
with tempfile.TemporaryDirectory() as tmp:
    for i, t in enumerate(times):
        f = os.path.join(tmp, f'{i}.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', t, '-i', video, '-frames:v', '1', f], check=True)
        img.paste(Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS), (i * (W + GAP), 0))
S, D = 4, 150                        # κουμπί σε 4x και σμίκρυνση, για καθαρές άκρες
btn = Image.new('RGBA', (D * S, D * S), (0, 0, 0, 0))
b = ImageDraw.Draw(btn)
b.ellipse((0, 0, D * S - 1, D * S - 1), fill=INK + (255,))
b.ellipse((5 * S, 5 * S, D * S - 5 * S, D * S - 5 * S), outline=PAPER + (255,), width=4 * S)
cx, cy, r = D * S / 2 + 6 * S, D * S / 2, 34 * S
b.polygon([(cx - r * 0.75, cy - r), (cx - r * 0.75, cy + r), (cx + r, cy)], fill=PAPER + (255,))
btn = btn.resize((D, D), Image.LANCZOS)
img.paste(btn, ((img.width - D) // 2, int(H * 0.80) - D // 2), btn)
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
img.save(out, quality=84, optimize=True, progressive=True)
print(out, img.size, os.path.getsize(out), 'bytes')
