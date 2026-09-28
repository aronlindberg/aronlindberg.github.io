# CV tooling

`cv.html` is the source of truth for the CV going forward. Edit it directly —
the Download PDF button prints the page, so the PDF can never drift from it.

These scripts exist only for the one-time (or occasional) case of regenerating
`cv.html` from the Word document:

```bash
cp "/path/to/CV - Aron Lindberg - <date>.docx" cv.docx
python3 gen_cv.py     # docx -> cv_header.html + cv_body.html
python3 build_cv.py   # -> cv.html
```

`gen_cv.py` preserves italics and bold from Word and maps:
Heading2 -> `<h2>`, all-bold paragraph -> `<h3>`, numbered paragraph -> `<li>`.
