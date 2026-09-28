#!/usr/bin/env python3
"""Generate the CV page body from the Word source, preserving emphasis exactly."""
import zipfile, html, re
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
SRC = 'cv.docx'

z = zipfile.ZipFile(SRC)
root = ET.fromstring(z.read('word/document.xml'))
body = root.find(W + 'body')


def runs(p):
    """Yield (text, bold, italic) for each run, merging adjacent like-formatted runs."""
    out = []
    for r in p.iter(W + 'r'):
        rpr = r.find(W + 'rPr')
        b = rpr is not None and rpr.find(W + 'b') is not None
        i = rpr is not None and rpr.find(W + 'i') is not None
        t = ''.join(x.text or '' for x in r.iter(W + 't'))
        if not t:
            continue
        if out and out[-1][1] == b and out[-1][2] == i:
            out[-1][0] += t
        else:
            out.append([t, b, i])
    return out


def render(p):
    parts = []
    for t, b, i in runs(p):
        e = html.escape(t)
        if i:
            e = f'<em>{e}</em>'
        if b:
            e = f'<strong>{e}</strong>'
        parts.append(e)
    s = ''.join(parts)
    # collapse adjacent identical tags produced by Word's run splitting
    s = re.sub(r'</em>(\s*)<em>', r'\1', s)
    s = re.sub(r'</strong>(\s*)<strong>', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def is_list(p):
    ppr = p.find(W + 'pPr')
    return ppr is not None and ppr.find(W + 'numPr') is not None


def style(p):
    ppr = p.find(W + 'pPr')
    if ppr is None:
        return ''
    ps = ppr.find(W + 'pStyle')
    return ps.get(W + 'val', '') if ps is not None else ''


def all_bold(p):
    rs = runs(p)
    return bool(rs) and all(r[1] for r in rs)


# --- walk the document -------------------------------------------------------
header, out = [], []
seen_h2 = False
open_list = False


def close_list():
    global open_list
    if open_list:
        out.append('      </ol>')
        open_list = False


for el in body:
    if el.tag != W + 'p':
        continue
    st = style(el)
    txt = render(el)
    if not txt:
        continue

    if st == 'Heading1':
        continue  # name is rendered in the masthead

    if st == 'Heading2':
        close_list()
        seen_h2 = True
        plain = re.sub('<[^>]+>', '', txt)
        slug = re.sub(r'[^a-z0-9]+', '-', plain.lower()).strip('-')
        out.append(f'\n      <h2 id="{slug}">{plain}</h2>')
        continue

    if not seen_h2:
        header.append(txt)
        continue

    if is_list(el):
        if not open_list:
            out.append('      <ol class="cv-entries">')
            open_list = True
        out.append(f'        <li>{txt}</li>')
    elif all_bold(el):
        close_list()
        plain = re.sub('<[^>]+>', '', txt).strip()
        out.append(f'      <h3>{plain}</h3>')
    else:
        close_list()
        out.append(f'      <p class="cv-line">{txt}</p>')

close_list()

open('cv_header.html', 'w').write('\n'.join(header))
open('cv_body.html', 'w').write('\n'.join(out))
print('header lines:', len(header))
print('body lines  :', len(out))
print('h2 sections :', sum(1 for l in out if '<h2' in l))
print('entries     :', sum(1 for l in out if l.strip().startswith('<li>')))
