#!/usr/bin/env python3
"""Build the homepage: template.html + previews read from the sibling projects -> index.html.

Expects momente/, rafturi/ and sublinieri/ next to this folder (as in ~/Life).
Usage: python3 build.py
"""
import glob
import html
import json
import os
import re
import shutil

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
LIFE = os.path.dirname(ROOT)

# the Momente mosaic: COLS x ROWS photo tiles, sampled evenly over the years
COLS, ROWS = 48, 9
TILE, GAP = 40, 2  # px, the image is shown at about half size
# how many of the latest read books the Rafturi shelf shows
COVERS = 7
# Sublinieri quotes short enough to show whole on the card
QUOTE_WORDS = 32


def momente():
    photos = json.load(open(os.path.join(LIFE, 'momente', 'data', 'photos.json'), encoding='utf-8'))
    photos = sorted((p for p in photos if not p.get('hidden') and not p.get('story')), key=lambda p: p['date'])
    thumbs = [t for t in (os.path.join(LIFE, 'momente', 'thumbs', p['date'][:4], p['id'] + '.jpg') for p in photos)
              if os.path.exists(t)]
    n = COLS * ROWS
    picked = [thumbs[i * len(thumbs) // n] for i in range(n)]
    pitch = TILE + GAP
    # transparent gaps, so the card shows through in both themes
    mosaic = Image.new('RGBA', (COLS * pitch - GAP, ROWS * pitch - GAP), (0, 0, 0, 0))
    for i, t in enumerate(picked):
        tile = Image.open(t).convert('RGB').resize((TILE, TILE), Image.LANCZOS)
        mosaic.paste(tile, ((i % COLS) * pitch, (i // COLS) * pitch))
    mosaic.save(os.path.join(ROOT, 'mosaic.webp'), quality=80)
    first, last = photos[0]['date'][:4], photos[-1]['date'][:4]
    return f'{len(photos):,}'.replace(',', '.') + f' fotografii · {first}–{last}'


def rafturi():
    data = json.load(open(os.path.join(LIFE, 'rafturi', 'data', 'books.json'), encoding='utf-8'))
    books = data['read'][:COVERS]
    out = os.path.join(ROOT, 'covers')
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    imgs = []
    for b in books:
        src = os.path.join(LIFE, 'rafturi', 'covers', b['book_id'] + '.jpg')
        if os.path.exists(src):
            shutil.copy(src, out)
            imgs.append(f'<img src="covers/{b["book_id"]}.jpg" alt="{html.escape(b["title"])}" loading="lazy">')
    return ''.join(imgs), f'{len(data["read"])} de cărți citite · {len(data["currently"])} în curs'


def sublinieri():
    quotes = []
    files = sorted(glob.glob(os.path.join(LIFE, 'sublinieri', 'entries', '*.md')))
    for path in files:
        m = re.match(r'---\n(.*?)\n---\n?(.*)', open(path, encoding='utf-8').read(), re.S)
        meta = dict(line.split(': ', 1) for line in m.group(1).splitlines() if ': ' in line)
        body = ' '.join(m.group(2).replace('<!-- more -->', '').split())
        if meta.get('kind', 'quote') == 'quote' and meta.get('style') != 'dialogue' \
                and body and len(body.split()) <= QUOTE_WORDS:
            quotes.append({'text': body, 'source': meta['source'].split(',')[0]})
    return json.dumps(quotes, ensure_ascii=False), f'{len(files)} de citate și note'


def main():
    momente_meta = momente()
    covers, rafturi_meta = rafturi()
    quotes, sublinieri_meta = sublinieri()
    page = open(os.path.join(ROOT, 'template.html'), encoding='utf-8').read()
    for key, value in {'MOMENTE_META': momente_meta,
                       'COVERS': covers, 'RAFTURI_META': rafturi_meta,
                       'QUOTES': quotes, 'SUBLINIERI_META': sublinieri_meta}.items():
        page = page.replace('{{' + key + '}}', value)
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
    print(f'index.html: {momente_meta}; {rafturi_meta}; {sublinieri_meta}')


if __name__ == '__main__':
    main()
