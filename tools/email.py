#!/usr/bin/env python3
"""Φτιάχνει το email μιας ανακοίνωσης για το Sender, από το ίδιο .md του site.

Παράδειγμα:
  python3 tools/email.py src/content/anakoinoseis/2026-11-16-apergoume-25-noemvri.md > email.html

Στο Sender: νέα καμπάνια, σχέδιο με δικό σας HTML, επικόλληση. Στη θέση του
{{UNSUBSCRIBE}} μπαίνει ο σύνδεσμος διαγραφής του Sender.
Το email έχει την αρχή του κειμένου και κουμπί για όλη την ανακοίνωση στο site.
Επιλογές: --site https://smtm.gr  --paras 3 (πόσες παράγραφοι της αρχής)
"""
import argparse, html, os, re, sys
import yaml

ap = argparse.ArgumentParser()
ap.add_argument('md')
ap.add_argument('--site', default='https://smtm.gr')
ap.add_argument('--paras', type=int, default=3)
a = ap.parse_args()

src = open(a.md, encoding='utf-8').read()
_, fm, body = src.split('---', 2)
d = yaml.safe_load(fm)
slug = os.path.splitext(os.path.basename(a.md))[0]
site = a.site.rstrip('/')
url = f'{site}/anakoinoseis/{slug}/'
pdf = site + d['pdf'] if d.get('pdf') else ''

# Η αρχή του κειμένου: οι πρώτες παράγραφοι, χωρίς την προσφώνηση
paras = [p for p in re.findall(r'<p>(.*?)</p>', body, flags=re.S)]
paras = [p for p in paras if not re.match(r'^Συναδέλφισσες, συνάδελφοι,?$', re.sub(r'<[^>]+>', '', p).strip())]
excerpt = paras[: a.paras]

RED, INK, PAPER, PAPER2, GREY = '#CC2A1E', '#151515', '#F1ECE2', '#E7DFD0', '#56514A'
DISPLAY = "'Arial Narrow','Roboto Condensed',Arial,Helvetica,sans-serif"
TEXT = "Arial,Helvetica,sans-serif"
MONTHS = ['Ιανουαρίου', 'Φεβρουαρίου', 'Μαρτίου', 'Απριλίου', 'Μαΐου', 'Ιουνίου', 'Ιουλίου',
          'Αυγούστου', 'Σεπτεμβρίου', 'Οκτωβρίου', 'Νοεμβρίου', 'Δεκεμβρίου']
dt = d['date']
date = f'{dt.day} {MONTHS[dt.month - 1]} {dt.year}'
esc = lambda s: html.escape(str(s), quote=True)

def para(p):
    p = p.replace('<strong>', f'<strong style="color:{INK}">')
    return f'<p style="margin:0 0 16px;font:16px/1.6 {TEXT};color:#2A2723">{p}</p>'

event = ''
if d.get('event'):
    e = d['event']
    event = f'''<tr><td style="padding:0 32px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="background:{INK};padding:18px 20px">
<div style="font:bold 11px/1.4 {TEXT};letter-spacing:2px;color:#F3A69F;text-transform:uppercase">{esc(e['label'])}</div>
<div style="font:bold 26px/1.1 {DISPLAY};color:{PAPER};margin-top:6px">{esc(e['when'])}</div>
<div style="font:bold 17px/1.3 {DISPLAY};color:{PAPER};margin-top:6px">{esc(e['where'])}</div>
</td></tr></table></td></tr>'''

subs = ''.join(f'<div style="font:bold 17px/1.25 {DISPLAY};color:{INK if i else PAPER};margin-top:6px">{esc(s)}</div>'
               for i, s in enumerate(d.get('sub') or []))
pdf_link = (f'<p style="margin:14px 0 0;font:14px/1.5 {TEXT}"><a href="{esc(pdf)}" style="color:{INK};font-weight:bold">Κατέβασε το PDF για μοίρασμα</a></p>'
            if pdf else '')

out = f'''<!doctype html>
<html lang="el"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(d['title'])}</title></head>
<body style="margin:0;padding:0;background:{PAPER2}">
<div style="display:none;max-height:0;overflow:hidden">{esc(d.get('summary') or ' · '.join(d.get('sub') or []))}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPER2}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:{PAPER}">
<tr><td style="padding:22px 32px 18px;border-bottom:2px solid {INK}">
<table role="presentation" cellpadding="0" cellspacing="0"><tr>
<td style="padding-right:12px"><img src="{site}/logo-email.png" width="44" height="44" alt="" style="display:block"></td>
<td style="font:bold 12px/1.35 {TEXT};letter-spacing:1px;color:{INK}">ΣΩΜΑΤΕΙΟ ΜΙΣΘΩΤΩΝ<br>ΤΕΧΝΙΚΩΝ ΜΑΚΕΔΟΝΙΑΣ</td>
</tr></table></td></tr>
<tr><td style="background:{RED};padding:26px 32px 28px">
<div style="font:bold 11px/1.4 {TEXT};letter-spacing:2px;color:{INK};text-transform:uppercase">{esc(d.get('kind', 'Ανακοίνωση'))} · {esc(date)}</div>
<h1 style="margin:10px 0 4px;font:bold 38px/1.0 {DISPLAY};color:{PAPER}">{esc(d['title'])}</h1>
{subs}
</td></tr>
<tr><td style="padding:28px 32px 6px">
{''.join(para(p) for p in excerpt)}
</td></tr>
{event}
<tr><td style="padding:16px 32px 32px">
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="background:{RED}">
<a href="{esc(url)}" style="display:inline-block;padding:14px 22px;font:bold 16px/1.2 {TEXT};color:{PAPER};text-decoration:none">Διάβασε όλη την ανακοίνωση</a>
</td></tr></table>
{pdf_link}
</td></tr>
<tr><td style="padding:20px 32px 26px;border-top:2px solid {INK};font:13px/1.6 {TEXT};color:{GREY}">
<strong style="color:{INK}">Σωματείο Μισθωτών Τεχνικών Μακεδονίας</strong><br>
Εργατικό Κέντρο Θεσσαλονίκης, Αριστοτέλους 32, 5ος όροφος, Θεσσαλονίκη<br>
<a href="{site}/" style="color:{GREY}">{site.replace('https://', '')}</a> · <a href="mailto:info@smtm.gr" style="color:{GREY}">info@smtm.gr</a> · 694 834 9644 · 697 459 2442<br><br>
Το λαμβάνεις γιατί είσαι μέλος ή φίλος του Σωματείου. <a href="{{{{UNSUBSCRIBE}}}}" style="color:{GREY}">Δεν θέλω άλλα email</a>
</td></tr>
</table></td></tr></table>
</body></html>
'''
sys.stdout.write(out)
