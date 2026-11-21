#!/usr/bin/env python3
"""Turn a ΣΜΤΜ announcement source (.txt with @tags, the format of
anakoinoseis/tools/build_announcement.py) into an HTML fragment for the web.

Usage: announce2html.py source.txt > fragment.html
Prints JSON with title, subtitle lines and body HTML when --json is given.
"""
import html, json, re, sys

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'__(.+?)__', r'<em>\1</em>', s)
    s = re.sub(r'\[\[(.+?)\]\]', r'<mark>\1</mark>', s)
    return s

def slashes(s):
    # print uses "/" between slogans inside a box line; keep them, styled
    parts = [p.strip() for p in s.split('/')]
    return '<span class="sl">/</span> '.join(inline(p) for p in parts if p)

def convert(text):
    title, sub, body = '', [], []
    box = None          # list of html chunks while inside a demands box
    sub_items = None    # nested bullets inside the box
    bullets = None
    closing = []

    def flush_bullets():
        nonlocal bullets
        if bullets:
            body.append('<ul class="a-bullets">' + ''.join(f'<li>{b}</li>' for b in bullets) + '</ul>')
        bullets = None

    def flush_sub():
        nonlocal sub_items
        if sub_items and box is not None:
            box.append('<ul class="a-wages">' + ''.join(f'<li>{b}</li>' for b in sub_items) + '</ul>')
        sub_items = None

    def flush_box():
        nonlocal box
        flush_sub()
        if box is not None:
            body.append('<aside class="a-box">' + ''.join(box) + '</aside>')
        box = None

    def flush_closing():
        nonlocal closing
        if closing:
            body.append('<div class="a-closing">' + ''.join(f'<p>{c}</p>' for c in closing) + '</div>')
        closing = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        m = re.match(r'@([a-z+\-0-9]+)\s?(.*)', line)
        if not m:
            continue
        tag, rest = m.group(1), m.group(2)
        if tag not in ('box', 'boxb', 'boxc'):
            flush_box()
        if tag != 'b':
            flush_bullets()
        if tag not in ('c', 'c+'):
            flush_closing()
        if tag == 'title':
            title = rest
        elif tag == 'sub':
            sub = rest.split('|')
        elif tag.startswith('p'):
            body.append(f'<p>{inline(rest)}</p>')
        elif tag in ('h', 'hc'):
            body.append('<h2>' + '<br>'.join(inline(x) for x in rest.split('|')) + '</h2>')
        elif tag == 'b':
            bullets = (bullets or []) + [inline(rest)]
        elif tag == 'box':
            if box is None:
                box = [f'<p class="a-box-head">{inline(rest)}</p>']
            else:
                flush_sub()
                item = rest[1:] if rest.startswith('-') else rest
                box.append(f'<p class="a-box-item">{slashes(item)}</p>')
        elif tag == 'boxb':
            sub_items = (sub_items or []) + [inline(rest)]
        elif tag == 'boxc':
            flush_sub()
            box.append(f'<p class="a-box-note">{inline(rest)}</p>')
        elif tag in ('c', 'c+'):
            closing.append(inline(rest))
        elif tag == 'cm':
            body.append('<p class="a-callout">' + '<br>'.join(inline(x) for x in rest.split('|')) + '</p>')
        elif tag == 'q':
            body.append(f'<blockquote>{inline(rest)}</blockquote>')
        elif tag == 'r':
            body.append(f'<p class="a-right">{inline(rest)}</p>')
    flush_box(); flush_bullets(); flush_closing()
    return {'title': title, 'sub': sub, 'html': '\n'.join(body)}

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    src = open(args[0], encoding='utf-8').read()
    out = convert(src)
    if '--json' in sys.argv:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print(out['html'])
