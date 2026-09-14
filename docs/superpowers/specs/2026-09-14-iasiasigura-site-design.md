# IașiAsigură — site static SEO/AEO pentru Marina Metzak (asistent în brokeraj)

Data: 2026-09-14. Status: aprobat de Alexandru (brainstorming). Research de bază: `docs/research.md`.

## 1. Scop

Un site static, rapid, optimizat SEO + AEO/AIO, care prezintă persoana (Marina Metzak) și produsele de asigurare, și trimite clienții să cumpere online pe platforma brokerului (`metzak-marina.smartsales.ro`) sau să ceară ofertă pe WhatsApp. Site-ul nu vinde, nu calculează prețuri, nu stochează date personale.

Succes = trafic organic din Google + citări în răspunsurile AI (Google AI Overviews, ChatGPT, Perplexity, Claude) pentru căutări de asigurări din Iași/Moldova și pentru nișe naționale, convertit în conversații WhatsApp și în comenzi pe smartsales atribuite Marinei.

## 2. Date fixe

| Câmp | Valoare |
|---|---|
| Domeniu | `iasiasigura.com` (liber, cumpărat de Alexandru). `iasiasigura.ro` e al altcuiva (2018, parcat) — nu-l folosim. |
| Brand | **IașiAsigură** · tagline **„Ia și asigură!"** (joc de cuvinte: „Ia și asigură" / „Iași asigură") |
| Persoană | Marina Metzak, asistent în brokeraj, persoană fizică independentă (PFI) |
| Cod RAF | 160354 |
| Broker principal | DESTINE BROKER DE ASIGURARE-REASIGURARE SRL, Ploiești, Str. Torcători nr. 4, CUI 21678074, RBK-425/20.08.2007 |
| Telefon / WhatsApp | +40 752 205 206 (`wa.me/40752205206`) |
| E-mail | `contact@iasiasigura.com` (redirecționat spre Gmail-ul Marinei prin Cloudflare Email Routing) |
| Adresă | Bd. Metalurgiei nr. 4, Iași — întâlniri **doar cu programare** |
| Facebook | https://www.facebook.com/marina.metzak |
| Acoperire | Online în toată România; prezență fizică Iași și regiunea Moldova |
| Limbă | Română, exclusiv |

Materiale care vin ulterior de la Marina (placeholder-e vizibile în cod până atunci, marcate `TODO-MARINA`): poză profesională, biografie (ani de experiență, de când în asigurări), 3–5 testimoniale, confirmare că e-mailul funcționează.

## 3. Stack și infrastructură

- **HTML/CSS/JS static, generat de `build.py` (Python 3)**, același pattern ca DDD (`ddd-husi.ro`) și Contagex (`contagex.ro`). Output-ul generat se comite în repo; GitHub Pages servește din root.
- Dependență Python unică: `markdown` (pentru articolele de blog scrise în Markdown). Instalare: `pip3 install markdown`. Restul stdlib.
- Repo: `~/Work/marina-destine` → GitHub `alexandrumetzak/iasiasigura`, branch `main`, GitHub Pages din `main` / root. `CNAME` = `iasiasigura.com`.
- DNS pe **Cloudflare** (gratuit): `A` → IP-urile GitHub Pages (185.199.108–111.153), `AAAA` corespunzătoare, `www` CNAME → `alexandrumetzak.github.io`, **Email Routing** `contact@` → Gmail Marina. HTTPS forțat din setările GitHub Pages. `www` redirecționează la apex (GitHub o face automat când apex e domeniul din CNAME).
- Analytics: **Cloudflare Web Analytics** (fără cookie-uri, fără banner) + Google Search Console (verificare prin DNS TXT). Fără GA4 la lansare.
- Fără backend, fără formulare pe site. Lead-urile vin prin WhatsApp și prin fluxul smartsales.

## 4. Structura site-ului (URL-uri)

Toate paginile sunt `.html` la nivel de fișier (compatibil GitHub Pages), linkuri interne relative (prefix `R` ca în Contagex), canonical absolut.

| URL | Conținut |
|---|---|
| `/` | Homepage |
| `/asigurari/index.html` | Catalog: toate produsele, grupate PF / PJ |
| `/asigurari/<slug>.html` | 16 pagini produs (lista în §5) |
| `/zone/<slug>.html` | 9 pagini geo: `iasi`, `pascani`, `bacau`, `vaslui`, `botosani`, `suceava`, `piatra-neamt`, `roman`, `galati` |
| `/blog/index.html` | Lista articolelor, cele mai noi primele |
| `/blog/<slug>.html` | Articole (12 la lansare, §7) |
| `/despre.html` | Marina: cine e, cum lucrează, cod RAF, broker, poză, testimoniale |
| `/contact.html` | WhatsApp, telefon, e-mail, adresă cu programare, program |
| `/termeni.html`, `/confidentialitate.html`, `/cookies.html` | Legal |
| `/404.html` | Eroare, cu linkuri spre produse principale |
| `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/site.webmanifest` | Tehnic |

## 5. Produse

Două tipuri, definite în `content/products.json`:

- **`online`** — există flux self-service pe smartsales. CTA primar: „Cumpără online" → `https://metzak-marina.smartsales.ro/<path>?utm_source=iasiasigura&utm_medium=site&utm_campaign=<slug>`. CTA secundar: WhatsApp.
- **`consultanta`** — nu există flux online. CTA primar: WhatsApp cu mesaj pre-completat. CTA secundar: „Cere ofertă pe platformă" → `https://metzak-marina.smartsales.ro/home/asigurari?utm_source=iasiasigura&utm_medium=site&utm_campaign=<slug>#asigurariPj` (sau `#asigurariPf` pentru viață/pensii/CASCO PF).

Toate linkurile smartsales folosesc **exclusiv** subdomeniul `metzak-marina.smartsales.ro` (atribuirea comisionului vine din subdomeniu). Niciodată `destine.smartsales.ro`, niciodată URL-uri `/presale/create/<token>`. Verificat: smartsales tolerează query-string UTM pe `/rca` și `/home/asigurari`.

| Slug | Nume | Tip | Path smartsales | Grup |
|---|---|---|---|---|
| `rca` | Asigurare RCA | online | `/rca` | PF + PJ |
| `casco` | Asigurare CASCO | consultanta | `/home/asigurari#auto` | PF + PJ |
| `locuinta` | Asigurare locuință facultativă | online | `/locuinta` | PF |
| `pad` | Asigurare PAD (obligatorie) | online | `/pad` | PF |
| `calatorie` | Asigurare medicală de călătorie | online | `/travel` | PF |
| `storno` | Asigurare storno | online | `/travel` | PF |
| `sanatate` | Asigurare de sănătate | online | `/sanatate` | PF |
| `viata` | Asigurare de viață | consultanta | `/home/asigurari#sanatate` | PF |
| `pensii-private` | Pensie privată Pilon III | consultanta | `/home/asigurari#sanatate` | PF |
| `malpraxis` | Malpraxis (răspundere profesională medicală) | online | `/malpraxis` | PF |
| `raspundere-civila` | Răspundere civilă profesională și personală | consultanta | `/home/asigurari#asigurariPj` | PF + PJ |
| `taxi-uber-bolt` | Accidente taxi / Uber / Bolt (SIGNAL) | online | `/accidente` | PF + PJ |
| `rotr` | Asigurare ROTR | online | `/rotr` | PJ |
| `cargo-cmr` | CARGO și CMR (transport marfă) | consultanta | `/home/asigurari#asigurariPj` | PJ |
| `imm` | Asigurări pentru IMM (bunuri, răspundere, angajați) | consultanta | `/home/asigurari#asigurariPj` | PJ |
| `agricole` | Asigurări agricole (culturi, animale, utilaje) | consultanta | `/home/asigurari#asigurariPj` | PJ |

Asistența la domiciliu (`/asistentaladomiciliu`) și asistența rutieră (`/asistentarutiera`) apar ca linkuri secundare pe paginile `locuinta`, respectiv `rca`/`casco`, nu ca pagini proprii.

**Șablonul unei pagini produs** (aceeași ordine pe toate):
1. Breadcrumb · H1 · **răspuns direct de 40–60 cuvinte** (ce e, pentru cine, cum se cumpără) · cele două CTA-uri.
2. „Ce acoperă" / „Ce nu acoperă" (liste).
3. „Acte necesare" (listă scurtă).
4. „Cum cumperi în 3 pași" (online: pe smartsales; consultanță: WhatsApp → ofertă → poliță pe e-mail).
5. FAQ 6–8 întrebări, H3 sub formă de întrebare, răspunsuri autonome (cu `FAQPage` schema).
6. Produse conexe (3) + articole din blog relevante (2–3) + zone.
7. Bloc „Marina Metzak, asistent în brokeraj" cu poză mică și WhatsApp.

Fără prețuri, tarife sau „de la X lei" nicăieri pe site. Fără afirmații comparative despre asigurători.

## 6. Pagini geo

Scop: căutări „asigurari <oraș>", „rca <oraș>", „broker asigurari <oraș>". Conținut real, distinct per oraș (minim 500 de cuvinte unice), nu șablon cu orașul înlocuit:
- Intro: cum lucrează Marina cu clienții din <oraș> (online + WhatsApp; întâlnire la Iași cu programare).
- 2–3 particularități locale scrise manual (ex. Iași: trafic, parcări, UMF/rezidenți → malpraxis, Bolt/Uber; Bacău/Suceava: transportatori → ROTR/CMR; Botoșani/Vaslui: agricol; Galați: port/industrie).
- Produsele relevante pentru oraș (linkuri).
- FAQ local 4 întrebări.
- Schema: `Service` cu `areaServed: City`, `BreadcrumbList`, `FAQPage`. **Nu** `LocalBusiness` pe geo (există o singură entitate `InsuranceAgency` cu adresa din Iași, referențiată prin `@id`).

## 7. Blog / research (AEO)

Articole în `content/blog/<slug>.md` cu frontmatter (title, description, date, updated, category, related_products, faq). Generatorul produce `/blog/<slug>.html` și `/blog/index.html`. 12 articole la lansare:

1. `pret-rca-2026-cum-se-calculeaza` — factorii care influențează prima RCA
2. `bonus-malus-explicat` — clasele B0–B8 / M1–M8, cum se transferă
3. `rca-sau-casco-diferente` — ce acoperă fiecare, când ai nevoie de ambele
4. `pad-asigurare-obligatorie-locuinta` — ce e PAD, ce acoperă, amendă
5. `asigurare-locuinta-ce-acopera` — facultativă vs PAD, riscuri, sume
6. `asigurare-calatorie-grecia-turcia` — ce acoperire, EHIC vs privată
7. `malpraxis-asistent-medical-rezident` — cine e obligat, limite, cât durează
8. `asigurare-bolt-uber-iasi` — ce e obligatoriu pentru șoferi ridesharing
9. `rotr-ce-este-cat-costa` — cine are nevoie, acte, valabilitate
10. `pilon-3-pensie-privata-merita` — deductibilitate, cum alegi
11. `asigurare-sanatate-privata-vs-cas` — ce primești în plus
12. `ce-asigurari-ii-trebuie-unui-pfa-sau-imm` — ghid pentru firme mici

Fiecare articol: 900–1.500 cuvinte, răspuns direct sub H1, H2 sub formă de întrebare, FAQ 3–5 la final, „Actualizat: <lună an>", autor Marina Metzak (link Despre), CTA spre produsul conex. Schema `Article` + `FAQPage` + `BreadcrumbList`. Conținutul e generat de Claude ca draft și validat tehnic de Marina înainte de publicare (ea răspunde de corectitudinea informațiilor de asigurări).

## 8. Homepage

Secțiuni, în ordine: hero (H1 „Ia și asigură! Asigurări online, cu o persoană reală pe WhatsApp", CTA WhatsApp + „Vezi asigurările"); grid produse (16 carduri, tip vizibil: „online" / „ofertă personalizată"); „De ce cu Marina" (3–4 argumente: persoană reală, asistent înregistrat ASF, cumperi online la orice oră, gratuit — comisionul e plătit de asigurător); „Cum funcționează" (3 pași); FAQ homepage (6 întrebări: e gratuit?, e legal să cumpăr prin asistent?, cât durează?, primesc polița pe e-mail?, pot din alt județ?, ce se întâmplă la daună?); testimoniale (placeholder); zone (linkuri); ultimele 3 articole; footer legal.

## 9. SEO / AEO tehnic

- `<head>` complet pe fiecare pagină: title (≤60 caractere, brand la final), description (≤155), canonical absolut, `robots` cu `max-snippet:-1, max-image-preview:large`, OG + Twitter (og:image 1200×630 per tip de pagină: generic, produs, articol), `theme-color`, favicon SVG, manifest.
- JSON-LD (ca în Contagex, noduri referențiate prin `@id`):
  - `InsuranceAgency` `@id: https://iasiasigura.com/#agency` — name IașiAsigură, `founder`/`employee` → Person, adresă Iași, `areaServed: {"@type":"Country","name":"România"}`, telephone, email, `sameAs` Facebook.
  - `Person` `@id: #marina` — name, jobTitle „Asistent în brokeraj", `worksFor` → Organization Destine Broker (cu `identifier` RBK-425), `identifier` RAF 160354, image, sameAs.
  - `WebSite` cu `publisher` → #agency.
  - Per produs: `Service` (`provider` → #agency, `serviceType`, `areaServed`) + `FAQPage` + `BreadcrumbList`.
  - Per articol: `Article` (`author` → #marina, `publisher` → #agency, datePublished, dateModified) + `FAQPage` + `BreadcrumbList`.
- `robots.txt`: allow all, explicit `User-agent: GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `CCBot` → Allow. `Sitemap:` absolut.
- `sitemap.xml` cu `lastmod` real (data modificării fișierului sursă). `llms.txt` cu descriere, persoană, lista paginilor cu o propoziție fiecare.
- Interlinking: homepage → toate produsele + zone + blog; produs → 3 conexe + 2–3 articole + zone; articol → produs; zonă → produse. Breadcrumb vizibil pe toate paginile secundare.
- Performanță: un singur `css/styles.css` (≤30 KB), un singur `js/script.js` (meniu mobil, buton WhatsApp flotant, nimic altceva), fonturi: `system-ui` stack (fără Google Fonts) — sau o singură familie cu `display=swap` dacă designul o cere. Imagini WebP cu dimensiuni explicite și `loading="lazy"`. Țintă Lighthouse ≥95 pe mobil la toate categoriile.
- Accesibilitate: contrast AA, focus vizibil, `aria-label` pe butoanele iconice, un singur H1 per pagină.

## 10. Design vizual

- Mobile-first, lățime maximă conținut 1100 px. Paletă: albastru închis (încredere) + accent cald (galben/portocaliu pentru „Ia și asigură!") + verde WhatsApp doar pe butoanele WhatsApp. Fără stock photos generice; poza Marinei + iconografie simplă SVG inline.
- Buton WhatsApp flotant jos-dreapta pe mobil și desktop, cu mesaj pre-completat contextual (numele produsului din pagină).
- Header: logo text „IașiAsigură", meniu: Asigurări (dropdown PF/PJ), Zone, Blog, Despre, Contact, buton WhatsApp.

## 11. Legal și conformitate

Footer identic pe toate paginile:

> Marina Metzak — asistent în brokeraj, persoană fizică independentă, cod RAF 160354. Înregistrat la Autoritatea de Supraveghere Financiară. Activitate desfășurată în numele și pe seama DESTINE BROKER DE ASIGURARE-REASIGURARE SRL (RBK-425). [Verifică în Registrul ASF] · [ANPC] · [SOL] · Termeni · Confidențialitate · Cookies

- `/termeni.html`: rolul site-ului (informare + redirecționare către platforma brokerului), fără vânzare directă, răspunderea pentru conținut, drepturi de autor.
- `/confidentialitate.html`: nu colectăm date prin site; WhatsApp și smartsales au propriile politici (link); Cloudflare Web Analytics fără cookie-uri; drepturile GDPR; contact.
- `/cookies.html`: site-ul nu setează cookie-uri proprii; fără banner.
- Înainte de lansare: Alexandru/Marina confirmă cu Destine Broker (conformitate) textul footer-ului și folosirea numelui/logo-ului Destine. Până la confirmare, logo-ul Destine **nu** apare; numele apare doar ca text în footer/Despre (obligație legală de informare).

## 12. Structura repo și `build.py`

```
marina-destine/
├── build.py                 # generator: citește content/, scrie HTML în root
├── content/
│   ├── site.json            # date fixe (§2), navigație, footer, URL smartsales
│   ├── products.json        # 16 produse: slug, nume, tip, path, grup, texte, faq, conexe
│   ├── zones.json           # 9 orașe: slug, nume, județ, texte locale, faq, produse relevante
│   ├── home.json            # secțiuni homepage (argumente, pași, faq, testimoniale)
│   └── blog/*.md            # articole cu frontmatter
├── templates.py             # head(), header(), footer(), cta_block(), faq_block(), ldjson()
├── css/styles.css
├── js/script.js
├── assets/                  # logo.svg, favicon.svg, og-*.png, marina.webp (TODO-MARINA)
├── index.html, despre.html, contact.html, termeni.html, ... (GENERATE)
├── asigurari/*.html, zone/*.html, blog/*.html (GENERATE)
├── robots.txt, sitemap.xml, llms.txt, site.webmanifest, 404.html, CNAME
├── scripts/check_links.py   # verifică href interne + linkurile smartsales (HTTP 200)
├── docs/research.md, docs/superpowers/specs/, docs/superpowers/plans/
└── README.md                # cum adaugi un produs / un articol / o zonă; cum publici
```

Reguli: `build.py` e idempotent (rulat de două ori → același output); fișierele generate au comentariu `<!-- generat de build.py — editează content/ -->`; nicio pagină nu se editează manual; `python3 build.py && python3 scripts/check_links.py` înainte de fiecare commit.

## 13. Testare și verificare

1. `python3 build.py` fără erori; `git status` arată doar diferențe intenționate.
2. `scripts/check_links.py`: toate `href` interne rezolvă la fișiere existente; toate URL-urile `metzak-marina.smartsales.ro` răspund 200; niciun link către `destine.smartsales.ro` sau `/presale/`.
3. Fiecare pagină: exact un `<h1>`, `<title>` unic, `description` unică, canonical corect, JSON-LD valid (parsabil + trecut prin Rich Results Test pentru 1 produs, 1 articol, homepage).
4. Preview local `python3 -m http.server 8080`, test manual la 375 px și desktop pe: homepage, `rca`, `imm`, `zone/iasi`, un articol.
5. Lighthouse mobil ≥95 pe homepage + o pagină produs + un articol.
6. După deploy: `https://iasiasigura.com` cu HTTPS valid, `www` redirecționează, Search Console verificat, sitemap trimis, `contact@` primește un e-mail de test.

## 14. Plan de achiziție clienți (în afara codului — pentru Marina/Alexandru)

1. **Google Business Profile** „IașiAsigură – Marina Metzak", categorie „Agenție de asigurări", service-area Iași + județ, fără adresă publică (întâlniri cu programare), program, WhatsApp, link site. Recenzii cerute după fiecare poliță cu un mesaj-șablon pe WhatsApp (link direct de recenzie).
2. **Pagină Facebook business + Instagram** (separat de profilul personal): fiecare articol de blog = postare; poze reale; răspunsuri la mesaje în <1 oră.
3. **Sinergie METZ CARS**: fiecare mașină vândută → ofertă RCA/CASCO de la Marina; link + QR în anunțurile Autovit și în actele de vânzare. **Triangle Club**: QR „Ia și asigură!" la bar/recepție.
4. **Comunități locale**: grupuri Facebook șoferi Bolt/Uber Iași (produsul SIGNAL), grupuri rezidenți/asistenți medicali UMF (malpraxis), firme de transport din Moldova (ROTR/CMR).
5. **Reînnoiri**: evidență simplă (Google Sheet) cu data expirării fiecărei polițe; WhatsApp cu 30 zile înainte. Venit recurent, cost zero.
6. **După 2–3 luni de conținut**: Google Ads local pe „rca iasi”, „asigurare locuinta iasi”, buget mic, landing = paginile produs.
7. **Trimestrial**: actualizează „Actualizat: <lună an>” pe articole după revizuire reală (nu doar data), adaugă 2–3 articole noi, cere 2–3 recenzii noi.

## 15. În afara scopului (v1)

Calculator de prețuri, formulare pe site, conturi de utilizator, versiune în engleză, pagini pentru toate județele, integrare CRM, newsletter, chat AI pe site.
