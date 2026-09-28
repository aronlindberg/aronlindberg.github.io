#!/usr/bin/env python3
"""Assemble cv.html from the generated body fragment."""
import re, pathlib

body = open('cv_body.html').read()

# Wrap ranking markers like [UTD24, FT50] / [ABS 4*] / [IF 6.988] as styled tags
body = re.sub(r'\[([A-Z][^\]]{0,24})\]', r'<span class="tag">\1</span>', body)

SECTIONS = re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>', body)
nav = '\n'.join(
    f'        <a href="#{sid}">{name}</a>' for sid, name in SECTIONS
)

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Curriculum Vitae — Aron Lindberg</title>
  <meta name="description" content="Curriculum vitae of Aron Lindberg, Associate Professor of Information Systems at Stevens Institute of Technology." />
  <link rel="icon" href="images/favicon.svg" type="image/svg+xml" />
  <!-- Bump ?v= whenever cv.css changes so browsers can't serve a stale copy. -->
  <link rel="stylesheet" href="css/cv.css?v=1" />
</head>
<body>

<!-- Toolbar: hidden in print via @media print -->
<div class="cv-toolbar">
  <div class="cv-toolbar-inner">
    <a class="cv-back" href="index.html">&larr; aronlindberg.com</a>
    <button type="button" class="cv-download" onclick="window.print()">
      Download PDF
    </button>
  </div>
</div>

<main class="cv">

  <header class="cv-head">
    <h1>Aron Lindberg</h1>
    <p class="cv-affil">
      Stevens Institute of Technology, School of Business<br />
      Information Systems &amp; Analytics Area
    </p>
    <p class="cv-contact">
      Castle Point on Hudson, Hoboken NJ 07030-5991 USA<br />
      <a href="mailto:aron.lindberg@stevens.edu">aron.lindberg@stevens.edu</a>
    </p>
  </header>

  <!-- Section jump links: screen only -->
  <nav class="cv-jump" aria-label="CV sections">
{NAV}
  </nav>

{BODY}

</main>

<footer class="cv-foot">
  <p>Last updated May 26, 2026 &middot; <a href="index.html">aronlindberg.com</a></p>
</footer>

</body>
</html>
'''

out = TEMPLATE.replace('{NAV}', nav).replace('{BODY}', body.strip('\n'))
pathlib.Path('cv.html').write_text(out)
print('sections:', len(SECTIONS))
print('bytes   :', len(out))
