/* ==========================================================================
   VESTI ŠKOLE
   --------------------------------------------------------------------------
   Najlakše: otvori vesti/unos.html u pregledaču, dodaj vest kroz formular
   i preuzmi novi vesti.js koji zameni ovaj fajl.

   Ručno: dodaj novi blok { ... } u listu (redosled nije bitan, sortira se po datumu).
   Ključevi moraju biti pod navodnicima, kao u primerima ispod. Polja:
     datum      "2026-09-01"  (ili samo "2026-09" ako dan nije poznat)
     kategorija npr. "Обавештење", "Настава", "Ученици", "Такмичења", "Часопис"
     naslov     naslov vesti
     kratko     jedna-dve rečenice (prikazuju se na početnoj)
     tekst      duži tekst (prikazuje se na strani Новости); nov red = novi pasus
     link       (nije obavezno) adresa dokumenta ili stranice sa više detalja
     slika      (nije obavezno) putanja do slike, npr. "slike/vesti/koncert.webp"

   Opciono: ako škola objavljuje vesti na WordPress blogu, upiši adresu bloga
   u VESTI_WORDPRESS i te vesti će se automatski dodati na sajt.
   ========================================================================== */

window.VESTI_WORDPRESS = "";   // npr. "xivgimnazija.wordpress.com"

window.VESTI = [
    {
        "datum": "2026-09",
        "kategorija": "Обавештење",
        "naslov": "Ученичке стипендије за школску 2026/2027. годину",
        "kratko": "Објављено је обавештење и допуна обавештења о документацији и роковима за ученичке стипендије.",
        "tekst": "Обавештење и допуну обавештења о потребној документацији и роковима за ученичке стипендије за школску 2026/2027. годину можете погледати на сајту школе.",
        "link": "https://cetrnaestgim.edu.rs/"
    },
    {
        "datum": "2026-09",
        "kategorija": "Настава",
        "naslov": "Настава шпанског језика суботом",
        "kratko": "Настава шпанског језика за ученике других школа неће се одржати 12. септембра, а наставља се 19. септембра.",
        "tekst": "Обавештавамо ученике других школа који суботом похађају наставу шпанског језика у нашој школи да се настава неће одржати у суботу 12. септембра.\nНастава се наставља у суботу 19. септембра.",
        "link": "https://cetrnaestgim.edu.rs/"
    },
    {
        "datum": "2026-09-07",
        "kategorija": "Ученици",
        "naslov": "Размена уџбеника",
        "kratko": "Размена уџбеника биће организована у понедељак 7.9. и уторак 8.9. од 12 до 15 часова.",
        "tekst": "Размена уџбеника биће организована у понедељак 7. септембра и уторак 8. септембра, у периоду од 12 до 15 часова.",
        "link": ""
    },
    {
        "datum": "2026-09-01",
        "kategorija": "Обавештење",
        "naslov": "Почетак нове школске године 2026/27",
        "kratko": "Школска година почиње 1. септембра 2026. године. Добродошли!",
        "tekst": "Школска 2026/27. година почиње у уторак, 1. септембра 2026. године.\nРаспоред одељења по учионицама и распоред звоњења налазе се на страни Организација рада.",
        "link": ""
    },
    {
        "datum": "2026-08-31",
        "kategorija": "Ученици",
        "naslov": "Распоред ученика првих разреда по одељењима",
        "kratko": "Спискови ученика првог разреда по одељењима биће унети у есДневник у понедељак 31. августа.",
        "tekst": "Спискови ученика првих разреда по одељењима за школску 2026/2027. годину биће унети у есДневник у понедељак 31. августа.",
        "link": ""
    },
    {
        "datum": "2024-11-04",
        "kategorija": "Часопис",
        "naslov": "Представљен први број школског часописа „Ad astra“",
        "kratko": "Чланови новинарске секције представили су први број школског часописа у библиотеци школе.",
        "tekst": "Први број школског часописа „Ad astra“ представљен је 4. новембра 2024. године у библиотеци школе, у форми вршњачке радионице коју су водили чланови новинарске секције.",
        "link": "vesti/Casopis.html"
    }
];
