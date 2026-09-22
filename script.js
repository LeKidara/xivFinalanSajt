/* Meni, mobilni meni, ringišpil, animacije i dinamične vesti.
   Svaki deo proverava da li element postoji, pa isti fajl radi na svim stranama.
*/
(function () {
    'use strict';
    document.documentElement.classList.add('js');

    const KOREN = document.body.dataset.koren || '';

    /* ---------- Senka menija pri skrolovanju ---------- */
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const proveri = () => navbar.classList.toggle('skrolovano', window.scrollY > 10);
        window.addEventListener('scroll', proveri, { passive: true });
        proveri();
    }

    /* ---------- Mobilni meni ---------- */
    const hamburger = document.getElementById('hamburger');
    const offcanvas = document.getElementById('offcanvas');
    const exitBtn = document.getElementById('exit-btn');

    function closeMenu() {
        if (!offcanvas) return;
        offcanvas.classList.remove('open');
        document.body.classList.remove('menu-open');
        if (hamburger) {
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    }

    function openMenu() {
        offcanvas.classList.add('open');
        document.body.classList.add('menu-open');
        hamburger.classList.add('active');
        hamburger.setAttribute('aria-expanded', 'true');
    }

    if (hamburger && offcanvas) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            offcanvas.classList.contains('open') ? closeMenu() : openMenu();
        });
    }

    if (exitBtn) exitBtn.addEventListener('click', closeMenu);

    document.addEventListener('click', (e) => {
        if (offcanvas && offcanvas.classList.contains('open') && !offcanvas.contains(e.target)) closeMenu();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeMenu();
    });

    document.querySelectorAll('.offcanvas-links a:not(.dropdown-toggle)').forEach(a => a.addEventListener('click', closeMenu));

    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const otvoren = toggle.classList.contains('active');
            document.querySelectorAll('.dropdown-toggle').forEach(t => {
                t.classList.remove('active');
                t.setAttribute('aria-expanded', 'false');
            });
            if (!otvoren) {
                toggle.classList.add('active');
                toggle.setAttribute('aria-expanded', 'true');
            }
        });
    });

    /* ---------- Ringišpil ---------- */
    (function () {
        const slides = document.querySelectorAll('.carousel-slide');
        if (!slides.length) return;

        const tackiceBox = document.getElementById('carousel-tackice');
        const brojac = document.getElementById('carousel-brojac');
        const tackice = [];
        let current = 0;
        let timer = null;
        const dva = n => String(n).padStart(2, '0');
        const smanjenoKretanje = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        function show(index) {
            slides[current].classList.remove('active');
            if (tackice[current]) tackice[current].classList.remove('active');
            current = (index + slides.length) % slides.length;
            slides[current].classList.add('active');
            if (tackice[current]) tackice[current].classList.add('active');
            if (brojac) brojac.innerHTML = '<strong>' + dva(current + 1) + '</strong> / ' + dva(slides.length);
        }

        function restart() {
            clearInterval(timer);
            if (!smanjenoKretanje) timer = setInterval(() => show(current + 1), 7000);
        }

        if (tackiceBox) {
            slides.forEach((_, i) => {
                const b = document.createElement('button');
                b.type = 'button';
                b.setAttribute('aria-label', 'Слајд ' + (i + 1));
                if (i === 0) b.classList.add('active');
                b.addEventListener('click', () => { show(i); restart(); });
                tackiceBox.appendChild(b);
                tackice.push(b);
            });
        }

        document.querySelectorAll('.carousel-arrow').forEach(btn => {
            btn.addEventListener('click', () => {
                show(current + Number(btn.dataset.smer || 1));
                restart();
            });
        });

        // pauza kad kartica nije vidljiva (štedi bateriju)
        document.addEventListener('visibilitychange', () => {
            document.hidden ? clearInterval(timer) : restart();
        });

        show(0);
        restart();
    })();

    /* ---------- Pojavljivanje pri skrolovanju ---------- */
    const io = ('IntersectionObserver' in window)
        ? new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('vidljivo');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 })
        : null;

    function prati(el, i) {
        if (!io) { el.classList.add('vidljivo'); return; }
        el.style.transitionDelay = (i % 3) * 70 + 'ms';
        io.observe(el);
    }

    document.querySelectorAll('.reveal').forEach(prati);

    /* ======================================================================
       DINAMIČNE VESTI
       Izvor: vesti/vesti.js (window.VESTI) + opciono WordPress blog.
       ====================================================================== */

    const IK = {
        kalendar: '<svg class="ik" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/></svg>',
        desno: '<svg class="ik" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
        dole: '<svg class="ik" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
        spoljni: '<svg class="ik" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>'
    };

    const MESECI = ['јануар', 'фебруар', 'март', 'април', 'мај', 'јун', 'јул', 'август', 'септембар', 'октобар', 'новембар', 'децембар'];
    const MESECI_GEN = ['јануара', 'фебруара', 'марта', 'априла', 'маја', 'јуна', 'јула', 'августа', 'септембра', 'октобра', 'новембра', 'децембра'];

    function esc(t) {
        return String(t == null ? '' : t)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function formatDatum(d) {
        const m = /^(\d{4})-(\d{2})(?:-(\d{2}))?/.exec(d || '');
        if (!m) return esc(d);
        const god = m[1], mes = Number(m[2]) - 1;
        if (!m[3]) return MESECI[mes] + ' ' + god + '.';
        return Number(m[3]) + '. ' + MESECI_GEN[mes] + ' ' + god + '.';
    }

    function putanja(href) {
        if (!href) return '';
        if (/^(https?:|mailto:|tel:|#|\/)/.test(href)) return href;
        return KOREN + href;
    }

    function spoljni(href) {
        return /^https?:/.test(href || '');
    }

    function bezHtml(html) {
        const d = document.createElement('div');
        d.innerHTML = html || '';
        return (d.textContent || '').replace(/\s+\n/g, '\n').trim();
    }

    function iskratko(t, n) {
        t = (t || '').replace(/\s+/g, ' ').trim();
        return t.length > n ? t.slice(0, n).replace(/\s\S*$/, '') + '…' : t;
    }

    async function ucitajWordPress(sajt) {
        if (!sajt || !window.fetch) return [];
        try {
            const url = 'https://public-api.wordpress.com/rest/v1.1/sites/' + encodeURIComponent(sajt) +
                '/posts/?number=12&fields=title,date,URL,excerpt,content,categories';
            const odg = await fetch(url);
            if (!odg.ok) return [];
            const podaci = await odg.json();
            return (podaci.posts || []).map(p => {
                const kat = p.categories ? Object.keys(p.categories)[0] : '';
                const tekst = bezHtml(p.content);
                return {
                    datum: (p.date || '').slice(0, 10),
                    kategorija: kat && kat !== 'Uncategorized' ? kat : 'Вести',
                    naslov: bezHtml(p.title),
                    kratko: iskratko(bezHtml(p.excerpt) || tekst, 180),
                    tekst: iskratko(tekst, 1200),
                    link: p.URL
                };
            });
        } catch (e) {
            return [];
        }
    }

    async function sveVesti() {
        const lokalne = Array.isArray(window.VESTI) ? window.VESTI.slice() : [];
        const wp = await ucitajWordPress(window.VESTI_WORDPRESS);
        return lokalne.concat(wp)
            .filter(v => v && v.naslov)
            .sort((a, b) => String(b.datum || '').localeCompare(String(a.datum || '')));
    }

    function linkHtml(v, tekst, klasa) {
        if (!v.link) return '';
        const href = putanja(v.link);
        const dod = spoljni(v.link) ? ' target="_blank" rel="noopener"' : '';
        const ik = spoljni(v.link) ? IK.spoljni : IK.desno;
        return '<a class="' + klasa + '" href="' + esc(href) + '"' + dod + '>' + tekst + ik + '</a>';
    }

    function slikaHtml(v, klasa) {
        if (!v.slika) return '';
        return '<img class="' + klasa + '" src="' + esc(putanja(v.slika)) + '" alt="" loading="lazy" decoding="async">';
    }

    /* --- početna: najnovije vesti kao kartice --- */
    function karticaPocetna(v, i) {
        const el = document.createElement('article');
        el.className = 'news-article';
        const link = v.link ? putanja(v.link) : KOREN + 'vesti/novosti.html';
        const dod = spoljni(v.link) ? ' target="_blank" rel="noopener"' : '';
        el.innerHTML =
            slikaHtml(v, 'news-slika') +
            '<div class="news-meta">' +
                '<span class="kategorija">' + esc(v.kategorija || 'Вести') + '</span>' +
                '<span class="datum">' + IK.kalendar + formatDatum(v.datum) + '</span>' +
            '</div>' +
            '<h3>' + esc(v.naslov) + '</h3>' +
            '<p>' + esc(v.kratko) + '</p>' +
            '<a href="' + esc(link) + '"' + dod + ' class="link-strelica">Прочитај више' + IK.desno + '</a>';
        return el;
    }

    /* --- strana Новости: lista sa filterom i "Прикажи још" --- */
    function stavkaListe(v) {
        const el = document.createElement('article');
        el.className = 'news-item';
        const pasusi = String(v.tekst || v.kratko || '').split(/\n+/).filter(Boolean)
            .map(p => '<p>' + esc(p) + '</p>').join('');
        el.innerHTML =
            '<span class="datum">' + IK.kalendar + formatDatum(v.datum) + ' · ' + esc(v.kategorija || 'Вести') + '</span>' +
            '<h3>' + esc(v.naslov) + '</h3>' +
            '<p class="kratko">' + esc(v.kratko) + '</p>' +
            '<span class="vise">Прочитај више' + IK.dole + '</span>' +
            '<div class="detaljno">' + slikaHtml(v, 'news-slika') + pasusi +
                linkHtml(v, 'Опширније', 'link-strelica') + '</div>';
        el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'button');
        el.setAttribute('aria-expanded', 'false');
        return el;
    }

    function vezeZaOtvaranje(box) {
        box.addEventListener('click', (e) => {
            if (e.target.closest('a')) return;
            const item = e.target.closest('.news-item');
            if (!item) return;
            const bio = item.classList.contains('selected');
            box.querySelectorAll('.news-item').forEach(n => {
                n.classList.remove('selected');
                n.setAttribute('aria-expanded', 'false');
            });
            if (!bio) {
                item.classList.add('selected');
                item.setAttribute('aria-expanded', 'true');
            }
        });
        box.addEventListener('keydown', (e) => {
            const item = e.target.closest('.news-item');
            if (item && e.target === item && (e.key === 'Enter' || e.key === ' ')) {
                e.preventDefault();
                item.click();
            }
        });
    }

    (async function () {
        const pocetna = document.querySelector('[data-vesti-pocetna]');
        const lista = document.querySelector('[data-vesti-lista]');
        if (!pocetna && !lista) return;

        const vesti = await sveVesti();

        if (pocetna) {
            const broj = Number(pocetna.dataset.vestiPocetna) || 3;
            if (vesti.length) {
                pocetna.innerHTML = '';
                vesti.slice(0, broj).forEach((v, i) => {
                    pocetna.appendChild(karticaPocetna(v, i));
                });
            }
        }

        if (lista) {
            const filteriBox = document.querySelector('[data-vesti-filteri]');
            const vise = document.querySelector('[data-vesti-vise]');
            const POSTRANI = 6;
            let filter = 'Све';
            let prikazano = POSTRANI;

            if (!vesti.length) {
                lista.innerHTML = '<p class="prazno">Тренутно нема објављених вести.</p>';
                if (vise) vise.hidden = true;
                return;
            }

            function crtaj() {
                const izbor = vesti.filter(v => filter === 'Све' || (v.kategorija || 'Вести') === filter);
                lista.innerHTML = '';
                izbor.slice(0, prikazano).forEach(v => lista.appendChild(stavkaListe(v)));
                if (vise) vise.hidden = izbor.length <= prikazano;
            }

            if (filteriBox) {
                const kategorije = ['Све'].concat([...new Set(vesti.map(v => v.kategorija || 'Вести'))]);
                if (kategorije.length > 2) {
                    filteriBox.innerHTML = kategorije.map(k =>
                        '<button type="button" class="filter' + (k === filter ? ' aktivan' : '') + '" aria-pressed="' + (k === filter) + '">' + esc(k) + '</button>'
                    ).join('');
                    filteriBox.addEventListener('click', (e) => {
                        const b = e.target.closest('.filter');
                        if (!b) return;
                        filter = b.textContent;
                        prikazano = POSTRANI;
                        filteriBox.querySelectorAll('.filter').forEach(x => {
                            x.classList.toggle('aktivan', x === b);
                            x.setAttribute('aria-pressed', String(x === b));
                        });
                        crtaj();
                    });
                }
            }

            if (vise) {
                vise.addEventListener('click', () => {
                    prikazano += POSTRANI;
                    crtaj();
                });
            }

            vezeZaOtvaranje(lista);
            crtaj();
        }
    })();
})();
