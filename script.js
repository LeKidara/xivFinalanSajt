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
        const proveri = () => {
            navbar.classList.toggle('skrolovano', window.scrollY > 10);
            const max = document.documentElement.scrollHeight - window.innerHeight;
            navbar.style.setProperty('--napredak', max > 0 ? Math.min(1, window.scrollY / max).toFixed(3) : 0);
        };
        window.addEventListener('scroll', proveri, { passive: true });
        proveri();
    }

    /* ---------- Dugme „назад на врх“ ---------- */
    (function () {
        const dugme = document.getElementById('na-vrh');
        if (!dugme) return;
        const proveri = () => {
            const treba = window.scrollY > window.innerHeight * 0.9;
            dugme.hidden = !treba;
            requestAnimationFrame(() => dugme.classList.toggle('vidljivo', treba));
        };
        window.addEventListener('scroll', proveri, { passive: true });
        dugme.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
            const prvi = document.querySelector('.navbar-brand');
            if (prvi) prvi.focus({ preventScroll: true });
        });
        proveri();
    })();

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

    const smanjenoKretanje = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ---------- Polaroid fotografije na početnoj ---------- */
    (function () {
        const box = document.getElementById('polaroidi');
        if (!box) return;
        const slike = Array.from(box.querySelectorAll('.polaroid'));
        if (slike.length < 2) return;
        let timer = null;
        let radi = false;

        function sledeca() {
            if (radi) return;
            radi = true;
            const prva = slike.find(el => el.dataset.poz === '0');
            prva.classList.add('odlazi');
            setTimeout(() => {
                slike.forEach(el => {
                    const p = Number(el.dataset.poz);
                    el.dataset.poz = String((p - 1 + slike.length) % slike.length);
                });
                prva.classList.remove('odlazi');
                radi = false;
            }, smanjenoKretanje ? 0 : 880);
        }

        function kreni() {
            clearInterval(timer);
            if (!smanjenoKretanje) timer = setInterval(sledeca, 4500);
        }

        box.addEventListener('click', () => { sledeca(); kreni(); });

        // prevlačenje prstom / mišem
        let pocetakX = null;
        box.addEventListener('pointerdown', (e) => { pocetakX = e.clientX; });
        box.addEventListener('pointerup', (e) => {
            if (pocetakX !== null && Math.abs(e.clientX - pocetakX) > 40) { sledeca(); kreni(); }
            pocetakX = null;
        });
        box.addEventListener('pointercancel', () => { pocetakX = null; });

        // tastatura
        box.setAttribute('tabindex', '0');
        box.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowRight') { e.preventDefault(); sledeca(); kreni(); }
        });
        box.addEventListener('mouseenter', () => clearInterval(timer));
        box.addEventListener('mouseleave', kreni);
        document.addEventListener('visibilitychange', () => { document.hidden ? clearInterval(timer) : kreni(); });
        kreni();
    })();

    /* ---------- Crteži: dužina linije za animaciju iscrtavanja ---------- */
    document.querySelectorAll('.crtez path').forEach(p => {
        try { p.style.setProperty('--duzina', Math.ceil(p.getTotalLength())); } catch (e) { /* stari pregledači */ }
    });

    /* ---------- 3D naginjanje kartica pod mišem ---------- */
    if (!smanjenoKretanje && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
        document.querySelectorAll('.brzi-link').forEach(el => {
            el.addEventListener('pointermove', (e) => {
                const r = el.getBoundingClientRect();
                const x = (e.clientX - r.left) / r.width - 0.5;
                const y = (e.clientY - r.top) / r.height - 0.5;
                el.style.transform = 'perspective(700px) rotateX(' + (-y * 10) + 'deg) rotateY(' + (x * 12) + 'deg) translate(-3px, -3px)';
            });
            el.addEventListener('pointerleave', () => { el.style.transform = ''; });
        });
    }

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

    function prati(el) {
        if (!io) { el.classList.add('vidljivo'); return; }
        io.observe(el);
    }

    document.querySelectorAll('.reveal').forEach(prati);

    /* ---------- Brojači (npr. 32 одељења, 1000+ ученика) ---------- */
    (function () {
        const brojevi = document.querySelectorAll('[data-broj]');
        if (!brojevi.length) return;
        const format = n => n >= 1000 ? n.toLocaleString('sr-RS').replace(/\s/g, '.') : String(n);

        function broji(el) {
            const cilj = Number(el.dataset.broj);
            const sufiks = el.dataset.sufiks || '';
            if (smanjenoKretanje) { el.textContent = format(cilj) + sufiks; return; }
            const trajanje = 1600;
            const start = performance.now();
            (function korak(t) {
                const p = Math.min(1, (t - start) / trajanje);
                const e = 1 - Math.pow(1 - p, 4);
                el.textContent = format(Math.round(cilj * e)) + sufiks;
                if (p < 1) requestAnimationFrame(korak);
            })(start);
        }

        if (!('IntersectionObserver' in window)) return;
        const o = new IntersectionObserver((unosi) => {
            unosi.forEach(u => {
                if (u.isIntersecting) { broji(u.target); o.unobserve(u.target); }
            });
        }, { threshold: 0.3 });
        // brojimo samo one koji su ispod ekrana; ostali odmah pokazuju pravu vrednost
        brojevi.forEach(el => {
            if (el.getBoundingClientRect().top > window.innerHeight) {
                el.textContent = '0' + (el.dataset.sufiks || '');
                o.observe(el);
            }
        });
        window.addEventListener('beforeprint', () => brojevi.forEach(el => {
            el.textContent = format(Number(el.dataset.broj)) + (el.dataset.sufiks || '');
        }));
    })();

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
    const MESECI_KRATKO = ['јан', 'феб', 'мар', 'апр', 'мај', 'јун', 'јул', 'авг', 'сеп', 'окт', 'нов', 'дец'];
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

    function datumList(d) {
        const m = /^(\d{4})-(\d{2})(?:-(\d{2}))?/.exec(d || '');
        if (!m) return '<div class="datum-list"><b>–</b></div>';
        const mes = MESECI_KRATKO[Number(m[2]) - 1];
        const opis = ' aria-label="' + esc(formatDatum(d)) + '"';
        return m[3]
            ? '<div class="datum-list"' + opis + '><b>' + Number(m[3]) + '</b><span>' + mes + '</span><small>' + m[1] + '</small></div>'
            : '<div class="datum-list"' + opis + '><b>' + mes + '</b><small>' + m[1] + '</small></div>';
    }

    /* --- početna: najnovije vesti kao kartice --- */
    function karticaPocetna(v, i) {
        const el = document.createElement('article');
        el.className = 'news-article reveal vidljivo';
        const link = v.link ? putanja(v.link) : KOREN + 'vesti/novosti.html';
        const dod = spoljni(v.link) ? ' target="_blank" rel="noopener"' : '';
        el.innerHTML =
            '<div class="news-vrh">' + datumList(v.datum) +
                '<span class="kategorija">' + esc(v.kategorija || 'Вести') + '</span>' +
            '</div>' +
            slikaHtml(v, 'news-slika') +
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
