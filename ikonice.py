# -*- coding: utf-8 -*-
"""Skup linijskih SVG ikonica (24x24, boja = currentColor).
Upotreba:  ikona("knjiga")  ->  <svg ...>...</svg>
"""

_P = {
    # opšte
    "strelica-desno": ['<path d="M5 12h14"/>', '<path d="m12 5 7 7-7 7"/>'],
    "strelica-dole": ['<path d="m6 9 6 6 6-6"/>'],
    "strelica-levo": ['<path d="m15 18-6-6 6-6"/>'],
    "strelica-desno-mala": ['<path d="m9 18 6-6-6-6"/>'],
    "zatvori": ['<path d="M18 6 6 18"/>', '<path d="m6 6 12 12"/>'],
    "cekiraj": ['<path d="M20 6 9 17l-5-5"/>'],
    "preuzmi": ['<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>', '<path d="m7 10 5 5 5-5"/>', '<path d="M12 15V3"/>'],
    "spoljni": ['<path d="M15 3h6v6"/>', '<path d="M10 14 21 3"/>', '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'],
    "info": ['<circle cx="12" cy="12" r="10"/>', '<path d="M12 16v-4"/>', '<path d="M12 8h.01"/>'],
    "kuca": ['<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>', '<path d="M9 22V12h6v10"/>'],
    # kontakt
    "lokacija": ['<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/>', '<circle cx="12" cy="10" r="3"/>'],
    "telefon": ['<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'],
    "posta": ['<rect x="2" y="4" width="20" height="16" rx="2"/>', '<path d="m22 7-10 6L2 7"/>'],
    # teme
    "globus": ['<circle cx="12" cy="12" r="10"/>', '<path d="M2 12h20"/>', '<path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/>'],
    "avion": ['<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>'],
    "poruka": ['<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'],
    "ljudi": ['<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>', '<circle cx="9" cy="7" r="4"/>', '<path d="M22 21v-2a4 4 0 0 0-3-3.9"/>', '<path d="M16 3.1a4 4 0 0 1 0 7.8"/>'],
    "osoba": ['<circle cx="12" cy="8" r="5"/>', '<path d="M20 21a8 8 0 0 0-16 0"/>'],
    "sijalica": ['<path d="M9 18h6"/>', '<path d="M10 22h4"/>', '<path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V17h6v-.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/>'],
    "monitor": ['<rect x="2" y="3" width="20" height="14" rx="2"/>', '<path d="M8 21h8"/>', '<path d="M12 17v4"/>'],
    "medalja": ['<circle cx="12" cy="8" r="6"/>', '<path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/>'],
    "zgrada": ['<path d="M3 22h18"/>', '<path d="M6 18v-7"/>', '<path d="M10 18v-7"/>', '<path d="M14 18v-7"/>', '<path d="M18 18v-7"/>', '<path d="M12 2 20 7H4z"/>'],
    "knjiga": ['<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/>', '<path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>'],
    "kalendar": ['<rect x="3" y="4" width="18" height="18" rx="2"/>', '<path d="M16 2v4"/>', '<path d="M8 2v4"/>', '<path d="M3 10h18"/>'],
    "srce": ['<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/>'],
    "dokument": ['<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>', '<path d="M14 2v6h6"/>', '<path d="M8 13h8"/>', '<path d="M8 17h5"/>'],
    "sat": ['<circle cx="12" cy="12" r="10"/>', '<path d="M12 6v6l4 2"/>'],
    "kapa": ['<path d="M22 10 12 5 2 10l10 5 10-5z"/>', '<path d="M6 12v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/>'],
    "novine": ['<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/>', '<path d="M18 14h-8"/>', '<path d="M15 18h-5"/>', '<path d="M10 6h8v4h-8z"/>'],
    "mikrofon": ['<rect x="9" y="2" width="6" height="12" rx="3"/>', '<path d="M19 10v1a7 7 0 0 1-14 0v-1"/>', '<path d="M12 18v4"/>'],
    "pehar": ['<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>', '<path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>', '<path d="M4 22h16"/>', '<path d="M10 14.7V17c0 .6-.5 1-1 1.2C7.8 18.8 7 20.2 7 22"/>', '<path d="M14 14.7V17c0 .6.5 1 1 1.2 1.2.6 2 2 2 3.8"/>', '<path d="M18 2H6v7a6 6 0 0 0 12 0z"/>'],
    "olovka": ['<path d="M12 20h9"/>', '<path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>'],
    "kamera": ['<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3z"/>', '<circle cx="12" cy="13" r="3"/>'],
    "slojevi": ['<path d="M12 2 2 7l10 5 10-5z"/>', '<path d="m2 17 10 5 10-5"/>', '<path d="m2 12 10 5 10-5"/>'],
    "list": ['<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/>', '<path d="M2 21c0-3 1.9-5.4 5.2-6.1 2.4-.5 4.9-2 5.8-3.9"/>'],
    "paleta": ['<path d="M12 22a10 10 0 1 1 10-10c0 2.8-2.2 4-4 4h-1.8a2 2 0 0 0-1.4 3.4A1.9 1.9 0 0 1 12 22z"/>', '<circle cx="7.5" cy="10.5" r="1"/>', '<circle cx="12" cy="7" r="1"/>', '<circle cx="16.5" cy="10.5" r="1"/>'],
    "puls": ['<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'],
    "aktovka": ['<rect x="2" y="7" width="20" height="14" rx="2"/>', '<path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>'],
    "autobus": ['<rect x="3" y="3" width="18" height="14" rx="2"/>', '<path d="M3 11h18"/>', '<path d="M12 3v8"/>', '<path d="M7 17v3"/>', '<path d="M17 17v3"/>'],
    "epruveta": ['<path d="M9 3h6"/>', '<path d="M10 3v6.5L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9.5V3"/>', '<path d="M7 15h10"/>'],
    "glasanje": ['<path d="m9 12 2 2 4-4"/>', '<path d="M5 7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v12H5z"/>', '<path d="M22 19H2"/>'],
    "megafon": ['<path d="M3 11v2a1 1 0 0 0 1 1h3l5 4V6L7 10H4a1 1 0 0 0-1 1z"/>', '<path d="M16 9a4 4 0 0 1 0 6"/>', '<path d="M19 6a8 8 0 0 1 0 12"/>'],
    "karta": ['<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/>', '<path d="M13 5v2"/>', '<path d="M13 17v2"/>', '<path d="M13 11v2"/>'],
    "muzika": ['<path d="M9 18V5l12-2v13"/>', '<circle cx="6" cy="18" r="3"/>', '<circle cx="18" cy="16" r="3"/>'],
    "lopta": ['<circle cx="12" cy="12" r="10"/>', '<path d="M2.5 9.5c5 1 10 0 14.5-5"/>', '<path d="M7 3.5c3.5 4 5.5 10 6 18"/>', '<path d="M21.5 13c-4-1-9 0-13 5.5"/>'],
    "cip": ['<rect x="5" y="5" width="14" height="14" rx="2"/>', '<rect x="9" y="9" width="6" height="6"/>', '<path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>'],
    "vaga": ['<path d="M12 3v18"/>', '<path d="M5 21h14"/>', '<path d="M3 7h18"/>', '<path d="m6 7-3 7a3 3 0 0 0 6 0z"/>', '<path d="m18 7-3 7a3 3 0 0 0 6 0z"/>'],
    "osvezi": ['<path d="M3 12a9 9 0 0 1 15-6.7L21 8"/>', '<path d="M21 3v5h-5"/>', '<path d="M21 12a9 9 0 0 1-15 6.7L3 16"/>', '<path d="M3 21v-5h5"/>'],
    "pescani-sat": ['<path d="M5 22h14"/>', '<path d="M5 2h14"/>', '<path d="M17 22v-4.2a2 2 0 0 0-.6-1.4L12 12l-4.4 4.4a2 2 0 0 0-.6 1.4V22"/>', '<path d="M7 2v4.2a2 2 0 0 0 .6 1.4L12 12l4.4-4.4a2 2 0 0 0 .6-1.4V2"/>'],
    "lupa": ['<circle cx="11" cy="11" r="8"/>', '<path d="m21 21-4.3-4.3"/>'],
    "stit": ['<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'],
    "ruke": ['<path d="M11 14h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 16"/>', '<path d="m7 20 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.8-2.8L14.8 13"/>', '<path d="m2 15 6 6"/>'],
    "instagram": ['<rect x="2" y="2" width="20" height="20" rx="5"/>', '<circle cx="12" cy="12" r="4"/>', '<path d="M17.5 6.5h.01"/>'],
    "facebook": ['<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'],
    "navodnici": ['<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.76-2-2-2H4c-1.25 0-2 .75-2 1.97V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .01-1 1.03V20c0 1 0 1 1 1z"/>', '<path d="M15 21c3 0 7-1 7-8V5c0-1.25-.76-2-2-2h-4c-1.25 0-2 .75-2 1.97V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>'],
    "knjige": ['<path d="m16 6 4 14"/>', '<path d="M12 6v14"/>', '<path d="M8 8v12"/>', '<path d="M4 4v16"/>'],
    "vise": ['<path d="M12 5v14"/>', '<path d="M5 12h14"/>'],
}


def ikona(ime, klasa="ik"):
    delovi = "".join(_P[ime])
    return (f'<svg class="{klasa}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{delovi}</svg>')
