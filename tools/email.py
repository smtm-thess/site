#!/usr/bin/env python3
"""Φτιάχνει το email μιας ανακοίνωσης για το Sender, από το ίδιο .md του site.

Παράδειγμα:
  python3 tools/email.py src/content/anakoinoseis/2026-11-16-apergoume-25-noemvri.md > email.html

Στο Sender: Email campaigns, New campaign, Design, Custom HTML email, επικόλληση.
Το {{unsubscribe_link}} είναι η ετικέτα του Sender για τον σύνδεσμο διαγραφής (υποχρεωτική).
Το email έχει την αρχή του κειμένου και κουμπί για όλη την ανακοίνωση στο site.
Επιλογές: --site https://smtm.gr  --paras 3 (πόσες παράγραφοι της αρχής)
          --note-title «Νέο site, νέο email» --note «κείμενο (επιτρέπεται <strong>)»: πλαίσιο πριν το υποσέλιδο
Αν υπάρχει public/email/<slug>-video.jpg (tools/video_thumb.py), το βίντεο μπαίνει ως εικόνα με ▶.
Οι σύνδεσμοι προς το site έχουν ?ref=email, για να μετράει το GoatCounter από πού ήρθαν.
"""
import argparse, html, os, re, sys, unicodedata
import yaml

ap = argparse.ArgumentParser()
ap.add_argument('md')
ap.add_argument('--site', default='https://smtm.gr')
ap.add_argument('--paras', type=int, default=3)
ap.add_argument('--note-title', default='')
ap.add_argument('--note', default='')
a = ap.parse_args()

src = open(a.md, encoding='utf-8').read()
_, fm, body = src.split('---', 2)
d = yaml.safe_load(fm)
slug = os.path.splitext(os.path.basename(a.md))[0]
site = a.site.rstrip('/')
url = f'{site}/anakoinoseis/{slug}/'
REF = '?ref=email'
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

def caps(s):
    # Κεφαλαία χωρίς τόνους, γραμμένα στο ίδιο το κείμενο: το Gmail αγνοεί τη γλώσσα της
    # σελίδας, και με text-transform θα έβγαζε «ΑΝΑΚΟΊΝΩΣΗ».
    s = unicodedata.normalize('NFD', str(s))
    s = ''.join(c for c in s if c not in '\u0301\u0300\u0342')
    return unicodedata.normalize('NFC', s).upper()

def para(p):
    p = p.replace('<strong>', f'<strong style="color:{INK}">')
    return f'<p style="margin:0 0 16px;font:16px/1.6 {TEXT};color:#2A2723">{p}</p>'

event = ''
if d.get('event'):
    e = d['event']
    event = f'''<tr><td style="padding:0 32px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="background:{INK};padding:18px 20px">
<div style="font:bold 11px/1.4 {TEXT};letter-spacing:2px;color:#F3A69F;text-transform:uppercase">{esc(caps(e['label']))}</div>
<div style="font:bold 26px/1.1 {DISPLAY};color:{PAPER};margin-top:6px">{esc(e['when'])}</div>
<div style="font:bold 17px/1.3 {DISPLAY};color:{PAPER};margin-top:6px">{esc(e['where'])}</div>
</td></tr></table></td></tr>'''

subs = ''.join(f'<div style="font:bold 17px/1.25 {DISPLAY};color:{INK if i else PAPER};margin-top:6px">{esc(s)}</div>'
               for i, s in enumerate(d.get('sub') or []))
pdf_link = (f'<p style="margin:14px 0 0;font:14px/1.5 {TEXT}"><a href="{esc(pdf)}" style="color:{INK};font-weight:bold">Κατέβασε το PDF για μοίρασμα</a></p>'
            if pdf else '')
video = ''
thumb = f'public/email/{slug}-video.jpg'
if d.get('video') and os.path.exists(thumb):
    # Εικόνα με ▶ που ανοίγει το βίντεο στο site (τα email δεν παίζουν βίντεο).
    # Τη φτιάχνει το tools/video_thumb.py από τρία καρέ του βίντεο.
    import subprocess
    dur = ''
    try:
        sec = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                    'public' + (d['video']['src'] if isinstance(d['video'], dict) else d['video'])],
                                   capture_output=True, text=True).stdout)
        dur = f' · {int(sec // 60)}:{int(round(sec % 60)):02d}'
    except Exception:
        pass
    vurl = esc(url + REF) + '#video'
    video = f'''<tr><td style="padding:16px 32px 4px">
<a href="{vurl}" style="text-decoration:none"><img src="{site}/email/{slug}-video.jpg" width="536" alt="▶ Δες το βίντεο της απεργίας" style="display:block;width:100%;max-width:536px;height:auto;border:0"></a>
<p style="margin:10px 0 0;font:bold 15px/1.4 {TEXT}"><a href="{vurl}" style="color:{INK}">▶ Δες το βίντεο της απεργίας{dur}</a></p>
</td></tr>'''
elif d.get('video'):
    pdf_link = (f'<p style="margin:14px 0 0;font:14px/1.5 {TEXT}"><a href="{esc(url + REF)}#video" style="color:{INK};font-weight:bold">Δες το βίντεο της απεργίας</a></p>'
                + pdf_link.replace('margin:14px', 'margin:6px'))

note = ''
if a.note:
    title = f'<div style="font:bold 11px/1.4 {TEXT};letter-spacing:2px;color:{RED};text-transform:uppercase;margin-bottom:8px">{esc(caps(a.note_title))}</div>' if a.note_title else ''
    note = f'''<tr><td style="padding:0 32px 28px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="background:{PAPER2};border-left:4px solid {RED};padding:16px 20px">
{title}<div style="font:15px/1.55 {TEXT};color:#2A2723">{a.note.replace('<strong>', f'<strong style="color:{INK}">')}</div>
</td></tr></table></td></tr>'''

out = f'''<!DOCTYPE html>
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
<div style="font:bold 11px/1.4 {TEXT};letter-spacing:2px;color:{INK};text-transform:uppercase">{esc(caps(d.get('kind', 'Ανακοίνωση')))} · {esc(caps(date))}</div>
<h1 style="margin:10px 0 4px;font:bold 38px/1.0 {DISPLAY};color:{PAPER}">{esc(d['title'])}</h1>
{subs}
</td></tr>
<tr><td style="padding:28px 32px 6px">
{''.join(para(p) for p in excerpt)}
</td></tr>
{event}
{video}
<tr><td style="padding:16px 32px 32px">
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="background:{RED}">
<a href="{esc(url + REF)}" style="display:inline-block;padding:14px 22px;font:bold 16px/1.2 {TEXT};color:{PAPER};text-decoration:none">Διάβασε όλη την ανακοίνωση</a>
</td></tr></table>
{pdf_link}
</td></tr>
{note}
<tr><td style="padding:20px 32px 26px;border-top:2px solid {INK};font:13px/1.6 {TEXT};color:{GREY}">
<strong style="color:{INK}">Σωματείο Μισθωτών Τεχνικών Μακεδονίας</strong><br>
Εργατικό Κέντρο Θεσσαλονίκης, Αριστοτέλους 32, 5ος όροφος, Θεσσαλονίκη<br>
<a href="{site}/{REF}" style="color:{GREY}">{site.replace('https://', '')}</a> · <a href="mailto:info@smtm.gr" style="color:{GREY}">info@smtm.gr</a> · 694 834 9644 · 697 459 2442<br><br>
Το λαμβάνεις γιατί είσαι μέλος ή φίλος του Σωματείου. <a href="{{{{unsubscribe_link}}}}" style="color:{GREY}">Δεν θέλω άλλα email</a>
</td></tr>
</table></td></tr></table>
</body></html>
'''
sys.stdout.write(out)
