# -*- coding: utf-8 -*-
"""Smanjuje fotografije u folderu slike/ i pravi lakše .webp verzije.

Pokretanje (iz foldera sajta):
    pip install pillow
    python3 optimizuj_slike.py
    python3 napravi_stranice.py      # strane tada automatski koriste .webp

- Original se NE briše i ne menja.
- Slike šire od 1920 px smanjuju se na 1920 px (webp verzija).
- Posle ovoga sajt se učitava višestruko brže, naročito na telefonu.
"""
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    raise SystemExit("Potreban je Pillow:  pip install pillow")

MAX_SIRINA = 1920
KVALITET = 80
FOLDER = Path(__file__).parent / "slike"

ukupno_pre = ukupno_posle = 0
for f in sorted(FOLDER.rglob("*")):
    if f.suffix.lower() not in (".jpg", ".jpeg", ".png") or f.name.startswith(("logo-", "favicon", "apple-touch")):
        continue
    cilj = f.with_suffix(".webp")
    if cilj.exists() and cilj.stat().st_mtime >= f.stat().st_mtime:
        continue
    with Image.open(f) as im:
        im = ImageOps.exif_transpose(im)
        if im.width > MAX_SIRINA:
            im = im.resize((MAX_SIRINA, round(im.height * MAX_SIRINA / im.width)), Image.LANCZOS)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        im.save(cilj, "WEBP", quality=KVALITET, method=6)
    pre, posle = f.stat().st_size, cilj.stat().st_size
    ukupno_pre += pre
    ukupno_posle += posle
    print(f"✓ {f.name}: {pre // 1024} KB → {cilj.name}: {posle // 1024} KB")

if ukupno_pre:
    print(f"\nUkupno: {ukupno_pre // 1024} KB → {ukupno_posle // 1024} KB")
else:
    print("Nema novih slika za obradu.")
