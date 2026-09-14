# IașiAsigură

Site static pentru **Marina Metzak**, asistent în brokeraj (persoană fizică independentă), care activează în numele și pe seama **DESTINE BROKER DE ASIGURARE-REASIGURARE SRL** (RBK-425). Site-ul informează despre asigurări (RCA, CASCO, locuință, PAD, călătorie, sănătate, viață, malpraxis, ROTR, CMR, agricole, IMM etc.), redirecționează spre platforma brokerului (`metzak-marina.smartsales.ro`) pentru produsele „online" și spre WhatsApp pentru cele „consultanță". **Nu afișează prețuri, nu are formulare pe site și nu colectează date personale.**

Generat static de `build.py` (Python 3) din fișierele JSON/Markdown din `content/`. Output-ul HTML se comite în repo; GitHub Pages servește direct din `main` / root.

## Date fixe

| Câmp | Valoare |
|---|---|
| Domeniu | `iasiasigura.com` (liber, cumpărat de Alexandru). `iasiasigura.ro` e al altcuiva (2018, parcat) — nu-l folosim. |
| Brand | **IașiAsigură** · tagline **„Ia și asigură!"** (joc de cuvinte: „Ia și asigură" / „Iași asigură") |
| Persoană | Marina Metzak, asistent în brokeraj, persoană fizică independentă (PFI) |
| Cod RAF | 160354 |
| Broker principal | DESTINE BROKER DE ASIGURARE-REASIGURARE SRL, Ploiești, Str. Torcători nr. 4, CUI 21678074, RBK-425/20.08.2007 |
| Telefon / WhatsApp | +40 752 205 206 (`wa.me/40752205206`) |
| E-mail | `marina-mihaela.metzak@destine-broker.ro` (adresa de la broker; domeniul nu are e-mail) |
| Adresă | Bd. Metalurgiei nr. 4, Iași — întâlniri **doar cu programare** |
| Facebook | https://www.facebook.com/marina.metzak |
| Acoperire | Online în toată România; prezență fizică Iași și regiunea Moldova |
| Limbă | Română, exclusiv |

## Structura repo

```
build.py                   # generatorul: citește content/, scrie HTML-ul static
templates.py                # head(), header(), footer(), cta_block(), faq_block(), ldjson()
content/
  site.json                 # date fixe (tabelul de mai sus), navigație, footer, URL smartsales
  products.json              # 16 produse: slug, nume, tip, path, grup, texte, faq, articole conexe
  zones.json                 # 9 orașe: slug, nume, județ, texte locale, faq, produse relevante
  home.json                  # secțiuni homepage (argumente, pași, faq, testimoniale)
  blog/*.md                  # articole, cu frontmatter JSON între `---`
  pages/*.html + meta.json   # fragmente de conținut (despre, contact, termeni, confidențialitate, cookies)
css/styles.css
js/script.js
assets/                      # logo.svg, favicon.svg, og-*.svg/png, marina.webp (placeholder TODO-MARINA)
index.html, despre.html, contact.html, ...      # GENERATE — nu se editează manual
asigurari/*.html, zone/*.html, blog/*.html       # GENERATE
robots.txt, sitemap.xml, llms.txt, site.webmanifest, 404.html, CNAME   # GENERATE
scripts/
  check_site.py              # verifică output-ul generat (h1 unic, title/description, canonical, JSON-LD, linkuri, prețuri, TODO-MARINA cu --release)
  render_assets.sh            # randează PNG/WebP din SVG-urile din assets/
tests/                        # pytest: test_build.py, test_templates.py
docs/research.md, docs/superpowers/specs/, docs/superpowers/plans/
README.md
```

Reguli: `build.py` e idempotent (rulat de două ori → același output). Fișierele generate au comentariu `<!-- generat de build.py — editează content/ -->`. **Nicio pagină generată nu se editează manual** — orice modificare de conținut se face în `content/` sau în `templates.py`, apoi se rulează din nou `build.py`.

## Setup

```bash
pip3 install -r requirements.txt
```

Dependențe: `markdown` (pentru articolele de blog scrise în Markdown) și `pytest` (pentru teste). Restul e din stdlib Python 3.

## Build și verificare

```bash
python3 build.py                       # generează tot output-ul static din content/
python3 scripts/check_site.py          # verifică output-ul (fără acces la internet)
python3 scripts/check_site.py --online # + verifică că URL-urile smartsales răspund HTTP 200
python3 scripts/check_site.py --release # + FAIL dacă vreo pagină generată conține "TODO-MARINA"
python3 -m pytest -q                    # teste (build, template, check_site); `pytest -q` merge la fel, via pyproject.toml
```

`check_site.py` verifică: exact un `<h1>` pe pagină, `<title>` unic ≤ 60 caractere, `description` unică ≤ 155 caractere, `canonical` corect, JSON-LD valid, niciun link către `destine.smartsales.ro` sau `/presale/`, toate URL-urile `metzak-marina.smartsales.ro` au `utm_source=iasiasigura`, linkurile interne rezolvă la fișiere existente, și că nicio pagină nu „pare să conțină un preț" (regex pe „de la/doar/numai N lei/eur").

### Gate de release

Flag-ul `--release` face `check_site.py` să pice (`PROBLEMĂ`, exit 1) dacă găsește șirul `TODO-MARINA` în orice `.html` generat. Rulările normale (fără `--release`) trec în continuare cât timp există placeholdere — asta e intenționat, ca să nu blocheze dezvoltarea zilnică.

**Înainte de orice deploy, rulează:**

```bash
python3 build.py && python3 scripts/check_site.py --release
```

Dacă exit code e diferit de 0, mai sunt placeholdere de completat. La data acestui README, `--release` pică din cauza:

- **Poza Marinei**: `assets/marina.webp` este un placeholder generat din SVG (`scripts/render_assets.sh`), nu poza reală.
- **`person.bio_short`** din `content/site.json` — 2 propoziții despre experiență (de câți ani în asigurări, ce produse preferă).
- **Testimoniale** din `content/home.json` — 3 testimoniale placeholder, afișate pe homepage și pe `despre.html`.
- **Program** în `content/pages/contact.html` — orele de lucru afișate pe pagina de contact.
- (bonus, în `content/pages/despre.html`): anul de când Marina lucrează în asigurări.

## Cum adaugi un articol de blog

1. Creezi `content/blog/<slug>.md` cu frontmatter JSON între `---`:

```
---
{"title": "Titlu articol",
 "desc": "Descriere ≤ 155 caractere, pentru meta description.",
 "date": "2026-09-14", "updated": "2026-09-14", "category": "Auto",
 "related_products": ["rca", "casco"],
 "faq": [["Întrebare?", "Răspuns."], ...]}
---
corpul articolului, în Markdown
```

Câmpuri obligatorii: `title`, `desc` (≤ 155 caractere), `date`, `updated`, `category`, `related_products` (slug-uri din `content/products.json`), `faq` (listă de perechi întrebare/răspuns).

2. Reguli pentru corpul articolului:
   - Primul paragraf începe cu **„Pe scurt:”** — un rezumat de 2-3 fraze.
   - Fiecare secțiune e un `## ` (H2), formulat ca **întrebare**.
   - **Niciun `# ` (H1)** în corp — H1-ul paginii vine din template.
   - Ultimul H2 este **„Ce faci mai departe”**.
   - Minim ~900 de cuvinte (verificat de teste).
3. Rulezi `python3 build.py`, verifici cu `python3 scripts/check_site.py`, apoi `git add` + commit.

## Cum adaugi/modifici un produs

Fiecare produs e un obiect în `content/products.json`, cu (printre altele) câmpurile:

- `slug`, `name`, `type` (`"online"` = buton „Cumpără online” către smartsales; `"consultanta"` = buton „Cere ofertă pe WhatsApp”), `path` (path-ul produsului pe `metzak-marina.smartsales.ro`), `group` (`["pf"]`, `["pj"]` sau ambele), `icon`, `short`, `wa_text`, `service_type`.
- SEO: `title` (≤ 60 caractere), `desc` (≤ 155 caractere), `h1`, `answer`.
- Conținut: `covers`, `not_covers` (opțional — dacă lipsește sau e gol, coloana „Ce nu acoperă” nu se randează), `docs`, `steps`, `faq` (perechi întrebare/răspuns), `articles` (slug-uri de articole din blog care menționează produsul).

**`articles` se mapează manual, invers**: când scrii un articol nou cu `related_products`, adaugă și tu manual slug-ul articolului în `articles` al produsului corespunzător din `products.json` — nu se generează automat.

După orice modificare: `python3 build.py && python3 scripts/check_site.py`.

## Cum adaugi o zonă (oraș)

Fiecare zonă e un obiect în `content/zones.json`: `slug`, `name`, `county`, `geo_region` (cod ISO, ex. `RO-IS`), `title`, `desc`, `h1`, `answer`, `local` (3 paragrafe specifice zonei — nu copiate din alte zone, testele verifică suprapunere textuală < 75% între zone), `products` (slug-uri din `products.json` relevante pentru zonă), `faq` (exact 4 perechi întrebare/răspuns).

Atenție la afirmații absolute despre obligativități legale (ex. ROTR, licențe de transport) — formulează-le ca „una dintre modalitățile acceptate”, nu ca regulă universală, pentru că depinde de tipul de vehicul/activitate.

## Cum actualizezi un articol

Schimbi câmpul `updated` din frontmatter **doar după o revizuire reală a conținutului** (verificare de prețuri, legislație, linkuri), nu doar pentru a „împrospăta” data. Data afișată pe pagină ca „Actualizat: <lună an>” vine din acest câmp.

## Cum înlocuiești poza

1. Pregătești poza Marinei: **600×600 px, sub 80 KB**, format WebP.
2. O salvezi ca `assets/marina.webp`, cu exact acest nume (înlocuiește placeholderul).
3. Regenerezi restul asset-urilor (og-image-uri, logo PNG, favicon) cu:

```bash
scripts/render_assets.sh
```

Scriptul randează SVG-urile sursă din `assets/` în PNG/WebP, folosind (în ordine de încercare) `rsvg-convert`, `qlmanage` (macOS) sau `magick` pentru SVG→PNG, și `cwebp` sau Pillow (`python3 -c "import PIL"`) pentru PNG→WebP.

## Publicare

1. `python3 build.py && python3 scripts/check_site.py --release` — trebuie să dea exit 0 (fără placeholdere TODO-MARINA rămase).
2. Commit-ezi output-ul generat împreună cu sursele din `content/` modificate.
3. Push pe `main` → GitHub Pages republică automat site-ul din root.
4. Verifici manual: `https://iasiasigura.com` cu HTTPS valid, `www` redirecționează la apex, sitemap trimis în Search Console, `contact@` primește un e-mail de test.

Gate-ul `--release` e menit exact pentru pasul 1: nu publici cu placeholdere vizibile pe site.

## Domeniu și DNS

DNS pe **Cloudflare** (gratuit):

- `A` → IP-urile GitHub Pages: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
- `AAAA` → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.
- `www` — CNAME → `alexandrumetzak.github.io`.
- **E-mail**: nu există e-mail pe domeniu; site-ul folosește adresa de la Destine Broker. DNS-ul e la GoDaddy, direct pe IP-urile GitHub (fără Cloudflare).
- HTTPS forțat din setările GitHub Pages (apex + `www`); `www` redirecționează automat la apex, pentru că apexul e domeniul din `CNAME`.
- **Analytics**: Cloudflare Web Analytics (fără cookie-uri, fără identificatori persistenți, deci fără banner de consimțământ). Snippet-ul se adaugă **manual în `templates.footer()`**, imediat înainte de `<script src="{R}js/script.js" defer></script>`, sub forma `<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "…"}'></script>` — **nu** prin proxy-ul Cloudflare (site-ul e servit de GitHub Pages, nu prin orange-cloud). Fără Google Analytics la lansare. **Când adaugi snippet-ul, ține textul legal sincronizat**: `content/pages/cookies.html` și `content/pages/confidentialitate.html` spun că singura resursă terță încărcată de site este beacon-ul de pe `static.cloudflareinsights.com`, fără cookie-uri și fără identificatori persistenți; dacă apare orice altă resursă externă, actualizează ambele pagini.

## Ce NU facem

- **Nu afișăm prețuri** pe site (nici „de la”, nici valori fixe) — `check_site.py` are un regex care detectează asta.
- **Nu punem formulare** pe site — lead-urile merg pe WhatsApp sau pe platforma smartsales.
- **Nu punem bannere/cookie-uri de tracking** — Cloudflare Web Analytics nu folosește cookie-uri.
- **Nu folosim logo-ul Destine Broker** fără acord scris explicit de la broker.
- **Nu edităm manual fișierele HTML generate** — orice schimbare trece prin `content/` sau `templates.py` și `python3 build.py`.

## Lighthouse (mobil)

Verificat local (`python3 -m http.server` + `npx lighthouse ... --chrome-flags="--headless=new"`, mod mobil implicit) pe homepage, o pagină produs (`/asigurari/rca.html`) și un articol (`/blog/pret-rca-2026-cum-se-calculeaza.html`): toate categoriile (Performance, Accessibility, Best Practices, SEO) la **100/100/100/100** după corecturile de contrast de culoare și de link-uri descrise în `.superpowers/sdd/2026-09-14-iasiasigura-site/task-9-report.md`.
