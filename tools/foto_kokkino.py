#!/usr/bin/env python3
"""Ασπρόμαυρη φωτογραφία που κρατά μόνο τα κόκκινα (πανό, σημαίες), στα χρώματα του site.

Για την κορυφή της αρχικής και για τα βίντεο: η φωτογραφία μιας διαδήλωσης γίνεται
ασπρόμαυρη, σε μελάνι και χαρτί, και ό,τι είναι κόκκινο (τα πανό μας, οι σημαίες)
μένει κόκκινο, στο κόκκινο του Σωματείου.

Παράδειγμα:
  python3 tools/foto_kokkino.py diadilosi.jpg src/content/anakoinoseis/foto/<κείμενο>/01.jpg --width 2000

--width: αν η φωτογραφία είναι μικρότερη, τη μεγαλώνει ως εκεί (για μικρές φωτογραφίες
από το κινητό ή από το διαδίκτυο). Όπως το tools/foto.py, γράφει μόνο τα pixel, χωρίς
τίποτα από όσα γράφει μέσα της το κινητό (τοποθεσία, ώρα, συσκευή).
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter, ImageOps

PAPER = np.array([241, 236, 226]) / 255
INK = np.array([21, 21, 21]) / 255
RED = np.array([204, 42, 30]) / 255


def smooth(x, a0, a1):
    t = np.clip((x - a0) / (a1 - a0), 0, 1)
    return t * t * (3 - 2 * t)


def kokkino(im, width=0, sat_lo=0.42, sat_hi=0.62):
    im = ImageOps.exif_transpose(im).convert('RGB')
    if width and im.width < width:
        h = round(im.height * width / im.width)
        im = im.resize((width, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2.2, percent=60, threshold=2))
    a = np.asarray(im).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    sat = np.where(mx > 0, (mx - mn) / (mx + 1e-6), 0)
    d = mx - mn + 1e-6
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # ασπρόμαυρη, με λίγο περισσότερη αντίθεση, από το μελάνι ως το χαρτί
    L = np.clip((lum - 0.04) / 0.92, 0, 1)
    L = smooth(L, 0, 1) * 0.55 + L * 0.45
    mono = INK + (PAPER - INK) * L[..., None]
    # μάσκα για τα κόκκινα: απόχρωση κοντά στο κόκκινο, έντονο χρώμα, όχι πολύ σκοτεινό
    hd = np.minimum(np.abs(hue), np.abs(hue - 360))
    m = (1 - smooth(hd, 10, 22)) * smooth(sat, sat_lo, sat_hi) * smooth(mx, 0.22, 0.38)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
    shade = np.clip(lum / 0.32, 0.55, 1.15)[..., None]
    out = mono * (1 - m[..., None]) + np.clip(RED * shade, 0, 1) * m[..., None]
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('out')
    ap.add_argument('--width', type=int, default=0, help='ελάχιστο πλάτος σε pixel')
    a = ap.parse_args()
    with Image.open(a.src) as im:
        res = kokkino(im, a.width)
    res.save(a.out, 'JPEG', quality=88, optimize=True, progressive=True)
    print(f'{a.src} -> {a.out} ({res.width}x{res.height})')
