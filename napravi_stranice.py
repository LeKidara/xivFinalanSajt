# -*- coding: utf-8 -*-
"""Pravi početnu stranu i sve podstranice sa istim menijem i footerom.

Pokretanje (iz foldera sajta):   python3 napravi_stranice.py

- Tekst podstranica menjaš u rečniku STRANE, a početnu u funkciji pocetna().
- Kontakt podaci su u rečniku KONTAKT (menjaju se na jednom mestu za ceo sajt).
- Vesti se NE menjaju ovde nego u vesti/vesti.js (ili kroz vesti/unos.html).
- Ikonice su u fajlu ikonice.py.
"""
import json
import re
from pathlib import Path
from html import escape
from ikonice import ikona

BASE = Path(__file__).parent

# Podaci sa zvaničnog sajta škole (cetrnaestgim.edu.rs) i edupage.org, septembar 2026.
KONTAKT = {
    "adresa": "Хаџи Проданова 5, 11000 Београд",
    "opstina": "Врачар",
    "telefon": "011 3444 295",
    "telefon_link": "+381113444295",
    "faks": "011 3086 920",
    "email": "direktor@cetrnaestgim.edu.rs",
    "instagram": "https://www.instagram.com/xivgimnazija/",
    "facebook": "https://www.facebook.com/XIV-beogradska-gimnazija-zvani%C4%8Dna-stranica-666411570213279/",
    "mapa": "https://www.google.com/maps/search/?api=1&query=%D0%A5%D0%B0%D1%9F%D0%B8+%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%BD%D0%BE%D0%B2%D0%B0+5+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4",
}

MENI = [
    ("О школи", [
        ("skoli/erasmus.html", "Еразмус"),
        ("skoli/etwinning.html", "еТвининг"),
        ("skoli/istorijat.html", "Историјат"),
        ("skoli/ucenici.html", "Ученик"),
        ("skoli/upis.html", "Упис"),
        ("skoli/zaposleni.html", "Запослени"),
    ]),
    ("Вести", [
        ("vesti/Casopis.html", "Школски часопис"),
        ("vesti/novosti.html", "Новости"),
        ("https://xivgimnazija.wordpress.com/", "Архив"),
    ]),
    ("Настава", [
        ("nastava/IzPred.html", "Изборни предмети"),
        ("nastava/predmeti.html", "Предмети"),
        ("nastava/udzbenici.html", "Уџбеници"),
    ]),
    ("Активности", [
        ("aktivnosti/ekskurzije.html", "Екскурзије и путовања"),
        ("aktivnosti/parlament.html", "Ученички парламент"),
        ("aktivnosti/vannastavneak.html", "Секције и ваннаставне активности"),
    ]),
]
ORG = ("orgrada/organizacijaRada.html", "Организација рада")

FONTOVI = "https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap"


def url(href, p):
    return href if href.startswith("http") else p + href


def spolja(href):
    return ' target="_blank" rel="noopener"' if href.startswith("http") else ""


def odeljak_za(putanja):
    for naziv, linkovi in MENI:
        if any(h == putanja for h, _ in linkovi):
            return naziv, linkovi
    return None, None


def slika(src, p, alt="", klasa="", lenjo=True, prioritet=False, w=1600, h=1000):
    """<img>/<picture>. Ako pored .jpg/.png postoji .webp (napravi ga optimizuj_slike.py),
    pregledač dobija manju .webp verziju."""
    webp = re.sub(r"\.(jpe?g|png)$", ".webp", src, flags=re.I)
    atributi = f' width="{w}" height="{h}" decoding="async"'
    if lenjo:
        atributi += ' loading="lazy"'
    if prioritet:
        atributi += ' fetchpriority="high"'
    kl = f' class="{klasa}"' if klasa else ""
    img = f'<img src="{p}{src}" alt="{alt}"{kl}{atributi}>'
    if webp != src and (BASE / webp).exists():
        return f'<picture><source srcset="{p}{webp}" type="image/webp">{img}</picture>'
    return img


def logo(p, klasa, velicina):
    return (f'<picture><source srcset="{p}slike/logo-xiv-128.webp 1x, {p}slike/logo-xiv-256.webp 2x" type="image/webp">'
            f'<img src="{p}slike/logo-xiv-128.png" srcset="{p}slike/logo-xiv-128.png 1x, {p}slike/logo-xiv-256.png 2x" '
            f'width="{velicina}" height="{velicina}" alt="Лого XIV београдске гимназије" class="{klasa}"></picture>')


# ------------------------------------------------------------------ vesti (iz vesti/vesti.js)

MESECI = ['јануар', 'фебруар', 'март', 'април', 'мај', 'јун', 'јул', 'август', 'септембар', 'октобар', 'новембар', 'децембар']
MESECI_GEN = ['јануара', 'фебруара', 'марта', 'априла', 'маја', 'јуна', 'јула', 'августа', 'септембра', 'октобра', 'новембра', 'децембра']


def ucitaj_vesti():
    try:
        s = (BASE / "vesti" / "vesti.js").read_text(encoding="utf-8")
        telo = s[s.index("window.VESTI = [") + len("window.VESTI = "):s.rindex(";")]
        vesti = json.loads(telo)
    except Exception as e:  # ako je fajl ručno pokvaren, strana i dalje radi
        print("! vesti.js nije moguće pročitati:", e)
        return []
    return sorted([v for v in vesti if v.get("naslov")], key=lambda v: v.get("datum", ""), reverse=True)


def datum_tekst(d):
    m = re.match(r"(\d{4})-(\d{2})(?:-(\d{2}))?", d or "")
    if not m:
        return escape(d or "")
    god, mes = m.group(1), int(m.group(2)) - 1
    if not m.group(3):
        return f"{MESECI[mes]} {god}."
    return f"{int(m.group(3))}. {MESECI_GEN[mes]} {god}."


def vest_link(v, p):
    l = v.get("link", "")
    if not l:
        return ""
    return l if re.match(r"^(https?:|mailto:|#|/)", l) else p + l


# ------------------------------------------------------------------ zajednički delovi

def gornja_traka(p):
    return f'''    <div class="gornja-traka">
        <div class="omot">
            <ul>
                <li class="sakrij-mob"><a href="{KONTAKT["mapa"]}" target="_blank" rel="noopener">{ikona("lokacija")}{KONTAKT["adresa"]}</a></li>
                <li><a href="tel:{KONTAKT["telefon_link"]}">{ikona("telefon")}{KONTAKT["telefon"]}</a></li>
                <li><a href="mailto:{KONTAKT["email"]}">{ikona("posta")}{KONTAKT["email"]}</a></li>
            </ul>
            <div class="drustvene sakrij-mob">
                <a href="{KONTAKT["instagram"]}" target="_blank" rel="noopener" aria-label="Инстаграм">{ikona("instagram")}</a>
                <a href="{KONTAKT["facebook"]}" target="_blank" rel="noopener" aria-label="Фејсбук">{ikona("facebook")}</a>
            </div>
        </div>
    </div>'''


def navbar(p, putanja):
    trenutni, _ = odeljak_za(putanja)
    pocetna_kl = ' class="aktivna" aria-current="page"' if putanja == "index.html" else ""
    stavke = [f'                    <li><a href="{p}index.html"{pocetna_kl}>Почетна</a></li>']
    for naziv, linkovi in MENI:
        kl = ' class="aktivna"' if naziv == trenutni else ""
        pod = "\n".join(
            f'                            <a class="hRed" href="{url(h, p)}"{spolja(h)}>{t}{ikona("strelica-desno")}</a>'
            for h, t in linkovi)
        stavke.append(f'''                    <li class="dropdown">
                        <a href="#"{kl} aria-haspopup="true">{naziv}{ikona("strelica-dole", "ik strelica")}</a>
                        <div class="dropdown-content">
{pod}
                        </div>
                    </li>''')
    kl = ' class="aktivna" aria-current="page"' if putanja == ORG[0] else ""
    stavke.append(f'                    <li><a href="{p}{ORG[0]}"{kl}>{ORG[1]}</a></li>')
    sve = "\n".join(stavke)
    return f'''    <nav class="navbar desktop-navbar" aria-label="Главни мени">
        <div class="omot">
            <div class="navbar-left">
                <a href="{p}index.html" class="navbar-brand">
                    {logo(p, "navbar-logo", 52)}
                    <span class="navbar-title"><small>Четрнаеста</small>београдска гимназија</span>
                </a>
            </div>
            <div class="navbar-center">
                <ul class="navbar-menu">
{sve}
                </ul>
            </div>
            <button class="hamburger" id="hamburger" aria-label="Отвори мени" aria-controls="offcanvas" aria-expanded="false">
                <span class="line"></span>
                <span class="line"></span>
                <span class="line"></span>
            </button>
        </div>
    </nav>'''


def offcanvas(p):
    stavke = [f'            <li><a href="{p}index.html">Почетна</a></li>']
    for naziv, linkovi in MENI:
        pod = "\n".join(
            f'                    <li class="dropdown-content1"><a href="{url(h, p)}"{spolja(h)}>{t}</a></li>'
            for h, t in linkovi)
        stavke.append(f'''            <li>
                <a href="#" class="dropdown-toggle" aria-expanded="false">{naziv}{ikona("strelica-dole")}</a>
                <ul class="dropdown-menu1">
{pod}
                </ul>
            </li>''')
    stavke.append(f'            <li><a href="{p}{ORG[0]}">{ORG[1]}</a></li>')
    sve = "\n".join(stavke)
    return f'''    <div class="offcanvas" id="offcanvas" aria-label="Мени">
        <div class="offcanvas-header">
            Мени
            <button class="exit-btn" id="exit-btn" aria-label="Затвори мени">{ikona("zatvori")}</button>
        </div>
        <ul class="offcanvas-links">
{sve}
        </ul>
        <div class="offcanvas-kontakt">
            <p><a href="tel:{KONTAKT["telefon_link"]}">{ikona("telefon")}{KONTAKT["telefon"]}</a></p>
            <p><a href="mailto:{KONTAKT["email"]}">{ikona("posta")}{KONTAKT["email"]}</a></p>
            <p><a href="{KONTAKT["instagram"]}" target="_blank" rel="noopener">{ikona("instagram")}@xivgimnazija</a></p>
        </div>
    </div>'''


def footer(p):
    brze = [("skoli/upis.html", "Упис"), ("vesti/novosti.html", "Новости"),
            ("nastava/udzbenici.html", "Уџбеници"), (ORG[0], "Распоред звоњења"),
            ("skoli/zaposleni.html", "Запослени")]
    brze_html = "\n".join(f'                    <li><a href="{p}{h}">{t}</a></li>' for h, t in brze)
    return f'''    <footer class="footer">
        <div class="omot footer-content">
            <div>
                <div class="footer-brand">
                    {logo(p, "", 56)}
                    <span>XIV београдска<br>гимназија</span>
                </div>
                <p>Гимназија на Врачару, у центру Београда. Образујемо генерације ученика од 1935. године.</p>
                <div class="drustvene">
                    <a href="{KONTAKT["instagram"]}" target="_blank" rel="noopener" aria-label="Инстаграм">{ikona("instagram")}</a>
                    <a href="{KONTAKT["facebook"]}" target="_blank" rel="noopener" aria-label="Фејсбук">{ikona("facebook")}</a>
                </div>
            </div>
            <div>
                <h2 class="footer-naslov">Брзе везе</h2>
                <ul>
{brze_html}
                </ul>
            </div>
            <div>
                <h2 class="footer-naslov">Контакт</h2>
                <ul class="footer-kontakt">
                    <li>{ikona("lokacija")}<a href="{KONTAKT["mapa"]}" target="_blank" rel="noopener">{KONTAKT["adresa"]}</a></li>
                    <li>{ikona("telefon")}<span><a href="tel:{KONTAKT["telefon_link"]}">{KONTAKT["telefon"]}</a><br><small>факс: {KONTAKT["faks"]}</small></span></li>
                    <li>{ikona("posta")}<a href="mailto:{KONTAKT["email"]}">{KONTAKT["email"]}</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-dno">
            <p class="omot footer-rights">© Четрнаеста београдска гимназија 2026. Сва права задржана. WEB DIZAJN: studio Srbljanović</p>
        </div>
    </footer>'''


def okvir(p, putanja, naslov, opis, css, telo, skripte=()):
    linkovi_css = "\n".join(f'    <link rel="stylesheet" href="{p}{c}">' for c in css)
    dodatne = "".join(f'    <script src="{p}{s}" defer></script>\n' for s in skripte)
    return f'''<!DOCTYPE html>
<html lang="sr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{naslov}</title>
    <meta name="description" content="{escape(opis)}">
    <meta name="theme-color" content="#0E9F7E">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="XIV београдска гимназија">
    <meta property="og:title" content="{escape(naslov)}">
    <meta property="og:description" content="{escape(opis)}">
    <meta property="og:locale" content="sr_RS">

    <link rel="icon" href="{p}favicon.ico" sizes="any">
    <link rel="icon" href="{p}slike/favicon-32.png" type="image/png" sizes="32x32">
    <link rel="icon" href="{p}slike/favicon-192.png" type="image/png" sizes="192x192">
    <link rel="apple-touch-icon" href="{p}slike/apple-touch-icon.png">
    <link rel="manifest" href="{p}site.webmanifest">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="{FONTOVI}">
{linkovi_css}
{dodatne}    <script src="{p}script.js" defer></script>
</head>

<body data-koren="{p}">
    <a class="preskoci" href="#sadrzaj">Пређи на садржај</a>

{gornja_traka(p)}

{navbar(p, putanja)}

    <!-- Mobilni meni -->
{offcanvas(p)}

    <div id="sadrzaj"></div>
{telo}

{footer(p)}
</body>

</html>
'''


# ------------------------------------------------------------------ delovi sadržaja

def kolone(n):
    return 2 if n in (2, 4) else 3


def kartice(stavke):
    """stavke: (ikona, naslov, tekst)"""
    k = "\n".join(f'''            <div class="kartica">
                <div class="ikona">{ikona(i)}</div>
                <h3>{n}</h3>
                <p>{t}</p>
            </div>''' for i, n, t in stavke)
    return f'        <div class="kartice k{kolone(len(stavke))}">\n{k}\n        </div>'


def tabela(zaglavlje, redovi, klasa=""):
    th = "".join(f'<th scope="col">{z}</th>' for z in zaglavlje)
    tr = "\n".join("                    <tr" + (' class="odmor"' if len(r) == 1 else "") + ">" +
                   ("".join(f"<td>{c}</td>" for c in r) if len(r) > 1 else f'<td colspan="{len(zaglavlje)}">{r[0]}</td>') +
                   "</tr>" for r in redovi)
    return f'''        <div class="tabela-omot">
            <table class="tabela {klasa}">
                <thead><tr>{th}</tr></thead>
                <tbody>
{tr}
                </tbody>
            </table>
        </div>'''


def dok(tekst, href="#"):
    return f'<a class="dugme dugme-svetlo" href="{href}">{ikona("preuzmi")}{tekst}</a>'


def veza(tekst, href):
    return f'<a class="dugme dugme-svetlo" href="{href}" target="_blank" rel="noopener">{tekst}{ikona("spoljni")}</a>'


def napomena(tekst):
    return f'        <div class="napomena">{ikona("info")}<p>{tekst}</p></div>'


def citat(tekst, autor):
    return f'''        <figure class="citat">
            {ikona("navodnici")}
            <blockquote>{tekst}</blockquote>
            <figcaption>{autor}</figcaption>
        </figure>'''


def poziv(naslov, tekst, dugme=""):
    return f'''        <div class="poziv">
            <div>
                <h3>{naslov}</h3>
                <p>{tekst}</p>
            </div>
            {dugme}
        </div>'''


def dugme_poziv(tekst, href, novi_prozor=False):
    dod = ' target="_blank" rel="noopener"' if novi_prozor else ""
    return f'<a class="dugme dugme-primarno" href="{href}"{dod}>{tekst}{ikona("strelica-desno")}</a>'


def osobe(lista):
    """lista: (uloga, ime)"""
    k = "\n".join(f'''            <div class="kartica osoba">
                <div class="avatar">{ikona("osoba")}</div>
                <span class="uloga">{u}</span>
                <h3>{i}</h3>
            </div>''' for u, i in lista)
    return f'        <div class="kartice k3 osobe">\n{k}\n        </div>'


STATISTIKA = [("1935.", "година оснивања"), ("32", "одељења"), ("1000+", "ученика"), ("8000+", "књига у библиотеци")]


def statistika():
    s = "\n".join(f'            <div><strong>{b}</strong><span>{t}</span></div>' for b, t in STATISTIKA)
    return f'        <div class="statistika">\n{s}\n        </div>'


# ------------------------------------------------------------------ podstranica

def podstranica(putanja, naslov, ik, podnaslov, sadrzaj, skripte=()):
    p = "../"
    odeljak, linkovi = odeljak_za(putanja)
    mrvice = f'<a href="{p}index.html">{ikona("kuca")}Почетна</a>'
    if odeljak:
        mrvice += ikona("strelica-desno-mala", "ik razdvoj") + f"<span>{odeljak}</span>"
    mrvice += ikona("strelica-desno-mala", "ik razdvoj") + f'<span aria-current="page">{naslov}</span>'

    if linkovi:
        stavke = []
        for h, t in linkovi:
            kl = ' class="trenutna" aria-current="page"' if h == putanja else ""
            znak = ikona("spoljni") if h.startswith("http") else ikona("strelica-desno-mala")
            stavke.append(f'                    <li><a href="{url(h, p)}"{kl}{spolja(h)}>{t}{znak}</a></li>')
        stavke_html = "\n".join(stavke)
        bocni = f'''            <aside class="podmeni" aria-label="{odeljak}">
                <div class="podmeni-naslov">{odeljak}</div>
                <ul>
{stavke_html}
                </ul>
            </aside>
'''
        kl_omot = "stranica-omot"
    else:
        bocni = ""
        kl_omot = "stranica-omot bez-menija"

    telo = f'''    <header class="stranica-hero">
        <div class="omot">
            <div class="ikona-velika">{ikona(ik)}</div>
            <div>
                <nav class="mrvice" aria-label="Путања">{mrvice}</nav>
                <h1>{naslov}</h1>
                <p>{podnaslov}</p>
            </div>
        </div>
    </header>

    <div class="omot">
        <div class="{kl_omot}">
{bocni}            <main class="container">
{sadrzaj}
            </main>
        </div>
    </div>'''
    opis = f"{naslov} – {podnaslov} XIV београдска гимназија, Хаџи Проданова 5, Београд."
    return okvir(p, putanja, f"{naslov} | XIV београдска гимназија", opis,
                 ["navbar.css", "pokusajZaSve.css"], telo, skripte)


# ------------------------------------------------------------------ početna

SLAJDOVI = [
    ("slike/ringispil1.JPG", "Од 1935. године на Врачару", "Добродошли у XIV београдску гимназију",
     "Школа са душом – место где се негују радозналост, одговорност и креативност.",
     [("skoli/upis.html", "Упис у први разред", True), ("skoli/istorijat.html", "О школи", False)]),
    ("slike/ringispil2.JPG", "Секције и пројекти", "Ваннаставне активности",
     "Хор, драмска секција, дебатни клуб, Клуб Уједињених нација и још много тога.",
     [("aktivnosti/vannastavneak.html", "Погледајте секције", True)]),
    ("slike/ringispil3.JPG", "Еразмус+ и еТвининг", "Учимо заједно са Европом",
     "Међународни пројекти и размене са школама из Шпаније, Немачке и других земаља.",
     [("skoli/erasmus.html", "Међународни пројекти", True)]),
]

BRZE_VEZE = [
    ("skoli/upis.html", "kapa", "Упис", "Смерови, документа и изборни програми"),
    ("orgrada/organizacijaRada.html", "sat", "Распоред звоњења", "Преподневна и поподневна смена"),
    ("nastava/udzbenici.html", "knjiga", "Уџбеници", "Спискови и размена уџбеника"),
    ("vesti/Casopis.html", "novine", "Школски часопис", "Часопис „Ad astra“"),
]


def kartica_vesti_pocetna(v, p):
    link = vest_link(v, p) or p + "vesti/novosti.html"
    dod = ' target="_blank" rel="noopener"' if link.startswith("http") else ""
    return f'''                <article class="news-article">
                    <div class="news-meta">
                        <span class="kategorija">{escape(v.get("kategorija", "Вести"))}</span>
                        <span class="datum">{ikona("kalendar")}{datum_tekst(v.get("datum"))}</span>
                    </div>
                    <h3>{escape(v["naslov"])}</h3>
                    <p>{escape(v.get("kratko", ""))}</p>
                    <a href="{link}"{dod} class="link-strelica">Прочитај више{ikona("strelica-desno")}</a>
                </article>'''


def pocetna():
    p = ""
    slajdovi = []
    for i, (src, nad, nasl, tekst, dugmad) in enumerate(SLAJDOVI):
        tag = "h1" if i == 0 else "h2"
        akt = " active" if i == 0 else ""
        dug = "\n".join(
            f'                            <a href="{h}" class="dugme {"dugme-primarno" if prim else "dugme-okvir"}">{t}{ikona("strelica-desno") if prim else ""}</a>'
            for h, t, prim in dugmad)
        slajdovi.append(f'''        <div class="carousel-slide{akt}">
            {slika(src, p, lenjo=(i != 0), prioritet=(i == 0))}
            <div class="carousel-caption">
                <div class="omot">
                    <div class="carousel-tekst">
                        <span class="nadnaslov">{nad}</span>
                        <{tag}>{nasl}</{tag}>
                        <p>{tekst}</p>
                        <div class="hero-dugmad">
{dug}
                        </div>
                    </div>
                </div>
            </div>
        </div>''')
    slajdovi_html = "\n".join(slajdovi)

    brze = "\n".join(f'''                <a href="{h}" class="brzi-link">
                    <span class="ikona">{ikona(ik)}</span>
                    <span><strong>{n}</strong><span>{t}</span></span>
                </a>''' for h, ik, n, t in BRZE_VEZE)

    vesti_html = "\n".join(kartica_vesti_pocetna(v, p) for v in ucitaj_vesti()[:3])

    tacke = "\n".join(f'                        <li>{ikona("cekiraj")}{t}</li>' for t in
                      ["Природно-математички и друштвено-језички смер",
                       "Пет страних језика: немачки, француски, руски, шпански и италијански",
                       "Међународни пројекти Еразмус+ и еТвининг",
                       "Ученички парламент са традицијом од 2001. године"])

    telo = f'''    <main>
    <!-- Ringišpil -->
    <section class="carousel" id="carousel" aria-label="Истакнуто">
{slajdovi_html}
        <div class="carousel-kontrole">
            <div class="omot">
                <button class="carousel-arrow prev" data-smer="-1" aria-label="Претходна слика">{ikona("strelica-levo")}</button>
                <button class="carousel-arrow next" data-smer="1" aria-label="Следећа слика">{ikona("strelica-desno-mala")}</button>
                <div class="carousel-tackice" id="carousel-tackice"></div>
                <div class="carousel-brojac" id="carousel-brojac"></div>
            </div>
        </div>
        <svg class="talas" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true">
            <path d="M0,40 C240,80 480,0 720,32 C960,64 1200,14 1440,38 L1440,80 L0,80 Z"></path>
        </svg>
    </section>

    <!-- Brze veze -->
    <section class="brzi-linkovi" aria-label="Брзе везе">
        <div class="omot">
            <div class="brzi-mreza">
{brze}
            </div>
        </div>
    </section>

    <!-- Školske vesti (automatski iz vesti/vesti.js) -->
    <section class="sekcija">
        <div class="omot">
            <div class="sekcija-zaglavlje">
                <div>
                    <span class="sekcija-oznaka">Шта је ново</span>
                    <h2>Школске вести</h2>
                </div>
                <a href="vesti/novosti.html" class="link-strelica">Све вести{ikona("strelica-desno")}</a>
            </div>
            <div class="news-grid" data-vesti-pocetna="3">
{vesti_html}
            </div>
        </div>
    </section>

    <!-- O školi -->
    <section class="sekcija">
        <div class="omot">
            <div class="about-section reveal">
                <div class="about-image">
                    {slika("slike/skola1.JPG", p, alt="Унутрашњост школе", w=1200, h=900)}
                </div>
                <div class="about-text">
                    <span class="sekcija-oznaka">О нама</span>
                    <h2>О нашој школи</h2>
                    <p>XIV београдска гимназија налази се у центру Београда, на Врачару. Основана је 1935. године и већ деценијама изводи на прави пут хиљаде ђака. Школу данас похађа више од хиљаду ученика у 32 одељења.</p>
                    <ul class="about-tacke">
{tacke}
                    </ul>
                    <a href="skoli/istorijat.html" class="dugme dugme-plavo">Историјат школе{ikona("strelica-desno")}</a>
                </div>
            </div>
{statistika()}
{citat("XIV београдска гимназија није само образовна установа. Она је заједница.", "Марија Милетић, директорка школе")}
        </div>
    </section>
    </main>'''
    opis = ("XIV београдска гимназија – гимназија на Врачару основана 1935. године. "
            "Природно-математички и друштвено-језички смер, упис, вести, распоред звоњења и активности ученика.")
    return okvir(p, "index.html", "XIV београдска гимназија", opis,
                 ["navbar.css", "stil.css", "novosti.css"], telo, ["vesti/vesti.js"])


# ------------------------------------------------------------------ sadržaj podstranica

STRANE = {}

STRANE["skoli/erasmus.html"] = ("Еразмус+", "globus", "Међународна сарадња, мобилности и учење кроз заједничке пројекте са школама из Европе.", f'''
        <p class="uvod">Еразмус+ је програм Европске уније за образовање, обуку, младе и спорт. Кроз њега наши ученици и наставници упознају нове школе, језике и културе.</p>

        <h2>Шта програм пружа ученицима</h2>
{kartice([
    ("avion", "Мобилности", "Боравци у партнерским школама у Европи, уз заједнички рад на пројектима."),
    ("poruka", "Страни језици", "Свакодневна употреба енглеског и других језика у стварним ситуацијама."),
    ("ljudi", "Сарадња", "Рад у међународним тимовима и упознавање вршњака из различитих земаља."),
    ("sijalica", "Нове вештине", "Тимски рад, презентовање, дигиталне вештине и самосталност."),
])}

        <h2>Пројекти школе</h2>
        <ul class="project-list">
            <li><strong>Еразмус+ – Шпанија, Немачка, Србија</strong> – мултилатерални пројекат са партнерским школама из Шпаније и Немачке.</li>
            <li><strong>Еразмус+ у Шпанији</strong> – мобилност ученика и наставника у партнерској школи у Шпанији.</li>
            <li><strong>Еразмус 2023.</strong> – пројектне активности у школској 2022/23. години.</li>
        </ul>
{napomena("Извештаји и презентације пројеката доступни су у школи. Позив за нове мобилности објављује се међу вестима.")}

{poziv("Питања о програму Еразмус+", "Обратите се тиму за међународну сарадњу или пишите на " + KONTAKT["email"] + ".", dugme_poziv("Сајт програма", "https://erasmus-plus.ec.europa.eu/", True))}''')

STRANE["skoli/etwinning.html"] = ("еТвининг", "monitor", "Онлајн пројекти са школама из целе Европе, као део редовне наставе.", f'''
        <div class="year-section">
            <div class="text">
                <h2>Шта је еТвининг</h2>
                <p>еТвининг је европска онлајн заједница школа. Наставници и ученици на безбедној платформи заједно раде на пројектима са вршњацима из других земаља.</p>
                <p>Пројекти се уклапају у редовну наставу језика, историје, биологије, информатике, уметности и других предмета.</p>
            </div>
            <div class="image">
                {slika("slike/ringispil2.JPG", "../", alt="Ученици на пројекту", w=1200, h=900)}
            </div>
        </div>

        <h2>Зашто учествујемо</h2>
{kartice([
    ("globus", "Сарадња без граница", "Рад са ученицима из других земаља без потребе за путовањем."),
    ("slojevi", "Учење кроз пројекте", "Истраживање, писање и представљање заједничких радова."),
    ("medalja", "Ознаке квалитета", "Успешни пројекти могу добити национални и европски знак квалитета."),
])}

        <h2>Пројекти школе</h2>
        <p>Школа учествује у актуелним еТвининг пројектима и редовно представља резултате реализованих пројеката (дисеминација).</p>
{napomena("Списак актуелних и реализованих пројеката биће објављен на овој страни.")}

        <div class="pdf-links">
            {veza("Платформа еТвининг", "https://school-education.ec.europa.eu/en/etwinning")}
        </div>''')

STRANE["skoli/istorijat.html"] = ("Историјат", "zgrada", "Од 1935. године до данас.", f'''
        <p class="uvod">Школа је основана 1935. године. Садашњи назив, XIV београдска гимназија, носи од школске 1953/54. године.</p>

        <div class="slika-okvir">
            {slika("slike/skola1.JPG", "../", alt="Зграда школе", w=1600, h=700)}
        </div>

        <h2>Кроз године</h2>
        <div class="linija">
            <div class="linija-stavka">
                <h3>1935.</h3>
                <p>Почиње образовно-васпитни рад школе под називом VII државна реална гимназија. Касније школа мења назив у VII женска гимназија.</p>
            </div>
            <div class="linija-stavka">
                <h3>1944.</h3>
                <p>Школа ради и током Другог светског рата. На Васкрс 1944. године, у једном од савезничких бомбардовања, зграда је прилично оштећена.</p>
            </div>
            <div class="linija-stavka">
                <h3>1947/48.</h3>
                <p>После рата власници куће у којој је школа одрекли су се власништва у корист Народног одбора за просвету града Београда.</p>
            </div>
            <div class="linija-stavka">
                <h3>1953/54.</h3>
                <p>Школа добија садашњи назив – XIV београдска гимназија.</p>
            </div>
            <div class="linija-stavka">
                <h3>1974.</h3>
                <p>Школа добија још једно име – „Београдски скојевци“.</p>
            </div>
            <div class="linija-stavka">
                <h3>1990.</h3>
                <p>Школа добија нови статут и званично враћа свој стари назив – XIV београдска гимназија.</p>
            </div>
            <div class="linija-stavka">
                <h3>2001.</h3>
                <p>Оснива се ученички парламент, један од најстаријих у београдским школама.</p>
            </div>
            <div class="linija-stavka">
                <h3>2007.</h3>
                <p>Зграда школе је реновирана.</p>
            </div>
            <div class="linija-stavka">
                <h3>2025.</h3>
                <p>Школа обележава 90 година постојања.</p>
            </div>
        </div>

        <h2>Школа данас</h2>
{statistika()}
        <p>Школа има 16 учионица, три рачунарска кабинета, језичку лабораторију са мултимедијалном таблом и библиотеку. Настава физичког васпитања одржава се у оближњем Спортском центру „Врачар“.</p>

{citat("Образовање није само стицање знања, већ и простор у коме се развијају радозналост, одговорност, креативност.", "Марија Милетић, директорка школе")}''')

STRANE["skoli/ucenici.html"] = ("Ученик", "kapa", "Информације, правила и подршка за ученике.", f'''
        <h2>Корисне информације</h2>
{kartice([
    ("sat", "Распоред звоњења", 'Распоред за обе смене налази се на страни <a href="../orgrada/organizacijaRada.html">Организација рада</a>.'),
    ("srce", "ПП служба", "Педагог и психолози школе пружају подршку ученицима и родитељима."),
    ("knjiga", "Библиотека", "Лектира, стручна литература и простор за учење – више од 8000 књига."),
    ("dokument", "Изостанци", "Оправдања се достављају одељењском старешини у прописаном року."),
])}

        <h2>Психолошко-педагошка служба</h2>
{osobe([("Педагог", "Оливера Роглић"), ("Психолог", "Сузана Дракулић"), ("Психолог", "Ивана Јанковић"),
        ("Психолог", "Вања Штулић"), ("Библиотекар", "Маријана Петровић")])}

        <h2>Права и обавезе ученика</h2>
        <div class="columns">
            <div class="column">
                <h3>{ikona("stit")}Ученик има право да:</h3>
                <ul>
                    <li>стиче квалитетно образовање;</li>
                    <li>буде благовремено обавештен о питањима која се тичу школовања;</li>
                    <li>изнесе своје мишљење кроз ученички парламент;</li>
                    <li>добије подршку када му је потребна.</li>
                </ul>
            </div>
            <div class="column">
                <h3>{ikona("dokument")}Ученик је дужан да:</h3>
                <ul>
                    <li>редовно похађа наставу;</li>
                    <li>поштује правила понашања у школи;</li>
                    <li>чува школску имовину;</li>
                    <li>уважава друге ученике и запослене.</li>
                </ul>
            </div>
        </div>

        <div class="pdf-links">
            {dok("Правилник о понашању (PDF)")}
            {dok("Кућни ред школе (PDF)")}
        </div>''')

STRANE["skoli/upis.html"] = ("Упис", "kapa", "Смерови, пријава за упис и потребна документа.", f'''
        <p class="uvod">Упис у први разред обавља се према календару Министарства просвете, на основу резултата завршног испита и успеха из основне школе.</p>

        <h2>Смерови</h2>
        <div class="columns">
            <div class="column">
                <h3>{ikona("epruveta")}Природно-математички смер</h3>
                <p>Четворогодишње школовање за ученике које занимају математика, физика, хемија, биологија и информатика.</p>
            </div>
            <div class="column">
                <h3>{ikona("knjiga")}Друштвено-језички смер</h3>
                <p>Четворогодишње школовање за ученике које занимају језици, књижевност, историја, психологија и друштво.</p>
            </div>
        </div>
        <p>Школа има по осам одељења у сваком разреду. За школску 2025/26. годину уписивано је по 112 ученика на сваком смеру.</p>

        <h2>Пријава за упис</h2>
        <p>Пријава за упис подноси се непосредно у школи, у терминима које школа објављује. За упис 2026. године пријаве су примане 1. и 2. јула, од 8 до 15 часова.</p>

        <h2>Потребна документа</h2>
        <ol class="koraci">
            <li><strong>Пријава за упис</strong>Пријава за упис ученика у средњу школу.</li>
            <li><strong>Уверење о завршном испиту</strong>Уверење о обављеном завршном испиту у основном образовању и васпитању.</li>
            <li><strong>Сведочанство</strong>Сведочанство о завршеном основном образовању и васпитању.</li>
            <li><strong>Извод из матичне књиге рођених</strong>Оригинал или оверена копија.</li>
        </ol>

        <h2>Избори при упису</h2>
        <div class="columns">
            <div class="column">
                <h3>{ikona("poruka")}Други страни језик</h3>
                <p>Немачки, француски, руски, шпански или италијански језик.</p>
            </div>
            <div class="column">
                <h3>{ikona("slojevi")}Два изборна програма</h3>
                <p>Језик, медији и култура · Појединац, група и друштво · Образовање за одрживи развој · Примењене науке.</p>
            </div>
        </div>

{poziv("Упис у средњу школу", "Резултати расподеле и сва званична обавештења објављују се на порталу Моја средња школа.", dugme_poziv("Моја средња школа", "https://mojasrednjaskola.gov.rs/", True))}''')

STRANE["skoli/zaposleni.html"] = ("Запослени", "ljudi", "Управа, стручна служба и наставници школе.", f'''
        <h2>Управа школе</h2>
{osobe([("Директорка", "Марија Милетић"), ("Помоћница директора", "Снежана Миленковић"),
        ("Помоћница директора", "Александра Арсић")])}

        <h2>Стручна служба и администрација</h2>
{osobe([("Педагог", "Оливера Роглић"), ("Психолог", "Сузана Дракулић"), ("Психолог", "Ивана Јанковић"),
        ("Психолог", "Вања Штулић"), ("Библиотекар", "Маријана Петровић"), ("Секретар", "Ивона Ивковић"),
        ("Рачуноводство", "Драгана Саздић-Јотић"), ("Администрација", "Љиљана Николић"), ("Администрација", "Марија Кесегић")])}

        <h2>Наставници по предметима</h2>
        <ul class="grupa">
            <li class="red">Српски језик и књижевност</li>
            <li class="red">Енглески језик</li>
            <li class="red">Немачки језик</li>
            <li class="red">Француски језик</li>
            <li class="red">Руски језик</li>
            <li class="red">Шпански језик</li>
            <li class="red">Латински језик</li>
            <li class="red">Математика</li>
            <li class="red">Физика</li>
            <li class="red">Хемија</li>
            <li class="red">Биологија</li>
            <li class="red">Рачунарство и информатика</li>
            <li class="red">Историја</li>
            <li class="red">Географија</li>
            <li class="red">Филозофија</li>
            <li class="red">Психологија</li>
            <li class="red">Музичка култура</li>
            <li class="red">Ликовна култура</li>
            <li class="red">Физичко васпитање</li>
            <li class="red">Грађанско васпитање</li>
            <li class="red">Верска настава</li>
        </ul>

        <div class="pdf-links">
            {dok("Распоред отворених врата (PDF)")}
        </div>''')

STRANE["vesti/Casopis.html"] = ("Школски часопис", "novine", "„Ad astra“ – часопис који пишу, фотографишу и уређују наши ученици.", f'''
        <p class="uvod">Школски часопис „Ad astra“ настаје у новинарској секцији. Први број представљен је 4. новембра 2024. године у школској библиотеци, у форми вршњачке радионице.</p>

        <h2>Бројеви часописа</h2>
        <div class="kartice k3">
            <div class="kartica broj">
                <div class="korica"><small>Школски часопис</small><b>Ad astra</b></div>
                <h3>Број 1</h3>
                <p>Новембар 2024.</p>
                {dok("Преузми PDF")}
            </div>
        </div>

        <h2>Ко прави часопис</h2>
        <p>Часопис уређују чланови новинарске секције, уз подршку наставница српског језика и књижевности Весне Гвозденац и Дуње Николић, наставнице ликовне културе Соње Бељић и библиотекарке Маријане Петровић.</p>

        <h2>Рубрике</h2>
{kartice([
    ("mikrofon", "Интервјуи", "Разговори са ученицима, наставницима и гостима школе."),
    ("pehar", "Успеси", "Такмичења, награде и пројекти наших ученика."),
    ("olovka", "Литерарни кутак", "Песме, приче и есеји ученика."),
    ("kamera", "Фото-прича", "Најзначајнији тренуци школске године у сликама."),
])}

{poziv("Пишите за часопис", "Новинарска секција прима нове сараднике током целе године.", dugme_poziv("Секције", "../aktivnosti/vannastavneak.html"))}''')


def novosti_sadrzaj():
    p = "../"
    stavke = []
    for v in ucitaj_vesti():
        pasusi = "".join(f"<p>{escape(x)}</p>" for x in (v.get("tekst") or v.get("kratko", "")).split("\n") if x.strip())
        link = vest_link(v, p)
        l_html = ""
        if link:
            dod = ' target="_blank" rel="noopener"' if link.startswith("http") else ""
            l_html = f'<a class="link-strelica" href="{link}"{dod}>Опширније{ikona("spoljni" if link.startswith("http") else "strelica-desno")}</a>'
        stavke.append(f'''            <article class="news-item">
                <span class="datum">{ikona("kalendar")}{datum_tekst(v.get("datum"))} · {escape(v.get("kategorija", "Вести"))}</span>
                <h3>{escape(v["naslov"])}</h3>
                <p class="kratko">{escape(v.get("kratko", ""))}</p>
                <span class="vise">Прочитај више{ikona("strelica-dole")}</span>
                <div class="detaljno">{pasusi}{l_html}</div>
            </article>''')
    lista = "\n".join(stavke)
    return f'''
        <h2>Најновије вести</h2>
        <div class="filteri" data-vesti-filteri></div>
        <div class="news-list" data-vesti-lista>
{lista}
        </div>
        <div class="pdf-links centar">
            <button type="button" class="dugme dugme-svetlo" data-vesti-vise hidden>{ikona("vise")}Прикажи још</button>
            {veza("Архива старих вести", "https://xivgimnazija.wordpress.com/")}
        </div>'''


STRANE["nastava/IzPred.html"] = ("Изборни предмети", "slojevi", "Обавезни изборни предмети, изборни програми и други страни језик.", f'''
        <p class="uvod">Поред обавезних предмета, ученици бирају обавезни изборни предмет, два изборна програма и други страни језик.</p>

        <h2>Обавезни изборни предмет</h2>
        <div class="columns">
            <div class="column">
                <h3>{ikona("knjiga")}Верска настава</h3>
                <p>Упознавање са верском традицијом и вредностима.</p>
            </div>
            <div class="column">
                <h3>{ikona("vaga")}Грађанско васпитање</h3>
                <p>Права, одговорност, дијалог и учешће у заједници.</p>
            </div>
        </div>

        <h2>Изборни програми</h2>
        <p>Ученици првог разреда бирају два од понуђених изборних програма:</p>
{kartice([
    ("kamera", "Језик, медији и култура", "Критичко читање медија и стварање сопственог садржаја."),
    ("ljudi", "Појединац, група и друштво", "Како функционишу групе, друштво и односи међу људима."),
    ("list", "Образовање за одрживи развој", "Екологија, енергија и одговоран однос према природи."),
    ("epruveta", "Примењене науке", "Примена природних наука кроз огледе и пројекте."),
])}

        <h2>Други страни језик</h2>
        <ul class="grupa">
            <li class="red">Немачки језик</li>
            <li class="red">Француски језик</li>
            <li class="red">Руски језик</li>
            <li class="red">Шпански језик</li>
            <li class="red">Италијански језик</li>
        </ul>
{napomena("Понуда изборних програма у старијим разредима зависи од смера. Детаљније информације можете добити од одељењског старешине.")}''')

STRANE["nastava/predmeti.html"] = ("Предмети", "knjiga", "Преглед предмета по областима.", f'''
        <h2>Језици и књижевност</h2>
        <ul class="grupa">
            <li class="red">Српски језик и књижевност</li>
            <li class="red">Енглески језик</li>
            <li class="red">Други страни језик</li>
            <li class="red">Латински језик</li>
        </ul>

        <h2>Природне науке и математика</h2>
        <ul class="grupa">
            <li class="red">Математика</li>
            <li class="red">Физика</li>
            <li class="red">Хемија</li>
            <li class="red">Биологија</li>
            <li class="red">Рачунарство и информатика</li>
            <li class="red">Географија</li>
        </ul>

        <h2>Друштвене науке</h2>
        <ul class="grupa">
            <li class="red">Историја</li>
            <li class="red">Психологија</li>
            <li class="red">Филозофија</li>
            <li class="red">Грађанско васпитање</li>
            <li class="red">Верска настава</li>
        </ul>

        <h2>Уметност и спорт</h2>
        <ul class="grupa">
            <li class="red">Музичка култура</li>
            <li class="red">Ликовна култура</li>
            <li class="red">Физичко и здравствено васпитање</li>
        </ul>

{napomena('Број часова и предмети по разредима разликују се у зависности од смера. Погледајте и страну <a href="IzPred.html">Изборни предмети</a>.')}''')

STRANE["nastava/udzbenici.html"] = ("Уџбеници", "knjiga", "Спискови уџбеника и размена уџбеника.", f'''
        <p class="uvod">Спискови уџбеника објављују се пре почетка школске године. Пре куповине проверите да ли се издање поклапа са списком.</p>

        <h2>Спискови по разредима</h2>
{tabela(["Разред", "Смер", "Списак"], [
    ["I разред", "оба смера", dok("Преузми")],
    ["II разред", "оба смера", dok("Преузми")],
    ["III разред", "оба смера", dok("Преузми")],
    ["IV разред", "оба смера", dok("Преузми")],
])}

        <h2>Размена уџбеника</h2>
        <p>Школа на почетку школске године организује размену уџбеника. У школској 2026/27. години размена је одржана 7. и 8. септембра, од 12 до 15 часова.</p>

        <h2>Препоруке</h2>
{kartice([
    ("osvezi", "Половни уџбеници", "Многи уџбеници могу се преузети од старијих ученика кроз размену."),
    ("cekiraj", "Издавач", "Уџбеник мора бити од истог издавача као на списку."),
    ("pescani-sat", "Куповина", "За поједине предмете наставник на првом часу даје додатна упутства."),
])}''')

STRANE["aktivnosti/ekskurzije.html"] = ("Екскурзије и путовања", "autobus", "Настава ван учионице: екскурзије и студијска путовања.", f'''
        <p class="uvod">Екскурзије се организују у складу са програмом школе и уз сагласност родитеља. Циљ је упознавање културног, историјског и природног наслеђа.</p>

        <h2>Где су ишли наши ученици</h2>
{tabela(["Разред", "Правац"], [
    ["I разред", "Суботица, Нови Сад, Сремски Карловци"],
    ["II разред", "Требиње, Вишеград, Тара"],
    ["III разред", "Студијско путовање у Грчку – Солун, Крф, острво Видо"],
    ["IV разред", "Матурска екскурзија у Италију"],
])}
{napomena("Правци се утврђују сваке школске године. Програм за текућу годину објављује се међу вестима.")}

        <h2>Остала путовања</h2>
{kartice([
    ("zgrada", "Посете установама културе", "Музеји, галерије и позоришта као део наставе."),
    ("epruveta", "Научни излети", "Посете научним центрима, институтима и факултетима."),
    ("globus", "Међународна путовања", "Мобилности у оквиру пројеката Еразмус+."),
])}

        <div class="pdf-links">
            {dok("Програм екскурзија (PDF)")}
            {dok("Сагласност родитеља (PDF)")}
        </div>''')

STRANE["aktivnosti/parlament.html"] = ("Ученички парламент", "glasanje", "Ученички парламент са најдужом традицијом – од 2001. године.", f'''
        <div class="year-section">
            <div class="text">
                <h2>О парламенту</h2>
                <p>XIV београдска гимназија може се похвалити најдужом традицијом ученичког парламентаризма, који постоји од 2001. године.</p>
                <p>Члан парламента може бити сваки ученик школе који је вољан да се укључи у његов рад. Парламент организује и мотивише ученике да осмисле пројекте и акције и учествују у њима, и јача везу између ученика и наставника.</p>
            </div>
            <div class="image">
                {slika("slike/ringispil3.JPG", "../", alt="Ученички парламент", w=1200, h=900)}
            </div>
        </div>

        <h2>Шта смо радили</h2>
{kartice([
    ("sijalica", "Радионице и семинари", "Међу њима и радионица „Жива библиотека – Разбијмо предрасуде“."),
    ("list", "Акције у школи", "Уређење школског дворишта и донације књига."),
    ("srce", "Хуманитарни рад", "Помоћ болесним ученицима, новогодишњи пакетићи за децу без родитеља, помоћ после земљотреса."),
    ("zgrada", "Прикупљање средстава", "Акције за обнову манастира и друге добротворне сврхе."),
])}

        <h2>Европски парламент младих</h2>
        <p>Чланови парламента учествовали су на заседањима Европског парламента младих у Берлину (2004), Кијеву (2006), Загребу (2011) и Естонији (2012).</p>

{poziv("Укључи се у рад парламента", "Сваки ученик који жели да учествује може постати члан парламента.")}''')

SEKCIJE = [
    ("muzika", "Хор", "Певање на школским свечаностима и концертима.", ["наступи"]),
    ("karta", "Драмска секција", "Представе, рецитали и наступи на школским приредбама.", ["позориште"]),
    ("novine", "Новинарска секција", "Писање и уређивање школског часописа „Ad astra“.", ["часопис"]),
    ("mikrofon", "Дебатни клуб", "Аргументација, јавни наступ и дебатна такмичења.", ["такмичења"]),
    ("globus", "Клуб Уједињених нација", "Теме међународних односа и организације УН.", ["симулације"]),
    ("poruka", "Лингвистичка секција", "Језици, лингвистика и припрема за такмичења.", ["језици"]),
    ("knjiga", "Веронаучна секција", "Активности у оквиру верске наставе.", ["радионице"]),
    ("paleta", "Ликовне изложбе", "Ученици стварају и организују изложбе својих радова.", ["изложбе"]),
    ("srce", "Хуманитарне акције", "Акције прикупљања помоћи и волонтирање.", ["волонтирање"]),
    ("epruveta", "Радионица прављења сапуна", "Креативна практична радионица.", ["радионица"]),
]
sekcije_html = "\n".join(f'''            <div class="aktivnost">
                <div class="ikona-krug">{ikona(i)}</div>
                <div class="info">
                    <h3>{n}</h3>
                    <p>{t}</p>
                    <div class="oznake">{"".join(f"<span>{o}</span>" for o in oz)}</div>
                </div>
            </div>''' for i, n, t, oz in SEKCIJE)

STRANE["aktivnosti/vannastavneak.html"] = ("Секције и ваннаставне активности", "paleta", "Активности после наставе за све ученике.", f'''
        <p class="uvod">Понуда секција и ваннаставних активности прилагођава се интересовањима ученика. Ученици учествују и у културним и уметничким догађајима и посетама установама културе.</p>

        <h2>Секције</h2>
        <div class="aktivnosti-grid">
{sekcije_html}
        </div>

{poziv("Пријава за секцију", "Јавите се наставнику који води секцију или одељењском старешини.")}''')

STRANE["orgrada/organizacijaRada.html"] = ("Организација рада", "sat", "Распоред звоњења, смене и школски календар.", f'''
        <h2>Распоред звоњења 2026/27.</h2>
{tabela(["Час", "Преподневна смена", "Поподневна смена"], [
    ["1.", "7:45 – 8:30", "14:00 – 14:45"],
    ["2.", "8:35 – 9:20", "14:50 – 15:35"],
    ["Велики одмор – 20 минута"],
    ["3.", "9:40 – 10:25", "15:55 – 16:40"],
    ["4.", "10:30 – 11:15", "16:45 – 17:30"],
    ["Одмор – 10 минута"],
    ["5.", "11:25 – 12:10", "17:40 – 18:25"],
    ["6.", "12:15 – 13:00", "18:30 – 19:15"],
    ["7.", "13:05 – 13:50", "19:20 – 20:05"],
])}

        <h2>Документа</h2>
{kartice([
    ("sat", "Распоред часова", '<a href="#">Преузми PDF' + ikona("preuzmi") + '</a>'),
    ("kalendar", "Школски календар", '<a href="#">Преузми PDF' + ikona("preuzmi") + '</a>'),
    ("olovka", "Распоред писаних провера", '<a href="#">Преузми PDF' + ikona("preuzmi") + '</a>'),
    ("ljudi", "Отворена врата", '<a href="#">Термини за родитеље' + ikona("preuzmi") + '</a>'),
    ("zgrada", "Распоред по учионицама", '<a href="#">Преузми PDF' + ikona("preuzmi") + '</a>'),
    ("knjige", "Допунска и додатна настава", '<a href="#">Преузми PDF' + ikona("preuzmi") + '</a>'),
])}''')


if __name__ == "__main__":
    STRANE["vesti/novosti.html"] = ("Новости", "megafon", "Вести и обавештења из живота школе.", novosti_sadrzaj())
    (BASE / "index.html").write_text(pocetna(), encoding="utf-8")
    print("✓ index.html")
    for putanja, (naslov, ik, podnaslov, sadrzaj) in STRANE.items():
        f = BASE / putanja
        f.parent.mkdir(parents=True, exist_ok=True)
        skripte = ["vesti/vesti.js"] if putanja == "vesti/novosti.html" else []
        f.write_text(podstranica(putanja, naslov, ik, podnaslov, sadrzaj, skripte), encoding="utf-8")
        print("✓", putanja)
