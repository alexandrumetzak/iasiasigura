# IașiAsigură — Plan de implementare site static

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Site static `iasiasigura.com` (HTML generat de `build.py`) pentru Marina Metzak, asistent în brokeraj, optimizat SEO/AEO, care trimite clienții la `metzak-marina.smartsales.ro` (cumpărare online) sau pe WhatsApp (ofertă).

**Architecture:** `build.py` citește `content/*.json` + `content/blog/*.md`, folosește funcțiile din `templates.py` (head/header/footer/JSON-LD/CTA) și scrie HTML în rădăcina repo-ului. Output-ul se comite; GitHub Pages servește din `main`/root. Zero backend, zero formulare, un CSS, un JS. Verificare automată cu `scripts/check_site.py` (structură, SEO, linkuri) + teste pytest pe generator.

**Tech Stack:** Python 3.11+ (stdlib + `markdown`), pytest, HTML5/CSS3/vanilla JS, GitHub Pages, Cloudflare DNS + Email Routing + Web Analytics.

Spec: `docs/superpowers/specs/2026-09-14-iasiasigura-site-design.md`. Research: `docs/research.md`.

## Global Constraints

- Domeniu canonic: `https://iasiasigura.com` (fără `www`). Brand: **IașiAsigură**, tagline **„Ia și asigură!"**.
- Persoană: Marina Metzak, asistent în brokeraj, PFI, cod RAF **160354**. Broker: DESTINE BROKER DE ASIGURARE-REASIGURARE SRL, RBK-425. Telefon/WhatsApp **+40 752 205 206**. E-mail `contact@iasiasigura.com`. Adresă: Bd. Metalurgiei nr. 4, Iași — „doar cu programare". Facebook `https://www.facebook.com/marina.metzak`.
- Toate linkurile către platformă: **numai** `https://metzak-marina.smartsales.ro/...` cu `?utm_source=iasiasigura&utm_medium=site&utm_campaign=<slug>`. Interzis: `destine.smartsales.ro`, orice URL cu `/presale/`.
- Fără prețuri/tarife/„de la X lei” nicăieri. Fără logo Destine până la confirmare scrisă (numele apare doar ca text).
- Fiecare pagină: exact un `<h1>`, `<title>` ≤ 60 caractere unic, `description` ≤ 155 unică, canonical absolut, JSON-LD valid.
- Fișierele generate poartă comentariul `<!-- generat de build.py — editează content/ -->` și nu se editează manual.
- Fără Google Fonts, fără cookie-uri proprii, fără GA4. Un singur `css/styles.css` (≤ 30 KB), un singur `js/script.js`.
- Limbă: română, diacritice corecte (ă â î ș ț). Ton direct, prietenos.
- Linkuri interne relative prin prefixul `R` (`""` în root, `"../"` în subfoldere). Canonical/OG/JSON-LD folosesc URL-uri absolute.
- Commit după fiecare task. Mesaje commit în română, prefix conventional (`feat:`, `content:`, `chore:`, `test:`), cu trailer `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

---

## Structura fișierelor

| Fișier | Responsabilitate |
|---|---|
| `content/site.json` | Date fixe (brand, persoană, contact, broker, navigație, footer legal, URL smartsales) |
| `content/home.json` | Secțiuni homepage (argumente, pași, FAQ, testimoniale) |
| `content/products.json` | 16 produse (slug, nume, tip, path smartsales, grup, texte, FAQ, conexe, articole) |
| `content/zones.json` | 9 orașe (slug, nume, județ, texte locale, FAQ, produse relevante) |
| `content/blog/<slug>.md` | Articole Markdown cu frontmatter |
| `content/pages/{despre,contact,termeni,confidentialitate,cookies}.html` | Fragmente HTML pentru paginile statice (corpul, fără head/header/footer) |
| `templates.py` | Funcții pure de randare: `head`, `header`, `footer`, `ldjson`, `breadcrumb`, `faqpage`, `agency_node`, `person_node`, `website_node`, `smartsales_url`, `wa_link`, `cta_block`, `faq_block`, `product_card`, `page` |
| `build.py` | Orchestrare: încarcă content, apelează `render_*`, scrie fișiere, sitemap, robots, llms.txt |
| `scripts/check_site.py` | Verificări post-build: h1 unic, title/desc unice, canonical, JSON-LD parsabil, linkuri interne, linkuri smartsales corecte (+ opțional HTTP 200 cu `--online`) |
| `tests/test_templates.py` | Teste unitare pentru `templates.py` |
| `tests/test_build.py` | Rulează `build.py` într-un tmpdir și verifică output-ul |
| `css/styles.css`, `js/script.js`, `assets/*` | Static |
| `CNAME`, `.gitignore`, `README.md`, `requirements.txt` | Repo |

---

### Task 1: Schelet repo, `content/site.json`, `templates.py` cu funcții de bază + teste

**Files:**
- Create: `requirements.txt`, `.gitignore`, `CNAME`, `content/site.json`, `templates.py`, `tests/test_templates.py`

**Interfaces:**
- Produces: `templates.SITE`, `templates.load_site() -> dict`, `smartsales_url(path: str, campaign: str) -> str`, `wa_link(text: str) -> str`, `ldjson(obj) -> str`, `breadcrumb(items: list[tuple[str, str|None]]) -> dict`, `faqpage(faqs: list[tuple[str,str]]) -> dict`, `agency_node() -> dict`, `person_node() -> dict`, `website_node() -> dict`, `head(title, desc, path, jsonld, R, og_image="/assets/og-default.png", og_type="website") -> str`, `header(R, wa_text) -> str`, `footer(R, wa_text) -> str`, `page(title, desc, path, jsonld, R, body, wa_text, og_image=..., og_type=...) -> str`.

- [ ] **Step 1: Fișiere de repo**

`requirements.txt`:
```
markdown==3.7
pytest==8.3.3
```

`.gitignore`:
```
__pycache__/
.pytest_cache/
.DS_Store
.claude/settings.local.json
```

`CNAME`:
```
iasiasigura.com
```

Rulează: `pip3 install -r requirements.txt`

- [ ] **Step 2: `content/site.json`**

```json
{
  "site_url": "https://iasiasigura.com",
  "brand": "IașiAsigură",
  "tagline": "Ia și asigură!",
  "smartsales": "https://metzak-marina.smartsales.ro",
  "person": {
    "name": "Marina Metzak",
    "job_title": "Asistent în brokeraj",
    "raf": "160354",
    "legal_form": "persoană fizică independentă",
    "phone_e164": "+40752205206",
    "phone_display": "+40 752 205 206",
    "wa_number": "40752205206",
    "email": "contact@iasiasigura.com",
    "facebook": "https://www.facebook.com/marina.metzak",
    "image": "/assets/marina.webp",
    "bio_short": "TODO-MARINA: 2 propoziții despre experiență (de câți ani în asigurări, ce produse preferă).",
    "address": {
      "street": "Bd. Metalurgiei nr. 4",
      "city": "Iași",
      "region": "Iași",
      "postal": "700000",
      "country": "RO",
      "note": "Întâlniri doar cu programare"
    },
    "geo": { "lat": 47.1385, "lng": 27.6135 }
  },
  "broker": {
    "name": "DESTINE BROKER DE ASIGURARE-REASIGURARE SRL",
    "rbk": "RBK-425",
    "url": "https://destine-broker.ro/",
    "cui": "21678074"
  },
  "links": {
    "asf_registry": "https://asfromania.ro/ro/a/1104/registre",
    "anpc": "https://anpc.ro/",
    "sol": "https://ec.europa.eu/consumers/odr/"
  },
  "nav": [
    ["asigurari/", "Asigurări"],
    ["zone/iasi.html", "Zone"],
    ["blog/", "Blog"],
    ["despre.html", "Despre Marina"],
    ["contact.html", "Contact"]
  ]
}
```

- [ ] **Step 3: Teste pentru funcțiile de bază** — `tests/test_templates.py`

```python
import json, re
import templates as T

def test_smartsales_url_adds_utm_before_fragment():
    u = T.smartsales_url("/home/asigurari#asigurariPj", "imm")
    assert u == ("https://metzak-marina.smartsales.ro/home/asigurari"
                 "?utm_source=iasiasigura&utm_medium=site&utm_campaign=imm#asigurariPj")

def test_smartsales_url_plain_path():
    assert T.smartsales_url("/rca", "rca").endswith("/rca?utm_source=iasiasigura&utm_medium=site&utm_campaign=rca")

def test_wa_link_encodes_text():
    u = T.wa_link("Bună Marina, vreau ofertă RCA")
    assert u.startswith("https://wa.me/40752205206?text=")
    assert "Bun%C4%83" in u and " " not in u

def test_ldjson_wraps_valid_json():
    s = T.ldjson({"@type": "Thing", "name": "Ăț"})
    assert s.startswith('<script type="application/ld+json">')
    inner = s.split(">", 1)[1].rsplit("<", 1)[0]
    assert json.loads(inner)["name"] == "Ăț"

def test_breadcrumb_positions_and_absolute_urls():
    b = T.breadcrumb([("Acasă", "/"), ("Asigurări", "/asigurari/"), ("RCA", None)])
    items = b["itemListElement"]
    assert [i["position"] for i in items] == [1, 2, 3]
    assert items[0]["item"] == "https://iasiasigura.com/"
    assert "item" not in items[2]

def test_faqpage_shape():
    f = T.faqpage([("Q?", "A.")])
    assert f["@type"] == "FAQPage" and f["mainEntity"][0]["acceptedAnswer"]["text"] == "A."

def test_agency_and_person_nodes_have_ids_and_raf():
    a, p = T.agency_node(), T.person_node()
    assert a["@id"] == "https://iasiasigura.com/#agency" and a["@type"] == "InsuranceAgency"
    assert p["@id"] == "https://iasiasigura.com/#marina" and p["jobTitle"] == "Asistent în brokeraj"
    assert any(i.get("value") == "160354" for i in p["identifier"])
    assert p["worksFor"]["name"].startswith("DESTINE BROKER")

def test_head_has_canonical_title_desc_and_no_google_fonts():
    h = T.head("Titlu", "Desc", "/asigurari/rca.html", [T.website_node()], "../")
    assert '<link rel="canonical" href="https://iasiasigura.com/asigurari/rca.html" />' in h
    assert "<title>Titlu</title>" in h and 'content="Desc"' in h
    assert "fonts.googleapis" not in h
    assert 'href="../css/styles.css"' in h

def test_page_has_single_h1_marker_and_footer_legal():
    out = T.page("T", "D", "/x.html", [], "", "<h1>Salut</h1>", "Bună")
    assert out.count("<h1") == 1
    assert "RAF 160354" in out and "Înregistrat la Autoritatea de Supraveghere Financiară" in out
    assert "generat de build.py" in out
    assert "destine.smartsales.ro" not in out
```

- [ ] **Step 4: Rulează testele → FAIL**

Run: `cd ~/Work/marina-destine && python3 -m pytest tests/test_templates.py -q`
Expected: `ModuleNotFoundError: No module named 'templates'`

- [ ] **Step 5: `templates.py`**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Funcții pure de randare pentru IașiAsigură. Nu scrie fișiere; build.py o face."""
import html, json, os, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))

def load_site():
    with open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8") as f:
        return json.load(f)

S = load_site()
SITE = S["site_url"]
SMARTSALES = S["smartsales"]
P = S["person"]
AGENCY_ID = SITE + "/#agency"
PERSON_ID = SITE + "/#marina"
GENERATED = "<!-- generat de build.py — editează content/ -->"

WA_SVG = ('<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" '
          'd="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 12 12 0 0 0 4.6 4c1.7.7 2.1.6 2.8.5a2.4 2.4 0 0 0 1.6-1.1 2 2 0 0 0 .1-1.1c0-.2-.2-.2-.5-.3z"/></svg>')

def smartsales_url(path, campaign):
    base, _, frag = path.partition("#")
    u = f"{SMARTSALES}{base}?utm_source=iasiasigura&utm_medium=site&utm_campaign={campaign}"
    return u + (f"#{frag}" if frag else "")

def wa_link(text):
    return f"https://wa.me/{P['wa_number']}?text=" + urllib.parse.quote(text)

def ldjson(obj):
    return ('<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>')

def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": SITE + u} if u else {})}
                                for i, (n, u) in enumerate(items)]}

def faqpage(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def person_node():
    return {"@context": "https://schema.org", "@type": "Person", "@id": PERSON_ID,
            "name": P["name"], "jobTitle": P["job_title"], "url": SITE + "/despre.html",
            "image": SITE + P["image"], "telephone": P["phone_e164"], "email": P["email"],
            "sameAs": [P["facebook"]],
            "identifier": [{"@type": "PropertyValue", "propertyID": "RAF", "value": P["raf"]}],
            "worksFor": {"@type": "Organization", "name": S["broker"]["name"], "url": S["broker"]["url"],
                          "identifier": {"@type": "PropertyValue", "propertyID": "RBK", "value": S["broker"]["rbk"]}}}

def agency_node():
    a = P["address"]
    return {"@context": "https://schema.org", "@type": "InsuranceAgency", "@id": AGENCY_ID,
            "name": S["brand"], "slogan": S["tagline"], "url": SITE + "/",
            "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/og-default.png",
            "telephone": P["phone_e164"], "email": P["email"],
            "founder": {"@id": PERSON_ID}, "employee": {"@id": PERSON_ID},
            "address": {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"],
                        "addressRegion": a["region"], "postalCode": a["postal"], "addressCountry": a["country"]},
            "geo": {"@type": "GeoCoordinates", "latitude": P["geo"]["lat"], "longitude": P["geo"]["lng"]},
            "areaServed": {"@type": "Country", "name": "România"},
            "sameAs": [P["facebook"]], "priceRange": "Gratuit pentru client"}

def website_node():
    return {"@context": "https://schema.org", "@type": "WebSite", "name": S["brand"], "url": SITE + "/",
            "inLanguage": "ro-RO", "publisher": {"@id": AGENCY_ID}}

def head(title, desc, path, jsonld, R, og_image="/assets/og-default.png", og_type="website"):
    canonical = SITE + path
    blocks = "\n  ".join(ldjson(o) for o in jsonld)
    t, d = html.escape(title), html.escape(desc)
    return f"""<!DOCTYPE html>
<html lang="ro">
<head>
  {GENERATED}
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t}</title>
  <meta name="description" content="{d}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <link rel="canonical" href="{canonical}" />
  <meta name="theme-color" content="#0b2545" />
  <meta name="geo.region" content="RO-IS" />
  <meta name="geo.placename" content="Iași" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:locale" content="ro_RO" />
  <meta property="og:site_name" content="{S['brand']}" />
  <meta property="og:title" content="{t}" />
  <meta property="og:description" content="{d}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE}{og_image}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{t}" />
  <meta name="twitter:description" content="{d}" />
  <meta name="twitter:image" content="{SITE}{og_image}" />
  <link rel="icon" href="{R}assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="{R}assets/apple-touch-icon.png" />
  <link rel="manifest" href="{R}site.webmanifest" />
  <link rel="stylesheet" href="{R}css/styles.css" />
  {blocks}
</head>
<body>"""

def nav_items(R):
    return "".join(f'<li><a href="{R}{href}">{label}</a></li>' for href, label in S["nav"])

def header(R, wa_text):
    return f"""
  <a class="skip-link" href="#main">Sari la conținut</a>
  <header class="site-header">
    <div class="container header-inner">
      <a href="{R}index.html" class="brand" aria-label="{S['brand']} — acasă">
        <span class="brand-mark" aria-hidden="true">Ia</span>
        <span class="brand-text"><strong>Iași<em>Asigură</em></strong><small>{S['tagline']}</small></span>
      </a>
      <nav class="nav" aria-label="Navigare principală">
        <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Deschide meniul"><span></span><span></span><span></span></button>
        <ul class="nav-menu" id="nav-menu">{nav_items(R)}</ul>
      </nav>
      <a href="{wa_link(wa_text)}" class="btn btn-wa header-wa" target="_blank" rel="noopener" aria-label="Scrie pe WhatsApp">{WA_SVG}<span>WhatsApp</span></a>
    </div>
  </header>
  <main id="main">"""

def footer(R, wa_text):
    b, L, a = S["broker"], S["links"], P["address"]
    return f"""
  </main>
  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <p class="footer-brand"><strong>Iași<em>Asigură</em></strong> · {S['tagline']}</p>
        <p class="footer-desc">Asigurări online pentru toată România, cu o persoană reală pe WhatsApp: {P['name']}, {P['job_title'].lower()}.</p>
        <p><a href="{P['facebook']}" rel="noopener" target="_blank">Facebook</a></p>
      </div>
      <div><h3>Asigurări</h3><ul>
        <li><a href="{R}asigurari/rca.html">RCA</a></li><li><a href="{R}asigurari/casco.html">CASCO</a></li>
        <li><a href="{R}asigurari/locuinta.html">Locuință</a></li><li><a href="{R}asigurari/pad.html">PAD</a></li>
        <li><a href="{R}asigurari/calatorie.html">Călătorie</a></li><li><a href="{R}asigurari/sanatate.html">Sănătate</a></li>
        <li><a href="{R}asigurari/malpraxis.html">Malpraxis</a></li><li><a href="{R}asigurari/">Toate asigurările</a></li></ul></div>
      <div><h3>Zone</h3><ul>
        <li><a href="{R}zone/iasi.html">Iași</a></li><li><a href="{R}zone/pascani.html">Pașcani</a></li>
        <li><a href="{R}zone/bacau.html">Bacău</a></li><li><a href="{R}zone/vaslui.html">Vaslui</a></li>
        <li><a href="{R}zone/botosani.html">Botoșani</a></li><li><a href="{R}zone/suceava.html">Suceava</a></li>
        <li><a href="{R}zone/piatra-neamt.html">Piatra Neamț</a></li><li><a href="{R}zone/roman.html">Roman</a></li>
        <li><a href="{R}zone/galati.html">Galați</a></li></ul></div>
      <div><h3>Contact</h3><ul>
        <li><a href="{wa_link(wa_text)}" target="_blank" rel="noopener">WhatsApp {P['phone_display']}</a></li>
        <li><a href="tel:{P['phone_e164']}">{P['phone_display']}</a></li>
        <li><a href="mailto:{P['email']}">{P['email']}</a></li>
        <li>{a['street']}, {a['city']} · {a['note'].lower()}</li>
        <li><a href="{R}despre.html">Despre Marina</a> · <a href="{R}blog/">Blog</a></li></ul></div>
    </div>
    <div class="container footer-legal">
      <p><strong>{P['name']}</strong> — {P['job_title'].lower()}, {P['legal_form']}, cod RAF {P['raf']}. Înregistrat la Autoritatea de Supraveghere Financiară. Activitate desfășurată în numele și pe seama {b['name']} ({b['rbk']}).</p>
      <p><a href="{L['asf_registry']}" rel="noopener" target="_blank">Verifică în Registrul ASF</a> · <a href="{L['anpc']}" rel="noopener" target="_blank">ANPC</a> · <a href="{L['sol']}" rel="noopener" target="_blank">SOL</a> · <a href="{R}termeni.html">Termeni</a> · <a href="{R}confidentialitate.html">Confidențialitate</a> · <a href="{R}cookies.html">Cookies</a></p>
      <p>&copy; <span id="year">2026</span> {S['brand']}. Acest site informează și redirecționează către platforma brokerului; nu afișează prețuri și nu colectează date personale.</p>
    </div>
  </footer>
  <a href="{wa_link(wa_text)}" class="fab-wa" target="_blank" rel="noopener" aria-label="Scrie pe WhatsApp">{WA_SVG}</a>
  <script src="{R}js/script.js" defer></script>
</body>
</html>"""

def page(title, desc, path, jsonld, R, body, wa_text, og_image="/assets/og-default.png", og_type="website"):
    return head(title, desc, path, jsonld, R, og_image, og_type) + header(R, wa_text) + body + footer(R, wa_text)
```

- [ ] **Step 6: Rulează testele → PASS**

Run: `python3 -m pytest tests/test_templates.py -q`
Expected: `9 passed`

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .gitignore CNAME content/site.json templates.py tests/test_templates.py
git commit -m "feat: schelet templates.py + site.json + teste

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Blocuri reutilizabile (CTA, FAQ, card produs) + CSS + JS + assets de bază

**Files:**
- Modify: `templates.py` (adaugă `cta_block`, `faq_block`, `product_card`, `related_block`)
- Create: `css/styles.css`, `js/script.js`, `assets/favicon.svg`, `assets/logo.svg`, `site.webmanifest`
- Test: `tests/test_templates.py` (adaugă)

**Interfaces:**
- Produces: `cta_block(product: dict, R) -> str` (product are `slug`, `name`, `type` ∈ {`online`,`consultanta`}, `path`, `wa_text`), `faq_block(faqs: list[tuple[str,str]], heading="Întrebări frecvente") -> str`, `product_card(p: dict, R) -> str`, `related_block(title, items: list[tuple[str,str]], R) -> str` (items = (href relativ fără R, label)).

- [ ] **Step 1: Teste**

Adaugă în `tests/test_templates.py`:

```python
RCA = {"slug": "rca", "name": "Asigurare RCA", "type": "online", "path": "/rca",
       "wa_text": "Bună Marina, vreau ofertă RCA.", "short": "Obligatorie pentru orice vehicul.", "icon": "🚗"}
IMM = {"slug": "imm", "name": "Asigurări IMM", "type": "consultanta", "path": "/home/asigurari#asigurariPj",
       "wa_text": "Bună Marina, vreau ofertă pentru firma mea.", "short": "Bunuri, răspundere, angajați.", "icon": "🏢"}

def test_cta_online_primary_is_smartsales_secondary_wa():
    h = T.cta_block(RCA, "../")
    assert 'class="btn btn-primary"' in h and "utm_campaign=rca" in h
    assert h.index("smartsales.ro") < h.index("wa.me")
    assert "Cumpără online" in h

def test_cta_consultanta_primary_is_wa_secondary_smartsales_form():
    h = T.cta_block(IMM, "../")
    assert h.index("wa.me") < h.index("smartsales.ro")
    assert "Cere ofertă pe WhatsApp" in h and "#asigurariPj" in h and "utm_campaign=imm" in h

def test_faq_block_uses_h3_questions():
    h = T.faq_block([("Cât durează?", "5 minute.")])
    assert "<h3>Cât durează?</h3>" in h and "5 minute." in h

def test_product_card_links_and_badge():
    h = T.product_card(RCA, "")
    assert 'href="asigurari/rca.html"' in h and "Online" in h
    assert "Ofertă personalizată" in T.product_card(IMM, "")
```

- [ ] **Step 2: Rulează → FAIL** (`AttributeError: module 'templates' has no attribute 'cta_block'`)

- [ ] **Step 3: Implementare în `templates.py`** (după `website_node`)

```python
def cta_block(p, R):
    ss = smartsales_url(p["path"], p["slug"])
    wa = wa_link(p["wa_text"])
    if p["type"] == "online":
        return f"""
    <div class="cta-row">
      <a href="{ss}" class="btn btn-primary" target="_blank" rel="noopener">Cumpără online</a>
      <a href="{wa}" class="btn btn-wa" target="_blank" rel="noopener">{WA_SVG}<span>Întreabă pe WhatsApp</span></a>
      <p class="cta-note">Cumperi direct pe platforma brokerului, în câteva minute, la orice oră. Polița vine pe e-mail.</p>
    </div>"""
    return f"""
    <div class="cta-row">
      <a href="{wa}" class="btn btn-wa btn-primary-wa" target="_blank" rel="noopener">{WA_SVG}<span>Cere ofertă pe WhatsApp</span></a>
      <a href="{ss}" class="btn btn-ghost-dark" target="_blank" rel="noopener">Formular de ofertă pe platformă</a>
      <p class="cta-note">Produs cu ofertă personalizată: Marina compară asigurătorii și îți trimite oferta pe WhatsApp sau e-mail. Gratuit.</p>
    </div>"""

def faq_block(faqs, heading="Întrebări frecvente"):
    items = "".join(f'<details class="faq-item"><summary><h3>{html.escape(q)}</h3></summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs)
    return f'\n    <section class="faq" id="faq"><h2>{heading}</h2>{items}</section>'

def product_card(p, R):
    badge = "Online" if p["type"] == "online" else "Ofertă personalizată"
    cls = "badge-online" if p["type"] == "online" else "badge-consult"
    return (f'<a class="card product-card" href="{R}asigurari/{p["slug"]}.html">'
            f'<span class="card-icon" aria-hidden="true">{p["icon"]}</span><span class="badge {cls}">{badge}</span>'
            f'<h3>{html.escape(p["name"])}</h3><p>{html.escape(p["short"])}</p></a>')

def related_block(title, items, R):
    lis = "".join(f'<li><a href="{R}{href}">{html.escape(label)}</a></li>' for href, label in items)
    return f'\n    <aside class="related"><h2>{title}</h2><ul>{lis}</ul></aside>' if items else ""
```

- [ ] **Step 4: Rulează → PASS** (`13 passed`)

- [ ] **Step 5: `css/styles.css`** (mobile-first; paletă albastru închis + accent galben cald + verde WhatsApp)

```css
/* IașiAsigură — stiluri. Fără fonturi externe. */
:root{--navy:#0b2545;--navy-2:#13315c;--blue:#1f5fa8;--sun:#f5b301;--sun-2:#ffcb3d;--wa:#25d366;--wa-2:#1ebe5b;
--ink:#132238;--slate:#4b5b70;--muted:#7a879a;--line:#e3e8ef;--bg:#fff;--bg-soft:#f5f8fc;--bg-alt:#eef3f9;
--radius:14px;--radius-sm:10px;--shadow:0 10px 30px rgba(11,37,69,.10);--container:1100px;
--ff:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;font-family:var(--ff);color:var(--ink);background:var(--bg);line-height:1.65;font-size:17px;-webkit-font-smoothing:antialiased}
h1,h2,h3{line-height:1.2;color:var(--navy);margin:0 0 .5em;letter-spacing:-.01em}
h1{font-size:clamp(1.9rem,4.5vw,3rem);font-weight:800}h2{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:700}h3{font-size:1.15rem;font-weight:650}
p{margin:0 0 1rem;color:var(--slate)}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
img,svg{max-width:100%;height:auto}ul,ol{padding-left:1.3rem;color:var(--slate)}
.container{width:100%;max-width:var(--container);margin-inline:auto;padding-inline:20px}.container-narrow{max-width:820px}
.skip-link{position:absolute;left:-999px;top:0;z-index:1000;background:var(--navy);color:#fff;padding:10px 16px}.skip-link:focus{left:0}
/* butoane */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font-weight:700;font-size:1rem;padding:13px 24px;border-radius:999px;border:2px solid transparent;cursor:pointer;transition:transform .15s,background .2s;text-decoration:none!important}
.btn:hover{transform:translateY(-2px)}
.btn-primary{background:var(--sun);color:var(--navy)}.btn-primary:hover{background:var(--sun-2)}
.btn-wa{background:var(--wa);color:#fff}.btn-wa:hover{background:var(--wa-2)}
.btn-ghost{background:transparent;border-color:rgba(255,255,255,.55);color:#fff}
.btn-ghost-dark{background:transparent;border-color:var(--navy);color:var(--navy)}
.cta-row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:1.2rem 0 1.6rem}.cta-note{flex-basis:100%;font-size:.92rem;color:var(--muted);margin:0}
/* header */
.site-header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.header-inner{display:flex;align-items:center;gap:16px;min-height:68px}
.brand{display:flex;align-items:center;gap:10px;color:var(--navy);text-decoration:none!important}
.brand-mark{display:grid;place-items:center;width:42px;height:42px;border-radius:12px;background:var(--sun);color:var(--navy);font-weight:900;font-size:1.1rem}
.brand-text strong{display:block;font-size:1.15rem;line-height:1.1}.brand-text em{font-style:normal;color:var(--blue)}.brand-text small{display:block;font-size:.72rem;color:var(--muted)}
.nav{margin-left:auto}.nav-menu{list-style:none;margin:0;padding:0;display:flex;gap:4px}
.nav-menu a{display:block;padding:10px 12px;border-radius:10px;color:var(--ink);font-weight:600;font-size:.95rem}.nav-menu a:hover{background:var(--bg-alt);text-decoration:none}
.nav-toggle{display:none;background:none;border:0;width:44px;height:44px;cursor:pointer}.nav-toggle span{display:block;width:22px;height:2px;background:var(--navy);margin:5px auto}
.header-wa{padding:10px 16px;font-size:.95rem}
/* hero */
.hero{background:linear-gradient(135deg,var(--navy) 0%,var(--navy-2) 60%,#1a4a86 100%);color:#fff;padding:56px 0 48px}
.hero h1{color:#fff}.hero p{color:rgba(255,255,255,.88);font-size:1.15rem;max-width:640px}.hero .eyebrow{color:var(--sun)}
.eyebrow{font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;color:var(--blue);margin:0 0 .6rem}
.hero-points{display:flex;flex-wrap:wrap;gap:10px 22px;list-style:none;padding:0;margin:1.2rem 0 0;color:rgba(255,255,255,.9);font-size:.95rem}
/* secțiuni și carduri */
section{padding:52px 0}.section-alt{background:var(--bg-soft)}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.card{display:block;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:20px;box-shadow:0 1px 3px rgba(11,37,69,.06);transition:transform .15s,box-shadow .2s;color:inherit;text-decoration:none!important}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow)}.card h3{margin:.4rem 0 .3rem}.card p{margin:0;font-size:.95rem}
.card-icon{font-size:1.6rem}.badge{float:right;font-size:.72rem;font-weight:700;padding:3px 9px;border-radius:999px}
.badge-online{background:#e6f7ee;color:#137a3d}.badge-consult{background:#fff3cf;color:#8a5b00}
.steps{counter-reset:s;display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.step{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:22px}
.step::before{counter-increment:s;content:counter(s);display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--sun);color:var(--navy);font-weight:800;margin-bottom:10px}
/* pagini conținut */
.page-hero{background:var(--bg-soft);padding:36px 0 26px;border-bottom:1px solid var(--line)}
.breadcrumb{list-style:none;padding:0;margin:0 0 12px;display:flex;flex-wrap:wrap;gap:6px;font-size:.88rem;color:var(--muted)}.breadcrumb li+li::before{content:"›";margin-right:6px}
.lead{font-size:1.15rem;color:var(--ink)}
.prose h2{margin-top:2rem}.prose li{margin-bottom:.35rem}.two-col{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.check li::marker{content:"✔ ";color:#137a3d}.cross li::marker{content:"✖ ";color:#b42318}
.faq-item{border:1px solid var(--line);border-radius:var(--radius-sm);margin-bottom:10px;background:#fff}.faq-item summary{cursor:pointer;padding:14px 18px;list-style:none}.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary h3{display:inline;font-size:1.02rem;margin:0}.faq-item summary::after{content:"+";float:right;font-weight:700;color:var(--blue)}.faq-item[open] summary::after{content:"–"}
.faq-a{padding:0 18px 14px}.faq-a p{margin:0}
.related{background:var(--bg-alt);border-radius:var(--radius);padding:20px 24px;margin:2rem 0}.related h2{font-size:1.2rem}.related ul{margin:0}
.author-box{display:flex;gap:16px;align-items:center;border:1px solid var(--line);border-radius:var(--radius);padding:18px;margin:2rem 0;background:#fff}
.author-box img{width:76px;height:76px;border-radius:50%;object-fit:cover}
.article-meta{color:var(--muted);font-size:.9rem}.article-card time{display:block;color:var(--muted);font-size:.85rem;margin-bottom:6px}
.testimonial{background:#fff;border-left:4px solid var(--sun);padding:16px 20px;border-radius:0 var(--radius-sm) var(--radius-sm) 0}
.testimonial cite{display:block;margin-top:8px;font-style:normal;color:var(--muted);font-size:.9rem}
/* footer */
.site-footer{background:var(--navy);color:rgba(255,255,255,.85);padding:48px 0 24px;margin-top:40px}
.site-footer a{color:#fff}.site-footer h3{color:var(--sun);font-size:1rem;margin-bottom:.6rem}.site-footer ul{list-style:none;padding:0;margin:0}.site-footer li{margin-bottom:6px;font-size:.95rem}
.site-footer p{color:rgba(255,255,255,.8)}.footer-grid{display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.footer-brand{font-size:1.2rem;color:#fff}.footer-brand em{font-style:normal;color:var(--sun)}
.footer-legal{border-top:1px solid rgba(255,255,255,.15);margin-top:28px;padding-top:18px;font-size:.85rem}
.fab-wa{position:fixed;right:18px;bottom:18px;z-index:60;display:grid;place-items:center;width:58px;height:58px;border-radius:50%;background:var(--wa);color:#fff;box-shadow:0 10px 24px rgba(37,211,102,.4)}
.fab-wa svg{width:30px;height:30px}
@media (max-width:860px){
  .nav-toggle{display:block}.nav{margin-left:auto}
  .nav-menu{display:none;position:absolute;left:0;right:0;top:68px;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;padding:10px 16px 16px}
  .nav-menu.open{display:flex}.header-wa span{display:none}.header-wa{padding:10px}
  .hero{padding:40px 0 36px}section{padding:40px 0}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.btn,.card{transition:none}}
```

- [ ] **Step 6: `js/script.js`**

```js
/* IașiAsigură — meniu mobil + an în footer. Fără tracking, fără cookie-uri. */
(function () {
  'use strict';
  var y = document.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { menu.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }
})();
```

- [ ] **Step 7: Assets de bază**

`assets/favicon.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#f5b301"/><text x="32" y="43" font-family="system-ui,Arial,sans-serif" font-size="30" font-weight="800" text-anchor="middle" fill="#0b2545">Ia</text></svg>
```

`assets/logo.svg` (folosit și pentru og/logo.png în Task 9):
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 96" width="420" height="96"><rect x="4" y="8" width="80" height="80" rx="18" fill="#f5b301"/><text x="44" y="64" font-family="system-ui,Arial,sans-serif" font-size="40" font-weight="800" text-anchor="middle" fill="#0b2545">Ia</text><text x="100" y="52" font-family="system-ui,Arial,sans-serif" font-size="40" font-weight="800" fill="#0b2545">Iași<tspan fill="#1f5fa8">Asigură</tspan></text><text x="102" y="80" font-family="system-ui,Arial,sans-serif" font-size="18" fill="#7a879a">Ia și asigură!</text></svg>
```

`site.webmanifest`:
```json
{"name":"IașiAsigură","short_name":"IașiAsigură","start_url":"/","display":"browser","background_color":"#ffffff","theme_color":"#0b2545","icons":[{"src":"/assets/favicon.svg","sizes":"any","type":"image/svg+xml"}]}
```

- [ ] **Step 8: Verifică dimensiunea CSS și commit**

Run: `wc -c css/styles.css` → Expected: sub 30000.

```bash
git add templates.py tests/test_templates.py css js assets site.webmanifest
git commit -m "feat: blocuri CTA/FAQ/card, CSS, JS, favicon, logo

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3: `build.py` cu homepage + `content/home.json` + `check_site.py` + test de build

**Files:**
- Create: `build.py`, `content/home.json`, `scripts/check_site.py`, `tests/test_build.py`, `content/products.json` (versiune minimă: doar câmpurile de card pentru 16 produse; textele complete vin în Task 4)

**Interfaces:**
- Produces: `build.build(root: str) -> list[str]` (returnează căile scrise; `root` = directorul de output, implicit repo root), `build.load_json(name) -> Any`, `build.PRODUCTS`, `build.write(root, path, content)`.
- `scripts/check_site.py [--online] [root]` → exit 0 dacă totul e ok, altfel listează problemele și exit 1.

- [ ] **Step 1: `content/home.json`**

```json
{
  "title": "Asigurări online în toată România | IașiAsigură – Marina Metzak",
  "desc": "Ia și asigură! RCA, locuință, PAD, călătorie, sănătate, malpraxis, firme. Cumperi online pe platforma brokerului sau ceri ofertă pe WhatsApp. Marina Metzak, asistent în brokeraj, Iași.",
  "h1": "Ia și asigură! Asigurări online, cu o persoană reală pe WhatsApp",
  "lead": "Cumperi RCA, locuință, călătorie sau sănătate online, în câteva minute, pe platforma brokerului. Pentru firme, agricol sau CASCO primești ofertă personalizată pe WhatsApp. Gratuit: comisionul e plătit de asigurător, nu de tine.",
  "points": ["Asistent în brokeraj înregistrat la ASF (RAF 160354)", "Oriunde în România, 100% online", "Răspuns pe WhatsApp în timpul programului", "Polița vine pe e-mail"],
  "why": [
    ["O persoană, nu un call-center", "Vorbești cu Marina, pe WhatsApp sau la telefon. Aceeași persoană înainte și după ce ai polița, inclusiv la daună."],
    ["Înregistrată la ASF", "Marina e asistent în brokeraj cu cod RAF 160354, în numele Destine Broker (RBK-425), broker cu peste 15 ani pe piață. Poți verifica în registrul ASF."],
    ["Cumperi online, la orice oră", "Platforma brokerului compară asigurătorii și emite polița pe loc. Plătești cu cardul, polița vine pe e-mail."],
    ["Nu costă nimic în plus", "Prețul e cel al asigurătorului. Comisionul de intermediere e plătit de asigurător, nu de tine."]
  ],
  "steps": [
    ["Alegi asigurarea", "Din lista de mai sus. Pentru RCA, locuință, PAD, călătorie, sănătate sau malpraxis, apeși „Cumpără online”."],
    ["Completezi datele", "Pe platforma brokerului, în câteva minute. Dacă ai nelămuriri, scrii pe WhatsApp și Marina te ghidează."],
    ["Primești polița pe e-mail", "Imediat după plată. Pentru produsele cu ofertă personalizată, Marina îți trimite oferta și emite polița după confirmare."]
  ],
  "faq": [
    ["Cât costă serviciul Marinei?", "Nimic în plus. Prețul poliței este cel stabilit de asigurător, iar comisionul de intermediere este plătit de asigurător, nu de client."],
    ["Este legal să cumpăr asigurări printr-un asistent în brokeraj?", "Da. Asistentul în brokeraj este un intermediar secundar înregistrat la ASF, care lucrează în numele unui broker autorizat. Marina are codul RAF 160354 și lucrează în numele Destine Broker (RBK-425)."],
    ["Cât durează să cumpăr o asigurare online?", "Pentru RCA, PAD sau călătorie, de obicei sub 10 minute: completezi datele, alegi oferta, plătești cu cardul și primești polița pe e-mail."],
    ["Pot cumpăra dacă nu sunt din Iași?", "Da. Platforma funcționează online pentru toată România. Întâlnirile față în față se fac la Iași, doar cu programare."],
    ["Primesc polița pe hârtie?", "Polița se emite electronic și se trimite pe e-mail. Este valabilă în format digital; o poți tipări dacă vrei."],
    ["Ce fac dacă am o daună?", "Scrii Marinei pe WhatsApp. Îți spune exact ce acte trebuie și cum deschizi dosarul de daună la asigurător."]
  ],
  "testimonials": [
    ["TODO-MARINA: testimonial 1 (2–3 propoziții).", "Client, Iași"],
    ["TODO-MARINA: testimonial 2.", "Client, Bacău"],
    ["TODO-MARINA: testimonial 3.", "Client, Suceava"]
  ]
}
```

- [ ] **Step 2: `content/products.json` minim** (16 intrări; Task 4 le completează cu textele lungi). Ordinea = ordinea în grid.

```json
[
 {"slug":"rca","name":"Asigurare RCA","type":"online","path":"/rca","group":["pf","pj"],"icon":"🚗","short":"Obligatorie pentru orice vehicul. Online în 5 minute.","wa_text":"Bună Marina, vreau ofertă RCA."},
 {"slug":"casco","name":"Asigurare CASCO","type":"consultanta","path":"/home/asigurari#auto","group":["pf","pj"],"icon":"🛡️","short":"Avarii, furt, vandalism. Ofertă comparată.","wa_text":"Bună Marina, vreau ofertă CASCO."},
 {"slug":"locuinta","name":"Asigurare locuință","type":"online","path":"/locuinta","group":["pf"],"icon":"🏠","short":"Facultativă: incendiu, inundație, furt, răspundere.","wa_text":"Bună Marina, vreau ofertă pentru asigurarea locuinței."},
 {"slug":"pad","name":"Asigurare PAD","type":"online","path":"/pad","group":["pf"],"icon":"🌍","short":"Obligatorie: cutremur, inundație, alunecări de teren.","wa_text":"Bună Marina, vreau să fac PAD pentru locuință."},
 {"slug":"calatorie","name":"Asigurare de călătorie","type":"online","path":"/travel","group":["pf"],"icon":"✈️","short":"Medicală în străinătate, pentru orice destinație.","wa_text":"Bună Marina, vreau asigurare de călătorie."},
 {"slug":"storno","name":"Asigurare storno","type":"online","path":"/travel","group":["pf"],"icon":"🎫","short":"Îți recuperezi banii dacă anulezi călătoria.","wa_text":"Bună Marina, vreau asigurare storno."},
 {"slug":"sanatate","name":"Asigurare de sănătate","type":"online","path":"/sanatate","group":["pf"],"icon":"🩺","short":"Acces la clinici private, fără liste de așteptare.","wa_text":"Bună Marina, vreau ofertă pentru asigurare de sănătate."},
 {"slug":"viata","name":"Asigurare de viață","type":"consultanta","path":"/home/asigurari#sanatate","group":["pf"],"icon":"❤️","short":"Protecție pentru familie, cu sau fără economisire.","wa_text":"Bună Marina, vreau ofertă pentru asigurare de viață."},
 {"slug":"pensii-private","name":"Pensie privată Pilon III","type":"consultanta","path":"/home/asigurari#sanatate","group":["pf"],"icon":"🏦","short":"Contribuție deductibilă, pensie în plus.","wa_text":"Bună Marina, vreau detalii despre Pilonul III."},
 {"slug":"malpraxis","name":"Asigurare malpraxis","type":"online","path":"/malpraxis","group":["pf"],"icon":"⚕️","short":"Obligatorie pentru medici, asistenți, rezidenți.","wa_text":"Bună Marina, vreau asigurare de malpraxis."},
 {"slug":"raspundere-civila","name":"Răspundere civilă","type":"consultanta","path":"/home/asigurari#asigurariPj","group":["pf","pj"],"icon":"⚖️","short":"Profesională sau personală, pentru daune aduse terților.","wa_text":"Bună Marina, vreau ofertă pentru răspundere civilă."},
 {"slug":"taxi-uber-bolt","name":"Asigurare taxi / Uber / Bolt","type":"online","path":"/accidente","group":["pf","pj"],"icon":"🚕","short":"Accidente pentru șofer și pasageri, ridesharing.","wa_text":"Bună Marina, sunt șofer Bolt/Uber și vreau asigurarea de accidente."},
 {"slug":"rotr","name":"Asigurare ROTR","type":"online","path":"/rotr","group":["pj"],"icon":"🚛","short":"Pentru licența de transport rutier.","wa_text":"Bună Marina, vreau asigurare ROTR."},
 {"slug":"cargo-cmr","name":"CARGO și CMR","type":"consultanta","path":"/home/asigurari#asigurariPj","group":["pj"],"icon":"📦","short":"Marfa transportată și răspunderea cărăușului.","wa_text":"Bună Marina, vreau ofertă CMR/CARGO."},
 {"slug":"imm","name":"Asigurări pentru IMM","type":"consultanta","path":"/home/asigurari#asigurariPj","group":["pj"],"icon":"🏢","short":"Bunuri, răspundere, angajați, echipamente.","wa_text":"Bună Marina, vreau ofertă de asigurare pentru firma mea."},
 {"slug":"agricole","name":"Asigurări agricole","type":"consultanta","path":"/home/asigurari#asigurariPj","group":["pj"],"icon":"🌾","short":"Culturi, animale, utilaje.","wa_text":"Bună Marina, vreau ofertă pentru asigurare agricolă."}
]
```

- [ ] **Step 3: `tests/test_build.py`**

```python
import os, re, json, subprocess, sys
import pytest
import build

@pytest.fixture(scope="module")
def out(tmp_path_factory):
    root = tmp_path_factory.mktemp("site")
    build.build(str(root))
    return root

def read(root, p): return (root / p).read_text(encoding="utf-8")

def test_homepage_written_with_single_h1_and_products(out):
    h = read(out, "index.html")
    assert h.count("<h1") == 1 and "Ia și asigură!" in h
    assert h.count('class="card product-card"') == 16
    assert "generat de build.py" in h

def test_homepage_jsonld_parses_and_has_agency_person_faq(out):
    h = read(out, "index.html")
    blocks = re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', h, re.S)
    types = {json.loads(b)["@type"] for b in blocks}
    assert {"InsuranceAgency", "Person", "WebSite", "FAQPage"} <= types

def test_no_forbidden_smartsales_links(out):
    for dp, _, fs in os.walk(out):
        for f in fs:
            if f.endswith(".html"):
                t = open(os.path.join(dp, f), encoding="utf-8").read()
                assert "destine.smartsales.ro" not in t and "/presale/" not in t, f

def test_check_site_passes(out):
    r = subprocess.run([sys.executable, "scripts/check_site.py", str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
```

- [ ] **Step 4: Rulează → FAIL** (`ModuleNotFoundError: No module named 'build'`)

- [ ] **Step 5: `build.py`**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator IașiAsigură. Rulează: python3 build.py  (scrie HTML în rădăcina repo-ului)."""
import html, json, os, sys, datetime
import templates as T

ROOT = T.ROOT
CONTENT = os.path.join(ROOT, "content")
WA_DEFAULT = "Bună Marina, vreau informații despre o asigurare."

def load_json(name):
    with open(os.path.join(CONTENT, name), encoding="utf-8") as f:
        return json.load(f)

PRODUCTS = load_json("products.json")
BY_SLUG = {p["slug"]: p for p in PRODUCTS}
HOME = load_json("home.json")
WRITTEN = []

def write(root, path, content):
    full = os.path.join(root, path.lstrip("/"))
    os.makedirs(os.path.dirname(full) or root, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    WRITTEN.append(path)

def crumbs_html(items, R):
    lis = "".join(f'<li><a href="{R}{u.lstrip("/") if u != "/" else "index.html"}">{html.escape(n)}</a></li>' if u else f"<li>{html.escape(n)}</li>" for n, u in items)
    return f'<ol class="breadcrumb" aria-label="Breadcrumb">{lis}</ol>'

# ---------------------------------------------------------------- HOMEPAGE
def render_home():
    R = ""
    cards = "".join(T.product_card(p, R) for p in PRODUCTS)
    points = "".join(f"<li>✔ {html.escape(x)}</li>" for x in HOME["points"])
    why = "".join(f'<div class="card"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for t, d in HOME["why"])
    steps = "".join(f'<div class="step"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for t, d in HOME["steps"])
    testi = "".join(f'<blockquote class="testimonial"><p>{html.escape(q)}</p><cite>{html.escape(w)}</cite></blockquote>' for q, w in HOME["testimonials"])
    zones = "".join(f'<li><a href="zone/{s}.html">Asigurări {n}</a></li>' for s, n in ZONE_LINKS)
    wa = T.wa_link(WA_DEFAULT)
    body = f"""
  <section class="hero"><div class="container">
    <p class="eyebrow">Marina Metzak · asistent în brokeraj · RAF {T.P['raf']}</p>
    <h1>{html.escape(HOME['h1'])}</h1>
    <p>{html.escape(HOME['lead'])}</p>
    <div class="cta-row"><a href="{wa}" class="btn btn-wa" target="_blank" rel="noopener">{T.WA_SVG}<span>Scrie pe WhatsApp</span></a><a href="#asigurari" class="btn btn-primary">Vezi asigurările</a></div>
    <ul class="hero-points">{points}</ul>
  </div></section>
  <section id="asigurari"><div class="container"><p class="eyebrow">Asigurări</p><h2>Alege asigurarea de care ai nevoie</h2>
    <p>Cele marcate <strong>Online</strong> se cumpără direct pe platforma brokerului. Cele cu <strong>Ofertă personalizată</strong> se rezolvă pe WhatsApp, cu ofertă comparată de Marina.</p>
    <div class="grid">{cards}</div></div></section>
  <section class="section-alt" id="de-ce"><div class="container"><p class="eyebrow">De ce cu Marina</p><h2>Asigurări simple, cu cineva care răspunde</h2><div class="grid">{why}</div></div></section>
  <section id="cum"><div class="container"><p class="eyebrow">Cum funcționează</p><h2>Trei pași, fără drumuri</h2><div class="steps">{steps}</div></div></section>
  <section class="section-alt"><div class="container container-narrow">{T.faq_block(HOME['faq'])}</div></section>
  <section id="testimoniale"><div class="container"><p class="eyebrow">Clienți</p><h2>Ce spun clienții</h2><div class="grid">{testi}</div></div></section>
  <section class="section-alt" id="zone"><div class="container"><p class="eyebrow">Zone</p><h2>Iași, Moldova și online în toată România</h2>
    <p>Întâlniri la Iași, cu programare. Restul se rezolvă pe WhatsApp și pe platformă, oriunde ai fi.</p><ul class="grid" style="list-style:none;padding:0">{zones}</ul></div></section>
  <section id="blog"><div class="container"><p class="eyebrow">Blog</p><h2>Ghiduri scrise pe înțelesul tău</h2><div class="grid" id="home-articles">{LATEST_ARTICLES_HTML[0]}</div><p><a href="blog/">Toate articolele →</a></p></div></section>"""
    jsonld = [T.website_node(), T.agency_node(), T.person_node(), T.faqpage([tuple(x) for x in HOME["faq"]])]
    return T.page(HOME["title"], HOME["desc"], "/", jsonld, R, body, WA_DEFAULT)

ZONE_LINKS = [("iasi", "Iași"), ("pascani", "Pașcani"), ("bacau", "Bacău"), ("vaslui", "Vaslui"), ("botosani", "Botoșani"),
              ("suceava", "Suceava"), ("piatra-neamt", "Piatra Neamț"), ("roman", "Roman"), ("galati", "Galați")]
LATEST_ARTICLES_HTML = [""]  # setat de render_blog (Task 6); listă ca să fie mutabil

# ---------------------------------------------------------------- BUILD
def build(root=ROOT):
    WRITTEN.clear()
    write(root, "/index.html", render_home())
    return list(WRITTEN)

if __name__ == "__main__":
    for p in build(ROOT if len(sys.argv) < 2 else sys.argv[1]):
        print("scris:", p)
```

- [ ] **Step 6: `scripts/check_site.py`**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifică output-ul generat. Folosire: python3 scripts/check_site.py [--online] [root]"""
import json, os, re, sys, urllib.request

ONLINE = "--online" in sys.argv
args = [a for a in sys.argv[1:] if a != "--online"]
ROOT = os.path.abspath(args[0]) if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://iasiasigura.com"
problems, titles, descs, ss_urls = [], {}, {}, set()

def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, "/")

for dp, dns, fs in os.walk(ROOT):
    dns[:] = [d for d in dns if not d.startswith(".") and d not in ("content", "tests", "scripts", "docs", "node_modules", "__pycache__")]
    for f in fs:
        if not f.endswith(".html"): continue
        path = os.path.join(dp, f); r = rel(path)
        t = open(path, encoding="utf-8").read()
        if r == "404.html": continue
        if t.count("<h1") != 1: problems.append(f"{r}: {t.count('<h1')} h1")
        m = re.search(r"<title>(.*?)</title>", t, re.S); title = m.group(1) if m else ""
        if not title: problems.append(f"{r}: fără title")
        elif len(title) > 60: problems.append(f"{r}: title {len(title)} caractere")
        if title in titles: problems.append(f"{r}: title duplicat cu {titles[title]}")
        titles[title] = r
        m = re.search(r'<meta name="description" content="(.*?)"', t); d = m.group(1) if m else ""
        if not d: problems.append(f"{r}: fără description")
        elif len(d) > 160: problems.append(f"{r}: description {len(d)} caractere")
        if d in descs: problems.append(f"{r}: description duplicată cu {descs[d]}")
        descs[d] = r
        expect = SITE + "/" + ("" if r == "index.html" else r.replace("index.html", ""))
        m = re.search(r'<link rel="canonical" href="(.*?)"', t)
        if not m or m.group(1) != expect: problems.append(f"{r}: canonical {m.group(1) if m else None} != {expect}")
        for b in re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', t, re.S):
            try: json.loads(b)
            except Exception as e: problems.append(f"{r}: JSON-LD invalid: {e}")
        if "destine.smartsales.ro" in t or "/presale/" in t: problems.append(f"{r}: link smartsales interzis")
        ss_urls.update(re.findall(r'https://metzak-marina\.smartsales\.ro[^"\s]*', t))
        for href in re.findall(r'href="([^"#?]+)', t):
            if href.startswith(("http", "mailto:", "tel:")): continue
            target = os.path.normpath(os.path.join(dp, href))
            if href.endswith("/"): target = os.path.join(target, "index.html")
            if not os.path.exists(target): problems.append(f"{r}: link rupt {href}")
        if re.search(r"\b(de la|doar|numai)\s+\d+\s*(lei|ron|€|eur)", t, re.I): problems.append(f"{r}: pare să conțină un preț")

for u in sorted(ss_urls):
    if "utm_source=iasiasigura" not in u: problems.append(f"smartsales fără UTM: {u}")
    if ONLINE:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            code = urllib.request.urlopen(req, timeout=20).getcode()
            if code != 200: problems.append(f"{u}: HTTP {code}")
        except Exception as e: problems.append(f"{u}: {e}")

print(f"{len(titles)} pagini verificate, {len(ss_urls)} URL-uri smartsales")
for p in problems: print("PROBLEMĂ:", p)
sys.exit(1 if problems else 0)
```

- [ ] **Step 7: Rulează testele → PASS**

Run: `python3 -m pytest -q` → Expected: `17 passed`. Apoi `python3 build.py && python3 scripts/check_site.py` → `1 pagini verificate, 0 URL-uri smartsales`, exit 0.

Notă: `test_check_site_passes` verifică linkurile interne; până la Task 4–7, homepage-ul linkează spre pagini inexistente (`asigurari/rca.html`, `zone/...`, `blog/`). Pentru ca testul să treacă acum, `check_site.py` primește flag-ul `--no-links` **doar** în acest task: adaugă în `check_site.py` linia `CHECK_LINKS = "--no-links" not in sys.argv` și condiționează bucla `for href in ...` cu `if CHECK_LINKS:`; în `tests/test_build.py` folosește `["scripts/check_site.py", "--no-links", str(out)]`. În Task 7 se scoate `--no-links` din test.

- [ ] **Step 8: Preview vizual**

Run: `python3 -m http.server 8080` și deschide `http://localhost:8080/` la 375 px și desktop. Verifică: hero lizibil, 16 carduri, badge-uri, meniu mobil se deschide, buton WhatsApp flotant, footer legal cu RAF.

- [ ] **Step 9: Commit**

```bash
git add build.py content/home.json content/products.json scripts/check_site.py tests/test_build.py index.html
git commit -m "feat: build.py cu homepage, check_site.py, teste de build

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4: Pagini produs (16) + catalog `/asigurari/`

**Files:**
- Modify: `content/products.json` (adaugă câmpurile lungi), `build.py` (adaugă `render_product`, `render_catalog`)
- Test: `tests/test_build.py` (adaugă)

**Interfaces:**
- Consumes: `T.cta_block`, `T.faq_block`, `T.related_block`, `T.page`, `T.breadcrumb`, `T.faqpage`, `T.agency_node`.
- Produces: fișiere `asigurari/<slug>.html`, `asigurari/index.html`. Câmpuri noi în products.json: `title`, `desc`, `h1`, `answer`, `covers[]`, `not_covers[]`, `docs[]`, `steps[]` (3), `faq[[q,a]]` (6–8), `related[]` (3 slug-uri), `articles[]` (slug-uri de blog, pot fi goale până la Task 6), `service_type`.

- [ ] **Step 1: Teste**

```python
def test_all_products_rendered_with_correct_cta(out):
    for p in build.PRODUCTS:
        h = read(out, f"asigurari/{p['slug']}.html")
        assert h.count("<h1") == 1
        assert f"utm_campaign={p['slug']}" in h
        if p["type"] == "online":
            assert "Cumpără online" in h and f"metzak-marina.smartsales.ro{p['path'].split('#')[0]}?" in h
        else:
            assert "Cere ofertă pe WhatsApp" in h
        assert '"@type": "Service"' in h and '"@type": "FAQPage"' in h and '"@type": "BreadcrumbList"' in h

def test_catalog_lists_pf_and_pj(out):
    h = read(out, "asigurari/index.html")
    assert "Pentru tine" in h and "Pentru firma ta" in h and h.count('class="card product-card"') >= 16
```

- [ ] **Step 2: Rulează → FAIL** (`FileNotFoundError: asigurari/rca.html`)

- [ ] **Step 3: Completează `content/products.json`**

Schema completă, exemplificată integral pe `rca` (celelalte 15 urmează același format, cu conținutul din brief-urile de mai jos):

```json
{"slug":"rca","name":"Asigurare RCA","type":"online","path":"/rca","group":["pf","pj"],"icon":"🚗",
 "short":"Obligatorie pentru orice vehicul. Online în 5 minute.",
 "wa_text":"Bună Marina, vreau ofertă RCA.",
 "service_type":"Asigurare de răspundere civilă auto (RCA)",
 "title":"Asigurare RCA online, oriunde în România | IașiAsigură",
 "desc":"Cumpără RCA online în 5 minute, cu oferte de la toți asigurătorii, prin Marina Metzak, asistent în brokeraj înregistrat la ASF. Polița vine pe e-mail. Fără costuri suplimentare.",
 "h1":"Asigurare RCA online: compari ofertele și primești polița pe e-mail",
 "answer":"RCA este asigurarea obligatorie prin lege pentru orice vehicul înmatriculat în România. Acoperă daunele pe care le provoci altora într-un accident. O cumperi online, pe platforma brokerului, comparând ofertele asigurătorilor autorizați, iar polița ajunge pe e-mail imediat după plată.",
 "covers":["Daune materiale produse altor vehicule sau bunuri","Vătămări corporale și deces ale terților","Cheltuieli de judecată legate de accident","Valabilitate în UE și în țările din Cartea Verde","Decontare directă (opțional): ți se repară mașina la propriul asigurător"],
 "not_covers":["Propriul tău vehicul (pentru asta există CASCO)","Daunele produse intenționat sau sub influența alcoolului","Daunele produse de un șofer fără permis valabil","Bunurile transportate în vehiculul tău"],
 "docs":["Talonul (certificatul de înmatriculare)","CI sau CUI-ul proprietarului","Datele șoferilor care vor conduce (pentru cotația corectă)"],
 "steps":[["Apasă „Cumpără online”","Ajungi pe platforma brokerului, pe pagina RCA a Marinei."],["Completează numărul de înmatriculare și datele","Platforma afișează ofertele asigurătorilor. Alegi perioada (1–12 luni) și opțiunile."],["Plătești cu cardul","Polița se emite pe loc și vine pe e-mail. Dacă ai nelămuriri, scrii pe WhatsApp."]],
 "faq":[
  ["Cât durează să fac RCA online?","De obicei sub 10 minute: introduci numărul de înmatriculare, verifici datele, alegi oferta și plătești cu cardul. Polița vine pe e-mail imediat."],
  ["Pot face RCA pentru 1 lună?","Da, RCA se poate încheia pe perioade de la 1 la 12 luni. Perioadele scurte sunt utile la vânzare, la înmatriculare temporară sau când mașina stă în garaj."],
  ["Ce este clasa bonus-malus?","Este sistemul prin care istoricul tău de daune influențează prima. Fără daune, urci în clase de bonus (B1–B8) și plătești mai puțin; cu daune, cobori în clase de malus (M1–M8)."],
  ["Ce înseamnă decontare directă?","O clauză opțională prin care, dacă nu ești vinovat, repari mașina la propriul asigurător, care recuperează apoi banii de la asigurătorul vinovatului."],
  ["Primesc polița pe hârtie?","Nu e nevoie. Polița RCA electronică, primită pe e-mail, este valabilă și poate fi verificată de Poliție în baza de date."],
  ["Pot renunța după ce am cumpărat?","Da. La RCA încheiat la distanță ai drept de retragere în 14 zile, cu restituire integrală dacă polița nu a intrat în vigoare, sau pro-rata dacă a intrat și nu a existat daună."],
  ["Marina ia comision de la mine?","Nu. Prețul e cel al asigurătorului, iar comisionul de intermediere e plătit de asigurător."]
 ],
 "related":["casco","taxi-uber-bolt","locuinta"],
 "articles":["pret-rca-2026-cum-se-calculeaza","bonus-malus-explicat","rca-sau-casco-diferente"]}
```

Brief-uri pentru celelalte 15 (implementatorul scrie textele în același format, 40–60 cuvinte la `answer`, 4–6 elemente la `covers`/`not_covers`, 3 `docs`, 3 `steps`, 6–7 `faq`, 3 `related`, `articles` din lista Task 6). Fără prețuri.

| slug | title (≤60) | answer (esență) | FAQ (întrebări) | related |
|---|---|---|---|---|
| casco | Asigurare CASCO cu ofertă comparată \| IașiAsigură | Facultativă; acoperă propriul vehicul: avarii, furt, vandalism, fenomene naturale; Marina compară asigurătorii și trimite oferta | Ce diferență față de RCA? Ce franșiză aleg? Mașină în leasing? Cât durează oferta? Acoperă și în străinătate? Ce acte trebuie? | rca, taxi-uber-bolt, imm |
| locuinta | Asigurare locuință facultativă online \| IașiAsigură | Protejează clădirea și bunurile la incendiu, inundație de la vecini, furt, fenomene; completează PAD; online | Diferența față de PAD? Ce sumă asigurată aleg? Apartament în chirie? Acoperă și bunurile? Ce fac la daună? Merge cu credit ipotecar? | pad, imm, raspundere-civila |
| pad | Asigurare PAD obligatorie online \| IașiAsigură | Obligatorie prin lege pentru orice locuință; acoperă cutremur, inundație, alunecări; sumă și primă fixe prin PAID; online în 5 minute | Cine e obligat? Ce amendă e? Ce sume acoperă? Diferența față de facultativă? Cât durează? Pot pentru locuința părinților? | locuinta, imm, calatorie |
| calatorie | Asigurare medicală de călătorie online \| IașiAsigură | Acoperă urgențe medicale, spitalizare, repatriere în străinătate; se cumpără online în 2 minute, pentru orice destinație | Cardul european nu ajunge? Ce sumă pentru SUA/Asia? Sporturi de iarnă? Cât înainte de plecare? Copiii? Ce fac dacă am nevoie de doctor? | storno, sanatate, rca |
| storno | Asigurare storno călătorie online \| IașiAsigură | Îți restituie costurile nerambursabile dacă anulezi din motive acoperite (boală, accident, deces în familie) | Când trebuie cumpărată? Ce motive sunt acceptate? Acoperă și zboruri low-cost? Diferența față de medicală? Ce acte la despăgubire? | calatorie, sanatate, viata |
| sanatate | Asigurare de sănătate privată online \| IașiAsigură | Acces la clinici private, consultații, analize, spitalizare, fără liste de așteptare; se cumpără online | Diferența față de abonament clinică? Include spitalizare? Boli preexistente? Pentru copii? Deductibilă pentru firmă? Ce clinici? | viata, calatorie, imm |
| viata | Asigurare de viață cu ofertă personalizată \| IașiAsigură | Protecție financiară pentru familie la deces/invaliditate; opțional economisire; ofertă comparată de Marina | Cât să fie suma asigurată? Cu sau fără economisire? Se cere control medical? Pentru credit ipotecar? Cât durează? Ce se întâmplă dacă renunț? | pensii-private, sanatate, locuinta |
| pensii-private | Pensie privată Pilon III, ofertă personalizată \| IașiAsigură | Contribuție voluntară (deductibilă până la 400 €/an per persoană) într-un fond privat; ofertă și înscriere cu Marina | Diferența față de Pilon II? Cât pot contribui? Când pot retrage? Ce randament? Poate plăti firma? Ce se întâmplă la deces? | viata, sanatate, imm |
| malpraxis | Asigurare malpraxis online pentru medici \| IașiAsigură | Obligatorie pentru personalul medical (medici, rezidenți, asistenți, farmaciști, kineto, psihologi); acoperă răspunderea pentru erori profesionale; online | Cine e obligat? Ce limită aleg? Rezident sau asistent? Valabilă în tot spitalul? Cât durează? Acoperă și cheltuieli de judecată? | raspundere-civila, sanatate, viata |
| raspundere-civila | Răspundere civilă profesională și personală \| IașiAsigură | Acoperă daunele aduse terților în activitatea profesională (avocați, contabili, IT, construcții) sau în viața privată (familie, câine, chiriaș) | Ce profesii au nevoie? Ce diferență față de malpraxis? Acoperă și amenzi? Chiriaș față de proprietar? Cât durează oferta? | malpraxis, imm, locuinta |
| taxi-uber-bolt | Asigurare accidente taxi, Uber, Bolt online \| IașiAsigură | Asigurare de accidente pentru șofer și pasageri în taxi/ridesharing (produs SIGNAL), cerută la autorizare; online; opțional asistență rutieră | E obligatorie pentru Bolt/Uber? Ce acoperă pentru pasageri? Se face pe mașină sau pe șofer? PFA sau SRL? Include tractare? Ce acte? | rca, casco, rotr |
| rotr | Asigurare ROTR pentru licență de transport \| IașiAsigură | Asigurare de răspundere a operatorului de transport rutier, cerută la obținerea/reînnoirea licenței ARR; online | Cine are nevoie? Ce sumă cere ARR? Pe firmă sau pe vehicul? Cât durează? Diferența față de CMR? Ce acte? | cargo-cmr, rca, imm |
| cargo-cmr | Asigurare CMR și CARGO transport marfă \| IașiAsigură | CMR = răspunderea cărăușului pentru marfa transportată; CARGO = marfa proprietarului; ofertă comparată | Diferența CMR/CARGO? Sumă în funcție de marfă? Transport intern/internațional? Refrigerată? Cabotaj? Cât durează oferta? | rotr, imm, raspundere-civila |
| imm | Asigurări pentru IMM și PFA, ofertă personalizată \| IașiAsigură | Pachet pentru firme mici: clădire și bunuri, echipamente, răspundere față de terți, accidente angajați; ofertă comparată | Ce e obligatoriu pentru o firmă? Magazin/restaurant/atelier? Spațiu închiriat? Angajații? Cât costă ca timp? Ce acte? | raspundere-civila, cargo-cmr, agricole |
| agricole | Asigurări agricole: culturi, animale, utilaje \| IașiAsigură | Culturi (grindină, secetă, îngheț), animale, utilaje agricole; necesară la subvenții/credite APIA; ofertă comparată | Ce riscuri pentru culturi? Se cere la APIA? Când se încheie (calendar)? Utilajele au nevoie de RCA? Animale? Cât durează oferta? | imm, rca, raspundere-civila |

- [ ] **Step 4: `render_product` și `render_catalog` în `build.py`**

```python
def render_product(p, articles_by_slug):
    R = "../"; path = f"/asigurari/{p['slug']}.html"
    crumbs = [("Acasă", "/"), ("Asigurări", "/asigurari/"), (p["name"], None)]
    covers = "".join(f"<li>{html.escape(x)}</li>" for x in p["covers"])
    nots = "".join(f"<li>{html.escape(x)}</li>" for x in p["not_covers"])
    docs = "".join(f"<li>{html.escape(x)}</li>" for x in p["docs"])
    steps = "".join(f'<div class="step"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for t, d in p["steps"])
    rel_products = [(f"asigurari/{s}.html", BY_SLUG[s]["name"]) for s in p["related"] if s in BY_SLUG]
    rel_articles = [(f"blog/{s}.html", articles_by_slug[s]["title"]) for s in p.get("articles", []) if s in articles_by_slug]
    body = f"""
  <section class="page-hero"><div class="container">{crumbs_html(crumbs, R)}
    <h1>{html.escape(p['h1'])}</h1><p class="lead">{html.escape(p['answer'])}</p>{T.cta_block(p, R)}</div></section>
  <div class="container prose">
    <div class="two-col"><div><h2>Ce acoperă</h2><ul class="check">{covers}</ul></div><div><h2>Ce nu acoperă</h2><ul class="cross">{nots}</ul></div></div>
    <h2>Acte necesare</h2><ul>{docs}</ul>
    <h2>Cum cumperi în 3 pași</h2><div class="steps">{steps}</div>
    {T.faq_block([tuple(x) for x in p['faq']])}
    {T.related_block("Asigurări conexe", rel_products, R)}{T.related_block("Citește și", rel_articles, R)}
    {author_box(R)}
    {T.cta_block(p, R)}
  </div>"""
    service = {"@context": "https://schema.org", "@type": "Service", "name": p["name"], "serviceType": p["service_type"],
               "provider": {"@id": T.AGENCY_ID}, "areaServed": {"@type": "Country", "name": "România"},
               "url": T.SITE + path, "description": p["answer"]}
    jsonld = [service, T.faqpage([tuple(x) for x in p["faq"]]), T.breadcrumb(crumbs)]
    return T.page(p["title"], p["desc"], path, jsonld, R, body, p["wa_text"], og_image="/assets/og-produs.png")

def author_box(R):
    P = T.P
    return f"""<div class="author-box"><img src="{R}assets/marina.webp" alt="{html.escape(P['name'])}" width="76" height="76" loading="lazy" />
      <div><strong>{P['name']}</strong>, {P['job_title'].lower()} (RAF {P['raf']})<br /><span class="article-meta">{html.escape(P['bio_short'])}</span><br /><a href="{R}despre.html">Despre Marina →</a></div></div>"""

def render_catalog():
    R = "../"; path = "/asigurari/"
    pf = "".join(T.product_card(p, R) for p in PRODUCTS if "pf" in p["group"])
    pj = "".join(T.product_card(p, R) for p in PRODUCTS if "pj" in p["group"])
    crumbs = [("Acasă", "/"), ("Asigurări", None)]
    body = f"""
  <section class="page-hero"><div class="container">{crumbs_html(crumbs, R)}<h1>Toate asigurările</h1>
    <p class="lead">Online = cumperi direct pe platforma brokerului. Ofertă personalizată = Marina compară asigurătorii și îți trimite oferta pe WhatsApp.</p></div></section>
  <section><div class="container"><h2>Pentru tine și familia ta</h2><div class="grid">{pf}</div></div></section>
  <section class="section-alt"><div class="container"><h2>Pentru firma ta</h2><div class="grid">{pj}</div></div></section>"""
    return T.page("Toate asigurările, online sau cu ofertă | IașiAsigură",
                  "Lista completă: RCA, CASCO, locuință, PAD, călătorie, sănătate, viață, pensii, malpraxis, răspundere civilă, taxi/Uber, ROTR, CMR, IMM, agricole.",
                  path, [T.breadcrumb(crumbs)], R, body, WA_DEFAULT)
```

În `build()` adaugă după homepage:
```python
    write(root, "/asigurari/index.html", render_catalog())
    for p in PRODUCTS:
        write(root, f"/asigurari/{p['slug']}.html", render_product(p, ARTICLES_BY_SLUG))
```
și definește la nivel de modul `ARTICLES_BY_SLUG = {}` (populat în Task 6).

- [ ] **Step 5: Rulează → PASS**; apoi `python3 build.py && python3 scripts/check_site.py --no-links` → 0 probleme (title ≤ 60, description ≤ 160, fără prețuri).

- [ ] **Step 6: Preview** `asigurari/rca.html` și `asigurari/imm.html` la 375 px: CTA-uri în ordinea corectă, FAQ expandabil, breadcrumb.

- [ ] **Step 7: Commit**

```bash
git add content/products.json build.py tests/test_build.py asigurari/
git commit -m "content: 16 pagini produs + catalog asigurari

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 5: Pagini geo (9)

**Files:**
- Create: `content/zones.json`
- Modify: `build.py` (`render_zone`), `tests/test_build.py`

**Interfaces:**
- Produces: `zone/<slug>.html`. Schema zones.json: `slug`, `name`, `county`, `title`, `desc`, `h1`, `answer`, `local[]` (2–3 paragrafe, ≥ 120 cuvinte fiecare, specifice orașului), `products[]` (4–6 slug-uri), `faq[[q,a]]` (4), `geo_region` (ex. `RO-IS`).

- [ ] **Step 1: Test**

```python
def test_zones_rendered_and_distinct(out):
    texts = []
    for s, _ in build.ZONE_LINKS:
        h = read(out, f"zone/{s}.html")
        assert h.count("<h1") == 1 and '"areaServed"' in h and '"@type": "FAQPage"' in h
        body = re.sub(r"<[^>]+>", " ", h.split('<main id="main">')[1].split("</main>")[0])
        texts.append(set(body.split()))
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            shared = len(texts[i] & texts[j]) / min(len(texts[i]), len(texts[j]))
            assert shared < 0.75, f"zone {i} și {j} prea asemănătoare ({shared:.0%})"
```

- [ ] **Step 2: Rulează → FAIL**

- [ ] **Step 3: `content/zones.json`** — exemplu complet pentru Iași; celelalte 8 după brief.

```json
[
 {"slug":"iasi","name":"Iași","county":"Iași","geo_region":"RO-IS",
  "title":"Asigurări Iași: RCA, locuință, sănătate | IașiAsigură",
  "desc":"Asigurări în Iași cu Marina Metzak, asistent în brokeraj înregistrat la ASF. RCA, CASCO, locuință, PAD, sănătate, malpraxis, Bolt/Uber. Online sau întâlnire cu programare.",
  "h1":"Asigurări în Iași, cu o persoană reală: Marina Metzak",
  "answer":"Dacă ești din Iași, poți cumpăra online orice asigurare de pe acest site sau poți stabili o întâlnire cu Marina, în Bd. Metalurgiei nr. 4, cu programare pe WhatsApp. RCA, locuință, PAD și călătorie se rezolvă în câteva minute; CASCO, firme și viață primesc ofertă comparată.",
  "local":[
   "Iașiul are peste 200.000 de vehicule înmatriculate și un trafic tot mai aglomerat pe Păcurari, Nicolina, Tudor Vladimirescu sau centura spre Lețcani. Asta înseamnă RCA obligatoriu pentru fiecare mașină, dar și tot mai multe motive pentru CASCO: parcări înghesuite, grindină vara, șantiere. Pentru mașinile aduse din import, RCA se face imediat după înmatriculare, iar Marina te ghidează online, fără drumuri la birou.",
   "Orașul e cel mai mare centru universitar-medical din Moldova. Rezidenții și asistenții medicali de la UMF, Spitalul Sf. Spiridon, Parhon sau Institutul Regional de Oncologie au nevoie de asigurare de malpraxis, care se cumpără online în câteva minute. Tot aici lucrează mii de șoferi Bolt și Uber, care au nevoie de asigurarea de accidente pentru pasageri la autorizare.",
   "Pentru locuință, în Iași contează PAD-ul obligatoriu (zonă seismică) și o asigurare facultativă care acoperă inundațiile de la vecini, tipice în blocurile din Tătărași, Alexandru cel Bun sau Dacia. Ansamblurile noi din Bucium, Copou sau Valea Adâncă sunt de regulă asigurate la cerința băncii; Marina te ajută să iei exact ce cere banca, fără extra."
  ],
  "products":["rca","casco","locuinta","pad","malpraxis","taxi-uber-bolt"],
  "faq":[
   ["Pot veni la birou în Iași?","Da, cu programare pe WhatsApp, în Bd. Metalurgiei nr. 4. Majoritatea clienților rezolvă totul online, dar dacă preferi o întâlnire, o stabilim."],
   ["Faceți RCA pentru mașini din import, abia înmatriculate în Iași?","Da. Ai nevoie de talon (sau de dovada de înmatriculare) și de CI. Se face online, în aceeași zi."],
   ["Sunt rezident la UMF Iași. Ce asigurare de malpraxis îmi trebuie?","Asigurarea de răspundere civilă profesională medicală, obligatorie pentru rezidenți. Limita se alege în funcție de specialitate; se cumpără online în câteva minute."],
   ["Sunt șofer Bolt în Iași. Ce asigurare îmi cere primăria la autorizare?","Asigurarea de accidente pentru șofer și pasageri. Se face online, pe mașină, și o primești pe e-mail."]
  ]}
]
```

Brief-uri pentru celelalte 8 (fiecare cu `local` scris specific, 3 paragrafe distincte):

| slug | name / county / geo | unghiuri locale (pentru `local`) | products |
|---|---|---|---|
| pascani | Pașcani / Iași / RO-IS | nod feroviar, navetiști spre Iași (RCA, călătorie), case cu grădină (locuință + PAD), mici firme și ateliere (IMM) | rca, locuinta, pad, imm, calatorie |
| bacau | Bacău / Bacău / RO-BC | firme de transport pe E85 și A7 (ROTR, CMR), aeroport (călătorie), industrie și IMM, zonă cu inundații pe Siret (locuință + PAD) | rca, rotr, cargo-cmr, imm, locuinta, pad |
| vaslui | Vaslui / Vaslui / RO-VS | agricultură (culturi, utilaje), navetă spre Iași, gospodării rurale (PAD), transportatori mici | agricole, rca, pad, locuinta, rotr |
| botosani | Botoșani / Botoșani / RO-BT | agricultură și zootehnie, diaspora (călătorie, viață pentru familie), locuințe în zone cu inundații pe Prut/Siret | agricole, rca, calatorie, viata, pad |
| suceava | Suceava / Suceava / RO-SV | transport internațional (CMR, ROTR), turism în Bucovina (pensiuni = IMM, răspundere), aeroport (călătorie), zone de munte (locuință, alunecări) | rotr, cargo-cmr, imm, rca, calatorie, pad |
| piatra-neamt | Piatra Neamț / Neamț / RO-NT | turism montan și pensiuni (IMM), lemn și ateliere (răspundere), navetă și trafic pe DN15 (RCA/CASCO) | rca, casco, imm, raspundere-civila, locuinta |
| roman | Roman / Neamț / RO-NT | industrie (Arcelor), firme de transport pe E85, apropiere de Bacău și Iași, agricultură pe Siret | rca, rotr, imm, agricole, pad |
| galati | Galați / Galați / RO-GL | port și industrie (CARGO, IMM, angajați), Dunăre (inundații → PAD), șantier naval, navetă spre Brăila | cargo-cmr, imm, pad, locuinta, rca |

- [ ] **Step 4: `render_zone` în `build.py`**

```python
ZONES = load_json("zones.json")

def render_zone(z):
    R = "../"; path = f"/zone/{z['slug']}.html"
    crumbs = [("Acasă", "/"), ("Zone", "/zone/iasi.html"), (z["name"], None)]
    local = "".join(f"<p>{html.escape(x)}</p>" for x in z["local"])
    cards = "".join(T.product_card(BY_SLUG[s], R) for s in z["products"] if s in BY_SLUG)
    others = [(f"zone/{s}.html", n) for s, n in ZONE_LINKS if s != z["slug"]]
    wa = f"Bună Marina, sunt din {z['name']} și vreau informații despre o asigurare."
    body = f"""
  <section class="page-hero"><div class="container">{crumbs_html(crumbs, R)}<h1>{html.escape(z['h1'])}</h1><p class="lead">{html.escape(z['answer'])}</p>
    <div class="cta-row"><a href="{T.wa_link(wa)}" class="btn btn-wa" target="_blank" rel="noopener">{T.WA_SVG}<span>Scrie pe WhatsApp</span></a><a href="{R}asigurari/" class="btn btn-primary">Vezi asigurările</a></div></div></section>
  <div class="container prose"><h2>Asigurări pentru {html.escape(z['name'])}: ce contează local</h2>{local}
    <h2>Cele mai cerute asigurări în {html.escape(z['name'])}</h2><div class="grid">{cards}</div>
    {T.faq_block([tuple(x) for x in z['faq']])}
    <p>Oriunde ai fi în România, cumperi online pe platforma brokerului, iar Marina răspunde pe WhatsApp. Întâlnirile față în față se fac la Iași, cu programare.</p>
    {T.related_block("Alte zone", others, R)}{author_box(R)}</div>"""
    service = {"@context": "https://schema.org", "@type": "Service", "name": f"Asigurări {z['name']}",
               "serviceType": "Intermediere asigurări", "provider": {"@id": T.AGENCY_ID},
               "areaServed": {"@type": "City", "name": z["name"], "containedInPlace": {"@type": "AdministrativeArea", "name": f"Județul {z['county']}"}},
               "url": T.SITE + path}
    return T.page(z["title"], z["desc"], path, [service, T.faqpage([tuple(x) for x in z["faq"]]), T.breadcrumb(crumbs)], R, body, wa)
```

În `build()`: `for z in ZONES: write(root, f"/zone/{z['slug']}.html", render_zone(z))`.

- [ ] **Step 5: Rulează → PASS**; `check_site.py --no-links` → 0 probleme.

- [ ] **Step 6: Commit**

```bash
git add content/zones.json build.py tests/test_build.py zone/
git commit -m "content: 9 pagini geo (Iași + Moldova)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6: Blog Markdown (12 articole) + index + articole recente pe homepage

**Files:**
- Create: `content/blog/*.md` (12), `blog/` (generat)
- Modify: `build.py` (`load_articles`, `render_article`, `render_blog_index`, populează `ARTICLES_BY_SLUG` și `LATEST_ARTICLES_HTML` înainte de homepage), `tests/test_build.py`

**Interfaces:**
- Produces: `build.load_articles() -> list[dict]` sortat descrescător după `date`; dict cu `slug, title, desc, date, updated, category, related_products, faq, html, words`. Frontmatter = bloc JSON între `---` la începutul fișierului (evităm dependența de YAML).

- [ ] **Step 1: Test**

```python
def test_articles_rendered_with_article_schema_and_author(out):
    arts = build.load_articles()
    assert len(arts) >= 12
    for a in arts:
        h = read(out, f"blog/{a['slug']}.html")
        assert h.count("<h1") == 1 and '"@type": "Article"' in h and '"@id": "https://iasiasigura.com/#marina"' in h
        assert "Actualizat:" in h and a["words"] >= 900, (a["slug"], a["words"])
    idx = read(out, "blog/index.html")
    assert idx.count('class="card article-card"') >= 12

def test_homepage_shows_three_latest_articles(out):
    h = read(out, "index.html")
    assert h.count('class="card article-card"') == 3
```

- [ ] **Step 2: Rulează → FAIL**

- [ ] **Step 3: Format articol** — `content/blog/pret-rca-2026-cum-se-calculeaza.md` (exemplu complet de frontmatter + structură; corpul se scrie la 900–1.500 cuvinte)

```markdown
---
{"title": "Cum se calculează prețul RCA în 2026: factorii care contează",
 "desc": "Ce influențează prima RCA în 2026: bonus-malus, vârsta șoferului, puterea motorului, județul, perioada. Explicat simplu, cu exemple.",
 "date": "2026-09-20", "updated": "2026-09-20", "category": "Auto",
 "related_products": ["rca", "casco"],
 "faq": [["De ce au prieteni prețuri diferite la RCA pentru aceeași mașină?", "Pentru că prima depinde de șofer (vârstă, clasa bonus-malus), de județ și de asigurător, nu doar de mașină."],
         ["Scade prețul dacă am mai multe clase de bonus?", "Da. Fiecare clasă de bonus reduce prima; la B8 reducerea este maximă."],
         ["Pot plăti RCA în rate?", "Unii asigurători permit plata în rate pentru polițele pe 12 luni; verifici opțiunea în platformă la cumpărare."]]}
---
**Pe scurt:** prețul RCA nu e „la stat” și nu e la fel pentru toți. Fiecare asigurător calculează prima după profilul tău de risc: mașina, tu ca șofer, județul și istoricul de daune. De aceea merită să compari ofertele înainte să cumperi.

## Ce factori influențează prima RCA?
...

## Cum funcționează clasa bonus-malus?
...

## Contează județul și mediul (urban/rural)?
...

## Perioada: 1 lună sau 12 luni?
...

## Cum obții cel mai bun preț fără să pierzi acoperiri?
...
```

Reguli pentru corp: prima linie bold „Pe scurt:” = răspuns direct (40–60 cuvinte); H2 sub formă de întrebare; fără H1 în Markdown (îl pune generatorul); fără prețuri concrete; ultimul H2 = „Ce faci mai departe” cu link către produsul conex (`../asigurari/<slug>.html`).

Lista celor 12 articole (slug · titlu · categorie · related_products · unghiul):
1. `pret-rca-2026-cum-se-calculeaza` · Cum se calculează prețul RCA în 2026 · Auto · rca, casco · factorii de tarifare, comparare
2. `bonus-malus-explicat` · Bonus-malus explicat: clasele B0–B8 și M1–M8 · Auto · rca · cum urci/cobori, transfer la schimbarea mașinii, verificare istoric
3. `rca-sau-casco-diferente` · RCA sau CASCO? Ce acoperă fiecare și când ai nevoie de ambele · Auto · rca, casco · cazuri concrete (parcare, grindină, furt)
4. `pad-asigurare-obligatorie-locuinta` · PAD: asigurarea obligatorie a locuinței, explicată · Locuință · pad, locuinta · cine e obligat, riscuri, amenzi, cum se face online
5. `asigurare-locuinta-ce-acopera` · Ce acoperă asigurarea facultativă de locuință (și ce nu) · Locuință · locuinta, pad · inundație de la vecini, bunuri, răspundere, credit
6. `asigurare-calatorie-grecia-turcia` · Asigurare de călătorie pentru Grecia, Turcia, Bulgaria: ce trebuie să știi · Călătorie · calatorie, storno · EHIC vs privată, sume, sporturi, copii
7. `malpraxis-asistent-medical-rezident` · Asigurarea de malpraxis pentru rezidenți și asistenți medicali · Sănătate · malpraxis, raspundere-civila · cine e obligat, limite, ce acoperă, cum se cumpără online
8. `asigurare-bolt-uber-iasi` · Șofer Bolt sau Uber în Iași: ce asigurări îți trebuie · Auto · taxi-uber-bolt, rca, casco · autorizare, accidente pasageri, RCA cu utilizare comercială
9. `rotr-ce-este-si-cine-are-nevoie` · ROTR: ce este, cine are nevoie și cum se obține · Firme · rotr, cargo-cmr · licența ARR, sume, acte
10. `pilon-3-pensie-privata-merita` · Pilonul III: merită pensia privată facultativă? · Viață · pensii-private, viata · deductibilitate, randament, retragere, angajator
11. `asigurare-sanatate-privata-vs-cas` · Asigurare de sănătate privată vs CAS: ce primești în plus · Sănătate · sanatate, viata · acces clinici, spitalizare, preexistente, firmă
12. `ce-asigurari-ii-trebuie-unui-pfa-sau-imm` · Ce asigurări îi trebuie unui PFA sau unei firme mici · Firme · imm, raspundere-civila, cargo-cmr · obligatorii vs recomandate, pe tip de activitate

- [ ] **Step 4: Cod în `build.py`**

```python
import re, markdown

BLOG_DIR = os.path.join(CONTENT, "blog")

def load_articles():
    arts = []
    for f in sorted(os.listdir(BLOG_DIR)):
        if not f.endswith(".md"): continue
        raw = open(os.path.join(BLOG_DIR, f), encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m: raise SystemExit(f"{f}: frontmatter lipsă")
        meta, body = json.loads(m.group(1)), m.group(2)
        meta["slug"] = f[:-3]
        meta["html"] = markdown.markdown(body, extensions=["tables"])
        meta["words"] = len(re.sub(r"<[^>]+>", " ", meta["html"]).split())
        meta.setdefault("updated", meta["date"])
        arts.append(meta)
    return sorted(arts, key=lambda a: a["date"], reverse=True)

RO_MONTHS = ["ianuarie","februarie","martie","aprilie","mai","iunie","iulie","august","septembrie","octombrie","noiembrie","decembrie"]
def ro_date(iso):
    y, m, d = iso.split("-"); return f"{int(d)} {RO_MONTHS[int(m)-1]} {y}"

def article_card(a, R):
    return (f'<a class="card article-card" href="{R}blog/{a["slug"]}.html"><time datetime="{a["updated"]}">{a["category"]} · {ro_date(a["updated"])}</time>'
            f'<h3>{html.escape(a["title"])}</h3><p>{html.escape(a["desc"])}</p></a>')

def render_article(a, all_articles):
    R = "../"; path = f"/blog/{a['slug']}.html"
    crumbs = [("Acasă", "/"), ("Blog", "/blog/"), (a["title"], None)]
    rel_products = [(f"asigurari/{s}.html", BY_SLUG[s]["name"]) for s in a.get("related_products", []) if s in BY_SLUG]
    others = [x for x in all_articles if x["slug"] != a["slug"] and x["category"] == a["category"]][:3] or [x for x in all_articles if x["slug"] != a["slug"]][:3]
    faq = [tuple(x) for x in a.get("faq", [])]
    body = f"""
  <section class="page-hero"><div class="container container-narrow">{crumbs_html(crumbs, R)}<h1>{html.escape(a['title'])}</h1>
    <p class="article-meta">De <a href="{R}despre.html">{T.P['name']}</a>, {T.P['job_title'].lower()} · Publicat: {ro_date(a['date'])} · Actualizat: {ro_date(a['updated'])}</p></div></section>
  <article class="container container-narrow prose">{a['html']}{T.faq_block(faq) if faq else ''}
    {T.related_block("Asigurările despre care e vorba", rel_products, R)}{author_box(R)}
    <h2>Citește și</h2><div class="grid">{"".join(article_card(x, R) for x in others)}</div></article>"""
    node = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
            "datePublished": a["date"], "dateModified": a["updated"], "inLanguage": "ro-RO",
            "author": {"@id": T.PERSON_ID}, "publisher": {"@id": T.AGENCY_ID},
            "mainEntityOfPage": T.SITE + path, "image": T.SITE + "/assets/og-articol.png", "wordCount": a["words"]}
    jsonld = [node, T.breadcrumb(crumbs)] + ([T.faqpage(faq)] if faq else [])
    wa = f"Bună Marina, am citit articolul „{a['title']}” și am o întrebare."
    return T.page(a["title"][:60] if len(a["title"]) <= 60 else a["title"][:57].rsplit(" ", 1)[0] + "…", a["desc"], path, jsonld, R, body, wa, og_image="/assets/og-articol.png", og_type="article")

def render_blog_index(arts):
    R = "../"; crumbs = [("Acasă", "/"), ("Blog", None)]
    cards = "".join(article_card(a, R) for a in arts)
    body = f"""<section class="page-hero"><div class="container">{crumbs_html(crumbs, R)}<h1>Ghiduri de asigurări, pe înțelesul tău</h1>
    <p class="lead">Articole scrise de Marina Metzak: ce acoperă fiecare asigurare, ce nu, și cum alegi fără să plătești degeaba. Actualizate periodic.</p></div></section>
  <section><div class="container"><div class="grid">{cards}</div></div></section>"""
    return T.page("Blog: ghiduri de asigurări explicate simplu | IașiAsigură",
                  "Ghiduri despre RCA, CASCO, locuință, PAD, călătorie, sănătate, malpraxis, pensii și asigurări pentru firme, scrise de un asistent în brokeraj.",
                  "/blog/", [T.breadcrumb(crumbs)], R, body, WA_DEFAULT)
```

Reordonează `build()`:
```python
def build(root=ROOT):
    WRITTEN.clear()
    arts = load_articles()
    ARTICLES_BY_SLUG.clear(); ARTICLES_BY_SLUG.update({a["slug"]: a for a in arts})
    LATEST_ARTICLES_HTML[0] = "".join(article_card(a, "") for a in arts[:3])
    write(root, "/index.html", render_home())
    write(root, "/asigurari/index.html", render_catalog())
    for p in PRODUCTS: write(root, f"/asigurari/{p['slug']}.html", render_product(p, ARTICLES_BY_SLUG))
    for z in ZONES: write(root, f"/zone/{z['slug']}.html", render_zone(z))
    write(root, "/blog/index.html", render_blog_index(arts))
    for a in arts: write(root, f"/blog/{a['slug']}.html", render_article(a, arts))
    return list(WRITTEN)
```

- [ ] **Step 5: Scrie cele 12 articole** în `content/blog/`, 900–1.500 cuvinte fiecare, după formatul de la Step 3. Verifică `words` cu: `python3 -c "import build; [print(a['slug'], a['words']) for a in build.load_articles()]"`.

- [ ] **Step 6: Rulează → PASS**; `check_site.py --no-links` → 0 probleme.

- [ ] **Step 7: Commit**

```bash
git add content/blog build.py tests/test_build.py blog/ index.html asigurari/
git commit -m "content: blog cu 12 articole SEO/AEO + index + recente pe homepage

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: Pagini statice (Despre, Contact, Termeni, Confidențialitate, Cookies, 404) + robots, sitemap, llms.txt + eliminarea `--no-links`

**Files:**
- Create: `content/pages/{despre,contact,termeni,confidentialitate,cookies}.html`, `content/pages/meta.json`
- Modify: `build.py` (`render_static`, `render_404`, `render_sitemap`, `render_robots`, `render_llms`), `tests/test_build.py`, `scripts/check_site.py` (fără schimbări de cod; doar testul scoate `--no-links`)

**Interfaces:**
- `content/pages/meta.json`: `{ "despre": {"title": "...", "desc": "...", "h1": "..."}, ... }`. Fragmentele HTML conțin doar corpul (fără H1; îl pune generatorul din meta).

- [ ] **Step 1: Test**

```python
def test_static_pages_and_technical_files(out):
    for p in ["despre", "contact", "termeni", "confidentialitate", "cookies"]:
        assert read(out, f"{p}.html").count("<h1") == 1
    assert "RAF 160354" in read(out, "despre.html") and "programare" in read(out, "contact.html")
    assert read(out, "404.html").count("<h1") == 1
    robots = read(out, "robots.txt"); assert "GPTBot" in robots and "ClaudeBot" in robots and "Sitemap: https://iasiasigura.com/sitemap.xml" in robots
    sm = read(out, "sitemap.xml"); assert sm.count("<url>") >= 40 and "<lastmod>" in sm and "404" not in sm
    llms = read(out, "llms.txt"); assert llms.startswith("# IașiAsigură") and "/asigurari/rca.html" in llms

def test_check_site_passes_with_links(out):
    r = subprocess.run([sys.executable, "scripts/check_site.py", str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
```
Șterge `test_check_site_passes` (varianta cu `--no-links`) din Task 3.

- [ ] **Step 2: Rulează → FAIL**

- [ ] **Step 3: Conținut `content/pages/`**

`meta.json`:
```json
{
 "despre": {"title": "Despre Marina Metzak, asistent în brokeraj | IașiAsigură", "desc": "Cine este Marina Metzak: asistent în brokeraj înregistrat la ASF (RAF 160354), în numele Destine Broker. Cum lucrează, ce asigurări face, cum o contactezi.", "h1": "Marina Metzak: asistent în brokeraj, înregistrat la ASF"},
 "contact": {"title": "Contact: WhatsApp, telefon, e-mail | IașiAsigură", "desc": "Scrie-i Marinei pe WhatsApp la +40 752 205 206 sau pe e-mail la contact@iasiasigura.com. Întâlniri la Iași, Bd. Metalurgiei 4, doar cu programare.", "h1": "Contact"},
 "termeni": {"title": "Termeni și condiții | IașiAsigură", "desc": "Termenii de utilizare ai site-ului iasiasigura.com: rol informativ, redirecționare către platforma brokerului, răspundere, drepturi de autor.", "h1": "Termeni și condiții"},
 "confidentialitate": {"title": "Politica de confidențialitate | IașiAsigură", "desc": "Cum sunt tratate datele personale: site-ul nu colectează date; WhatsApp și platforma brokerului au propriile politici. Drepturile tale GDPR.", "h1": "Politica de confidențialitate"},
 "cookies": {"title": "Politica de cookies | IașiAsigură", "desc": "Site-ul iasiasigura.com nu setează cookie-uri proprii și folosește analiză de trafic fără cookie-uri.", "h1": "Politica de cookies"}
}
```

`despre.html` (corp): poză (`assets/marina.webp`, `TODO-MARINA`), paragraf „Pe scurt” (cine e, RAF, broker, din ce an), secțiuni H2: „Cum lucrez” (online, WhatsApp, întâlnire cu programare), „Ce asigurări fac” (linkuri către toate cele 16), „Cum verifici că sunt înregistrată la ASF” (pași + link registru), „Ce spun clienții” (testimonialele din `home.json`), CTA WhatsApp. JSON-LD: `person_node()` + `breadcrumb`.

`contact.html` (corp): trei carduri (WhatsApp cu link, telefon `tel:`, e-mail `mailto:`), program (`TODO-MARINA: L–V 9–18`), adresă + „doar cu programare”, hartă ca link extern spre Google Maps (`https://maps.google.com/?q=Bd.+Metalurgiei+4+Iași`), fără iframe. JSON-LD: `agency_node()` + `breadcrumb`.

`termeni.html`: 1) Cine operează site-ul (Marina Metzak, PFI, RAF, broker); 2) Rolul site-ului: informare și redirecționare, nu vânzare directă; contractele se încheie pe platforma brokerului sau cu asigurătorul; 3) Informațiile sunt generale, nu constituie consultanță personalizată; produsele efective sunt cele din documentele asigurătorului; 4) Linkuri externe; 5) Drepturi de autor; 6) Legea aplicabilă, ANPC/SOL.

`confidentialitate.html`: 1) Site-ul nu colectează și nu stochează date personale (fără formulare, fără conturi); 2) WhatsApp (Meta) și platforma smartsales (BrokerNet/Destine Broker) au politici proprii, linkuri; 3) Analiză de trafic: Cloudflare Web Analytics, fără cookie-uri, fără identificatori; 4) Drepturi GDPR (acces, ștergere, opoziție) și cum le exerciți: `contact@iasiasigura.com`; 5) Datele transmise pe WhatsApp pentru ofertă sunt folosite doar pentru ofertare/emitere și șterse la cerere.

`cookies.html`: site-ul nu setează cookie-uri proprii; nu există banner pentru că nu e necesar; linkurile externe pot seta cookie-uri pe domeniile lor.

- [ ] **Step 4: Cod în `build.py`**

```python
PAGES_META = load_json("pages/meta.json")

def render_static(key):
    R = ""; m = PAGES_META[key]; path = f"/{key}.html"
    frag = open(os.path.join(CONTENT, "pages", f"{key}.html"), encoding="utf-8").read()
    crumbs = [("Acasă", "/"), (m["h1"], None)]
    body = f"""<section class="page-hero"><div class="container container-narrow">{crumbs_html(crumbs, R)}<h1>{html.escape(m['h1'])}</h1></div></section>
  <div class="container container-narrow prose">{frag}</div>"""
    extra = {"despre": [T.person_node()], "contact": [T.agency_node()]}.get(key, [])
    return T.page(m["title"], m["desc"], path, extra + [T.breadcrumb(crumbs)], R, body, WA_DEFAULT)

def render_404():
    body = """<section class="page-hero"><div class="container container-narrow"><h1>Pagina nu există</h1><p class="lead">Poate ai nevoie de una dintre acestea:</p>
    <ul><li><a href="/asigurari/rca.html">Asigurare RCA</a></li><li><a href="/asigurari/locuinta.html">Asigurare locuință</a></li><li><a href="/asigurari/">Toate asigurările</a></li><li><a href="/blog/">Blog</a></li></ul></div></section>"""
    out = T.page("Pagina nu există | IașiAsigură", "Pagina căutată nu există. Vezi asigurările disponibile sau scrie pe WhatsApp.", "/404.html", [], "", body, WA_DEFAULT)
    return out.replace('content="index, follow,', 'content="noindex, follow,')

def render_sitemap(paths, root):
    today = datetime.date.today().isoformat()
    urls = []
    for p in paths:
        if p.endswith("404.html"): continue
        loc = T.SITE + (p[:-len("index.html")] if p.endswith("index.html") else p)
        src_mtime = datetime.date.fromtimestamp(os.path.getmtime(os.path.join(root, p.lstrip("/")))).isoformat()
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{src_mtime or today}</lastmod></url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"

def render_robots():
    bots = ["*", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "PerplexityBot", "Google-Extended", "CCBot", "Bingbot"]
    return "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {T.SITE}/sitemap.xml\n"

def render_llms(arts):
    P = T.P
    lines = [f"# {T.S['brand']}", "", f"> Site de prezentare al {P['name']}, {P['job_title'].lower()} (cod RAF {P['raf']}) înregistrat la ASF, în numele {T.S['broker']['name']} ({T.S['broker']['rbk']}). Asigurări online pentru toată România; întâlniri la Iași cu programare. Contact: WhatsApp {P['phone_display']}, {P['email']}.", "",
             "Site-ul nu afișează prețuri; cumpărarea se face pe platforma brokerului (metzak-marina.smartsales.ro). Serviciul e gratuit pentru client: comisionul e plătit de asigurător.", "", "## Asigurări"]
    lines += [f"- [{p['name']}]({T.SITE}/asigurari/{p['slug']}.html): {p['short']} ({'cumpărare online' if p['type']=='online' else 'ofertă personalizată pe WhatsApp'})" for p in PRODUCTS]
    lines += ["", "## Zone"] + [f"- [Asigurări {n}]({T.SITE}/zone/{s}.html)" for s, n in ZONE_LINKS]
    lines += ["", "## Articole"] + [f"- [{a['title']}]({T.SITE}/blog/{a['slug']}.html): {a['desc']}" for a in arts]
    lines += ["", "## Despre", f"- [Despre Marina]({T.SITE}/despre.html)", f"- [Contact]({T.SITE}/contact.html)", ""]
    return "\n".join(lines)
```

În `build()` după articole:
```python
    for k in PAGES_META: write(root, f"/{k}.html", render_static(k))
    write(root, "/404.html", render_404())
    write(root, "/robots.txt", render_robots())
    write(root, "/llms.txt", render_llms(arts))
    write(root, "/sitemap.xml", render_sitemap([p for p in WRITTEN if p.endswith(".html")], root))
```

- [ ] **Step 5: Rulează → PASS**; `python3 build.py && python3 scripts/check_site.py --online` → 0 probleme, toate URL-urile smartsales HTTP 200.

- [ ] **Step 6: Commit**

```bash
git add content/pages build.py tests/test_build.py *.html robots.txt sitemap.xml llms.txt
git commit -m "feat: pagini statice, 404, robots, sitemap, llms.txt

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 8: Imagini OG, logo PNG, apple-touch-icon, placeholder poză Marina

**Files:**
- Create: `assets/og-default.svg`, `assets/og-produs.svg`, `assets/og-articol.svg`, `assets/og-default.png`, `assets/og-produs.png`, `assets/og-articol.png`, `assets/logo.png`, `assets/apple-touch-icon.png`, `assets/marina.webp` (placeholder până la poza reală), `scripts/render_assets.sh`

- [ ] **Step 1: SVG-uri OG 1200×630** (fundal navy, „Ia” în pătrat galben, titlu mare, subtitlu)

`assets/og-default.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#0b2545"/><rect x="80" y="120" width="160" height="160" rx="36" fill="#f5b301"/><text x="160" y="235" font-family="system-ui,Arial,sans-serif" font-size="96" font-weight="800" text-anchor="middle" fill="#0b2545">Ia</text><text x="280" y="215" font-family="system-ui,Arial,sans-serif" font-size="92" font-weight="800" fill="#fff">Iași<tspan fill="#f5b301">Asigură</tspan></text><text x="80" y="400" font-family="system-ui,Arial,sans-serif" font-size="56" font-weight="700" fill="#fff">Ia și asigură!</text><text x="80" y="470" font-family="system-ui,Arial,sans-serif" font-size="34" fill="#cfd8e6">Asigurări online în toată România, cu o persoană reală pe WhatsApp</text><text x="80" y="560" font-family="system-ui,Arial,sans-serif" font-size="28" fill="#f5b301">Marina Metzak · asistent în brokeraj · RAF 160354</text></svg>
```
`og-produs.svg` = același, cu al doilea text „Cumperi online sau ceri ofertă pe WhatsApp”. `og-articol.svg` = „Ghiduri de asigurări explicate simplu”.

- [ ] **Step 2: `scripts/render_assets.sh`** (PNG din SVG; pe macOS folosește `qlmanage` dacă `rsvg-convert` lipsește)

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../assets"
render() { # $1=svg $2=png $3=width
  if command -v rsvg-convert >/dev/null; then rsvg-convert -w "$3" "$1" -o "$2";
  else qlmanage -t -s "$3" -o . "$1" >/dev/null 2>&1 && mv "$1.png" "$2"; fi
  echo "ok: $2"; }
render og-default.svg og-default.png 1200
render og-produs.svg og-produs.png 1200
render og-articol.svg og-articol.png 1200
render logo.svg logo.png 840
render favicon.svg apple-touch-icon.png 180
```
Run: `chmod +x scripts/render_assets.sh && scripts/render_assets.sh`. Verifică cu `sips -g pixelWidth assets/og-default.png` → 1200.

- [ ] **Step 3: Placeholder `assets/marina.webp`** — un SVG cu inițialele „MM” pe fundal navy, 300×300, convertit la PNG cu `render`, apoi `sips -s format webp` nu există pe macOS; folosește `cwebp` dacă e instalat (`brew install webp`), altfel salvează `marina.png` și schimbă `image` în `site.json` și `author_box` la `.png`. Notează în README că poza reală înlocuiește fișierul cu același nume, 600×600, sub 80 KB.

- [ ] **Step 4: Rebuild + verificare** `python3 build.py && python3 scripts/check_site.py && python3 -m pytest -q`.

- [ ] **Step 5: Commit**

```bash
git add assets scripts/render_assets.sh content/site.json build.py
git commit -m "chore: imagini OG, logo PNG, apple-touch-icon, placeholder poză

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 9: README + verificare finală locală (Lighthouse, mobil) + push pe GitHub

**Files:**
- Create: `README.md`
- Modify: nimic altceva (doar corecturi dacă Lighthouse arată probleme)

- [ ] **Step 1: `README.md`** cu secțiunile: ce e site-ul; date fixe (tabelul din spec §2); structura repo; `pip3 install -r requirements.txt`; `python3 build.py`; `python3 scripts/check_site.py [--online]`; `python3 -m pytest`; „Cum adaugi un articol” (creezi `content/blog/<slug>.md` cu frontmatter JSON, rulezi build, commit); „Cum adaugi/modifici un produs” (`content/products.json`); „Cum actualizezi un articol” (schimbi `updated` doar după o revizuire reală); „Cum înlocuiești poza” (`assets/marina.webp`); „Publicare” (commit + push pe `main` → GitHub Pages); „Domeniu și DNS” (pașii din Task 10); „Ce NU facem” (prețuri, formulare, cookie-uri, logo Destine fără acord).

- [ ] **Step 2: Lighthouse local**

Run: `python3 -m http.server 8080` apoi, în alt terminal: `npx --yes lighthouse http://localhost:8080/ --preset=desktop --quiet --chrome-flags="--headless" --output=json --output-path=/tmp/lh-home.json && python3 -c "import json;d=json.load(open('/tmp/lh-home.json'))['categories'];print({k:round(v['score']*100) for k,v in d.items()})"`. Repetă cu `--form-factor=mobile --screenEmulation.mobile` (fără `--preset`) pentru `/`, `/asigurari/rca.html`, `/blog/pret-rca-2026-cum-se-calculeaza.html`.
Expected: toate categoriile ≥ 95 pe mobil. Dacă „Best practices” scade din cauza `http://localhost`, ignoră doar acel item.

- [ ] **Step 3: Test manual 375 px** pe homepage, `rca`, `imm`, `zone/iasi`, un articol: meniul se deschide/închide, butoanele CTA nu ies din ecran, FAQ se deschide, footer legal lizibil, buton flotant WhatsApp nu acoperă CTA-urile.

- [ ] **Step 4: Repo GitHub și push** (Alexandru creează repo-ul gol `alexandrumetzak/iasiasigura` pe GitHub sau confirmă alt nume)

```bash
git remote add origin git@github.com:alexandrumetzak/iasiasigura.git
git push -u origin main
```

- [ ] **Step 5: Commit README** (înainte de push, dacă nu a fost inclus)

```bash
git add README.md
git commit -m "docs: README cu instrucțiuni de conținut și publicare

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git push
```

---

### Task 10: Publicare: GitHub Pages, DNS Cloudflare, e-mail, Search Console, analytics (pași manuali, cu verificări)

Acești pași cer conturi ale lui Alexandru; Claude pregătește valorile și verifică rezultatul cu `dig`/`curl`.

- [ ] **Step 1: GitHub Pages** — Settings → Pages → Source: „Deploy from a branch”, `main` / `/ (root)`. Custom domain: `iasiasigura.com` (CNAME e deja în repo). Bifează „Enforce HTTPS” după ce DNS propagă.

- [ ] **Step 2: Cloudflare** — adaugă site-ul `iasiasigura.com` (plan Free), schimbă nameserverele la registrar. Înregistrări DNS (**proxy OFF / „DNS only”**, ca GitHub să emită certificatul):

```
A     @    185.199.108.153
A     @    185.199.109.153
A     @    185.199.110.153
A     @    185.199.111.153
AAAA  @    2606:50c0:8000::153
AAAA  @    2606:50c0:8001::153
AAAA  @    2606:50c0:8002::153
AAAA  @    2606:50c0:8003::153
CNAME www  alexandrumetzak.github.io
```

Verificare: `dig +short iasiasigura.com A` → cele 4 IP-uri; `curl -sI https://iasiasigura.com | head -1` → `HTTP/2 200`; `curl -sI https://www.iasiasigura.com | grep -i location` → `https://iasiasigura.com/`.

- [ ] **Step 3: Cloudflare Email Routing** — Email → Email Routing → Enable (adaugă automat MX + TXT SPF). Rule: `contact@iasiasigura.com` → Gmail-ul Marinei (`TODO-MARINA`), confirmă adresa de destinație din e-mailul primit. Test: trimite un e-mail la `contact@iasiasigura.com` și confirmă că ajunge. Notă: trimiterea *de pe* `contact@` se face din Gmail cu „Send mail as” (necesită SMTP; opțional, pasul se poate sări).

- [ ] **Step 4: Cloudflare Web Analytics** — Analytics & Logs → Web Analytics → Add site (`iasiasigura.com`). Copiază snippet-ul (`<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "..."}'></script>`), adaugă-l în `templates.footer()` înainte de `<script src="{R}js/script.js"`, rebuild, commit, push. Actualizează `content/pages/confidentialitate.html` dacă textul nu menționează deja Cloudflare Web Analytics.

- [ ] **Step 5: Google Search Console** — adaugă proprietatea `iasiasigura.com` (tip Domain), verificare prin TXT în Cloudflare DNS. Trimite `https://iasiasigura.com/sitemap.xml`. Cere indexare manuală pentru `/`, `/asigurari/rca.html`, `/despre.html`.

- [ ] **Step 6: Bing Webmaster Tools** — import din Search Console (un click). Bing alimentează ChatGPT search și Copilot.

- [ ] **Step 7: Rich Results Test** — `https://search.google.com/test/rich-results` pe `/`, `/asigurari/rca.html`, un articol. Expected: FAQ, Breadcrumb, Article detectate fără erori. Dacă apar avertismente pe `Person.image` din cauza placeholder-ului, se rezolvă când vine poza reală.

- [ ] **Step 8: Lighthouse pe domeniul live** (mobil) pe aceleași 3 pagini. Expected ≥ 95.

- [ ] **Step 9: Google Business Profile** (Marina, din contul ei Google): nume „IașiAsigură – Marina Metzak”, categorie „Agenție de asigurări”, tip „service-area business” cu zona Iași + județ, fără adresă publică, program, telefon +40 752 205 206, site `https://iasiasigura.com`, descriere (250 caractere din `home.json` lead). După verificare, adaugă link de recenzie în README și în șablonul WhatsApp de după emitere.

- [ ] **Step 10: Confirmare conformitate** — Alexandru trimite către Destine Broker (departamentul de conformitate) linkul site-ului + textul footer-ului legal și cere confirmare scrisă pentru: menționarea brokerului, cod RAF, eventuala folosire a logo-ului. Până la răspuns, site-ul rămâne live fără logo Destine (deja conform Global Constraints).

---

## Self-review

**Spec coverage:** §1 scop → toate; §2 date fixe → Task 1 `site.json`; §3 stack → Task 1–3, 9, 10; §4 URL-uri → Task 3–7; §5 produse (16, două tipuri, UTM, șablon pagină) → Task 2 `cta_block`, Task 4; §6 geo → Task 5; §7 blog (12, frontmatter, Article schema, `Actualizat`) → Task 6; §8 homepage → Task 3; §9 SEO/AEO (head, JSON-LD, robots cu boți AI, sitemap lastmod, llms.txt, interlinking, performanță, accesibilitate) → Task 1, 3, 7, 9; §10 design → Task 2 CSS; §11 legal (footer, termeni, confidențialitate, cookies, fără logo Destine) → Task 1 footer, Task 7; §12 structură repo/build idempotent → Task 3 (`build()` rescrie determinist; `lastmod` folosește mtime, deci a doua rulare nu schimbă output-ul HTML, doar sitemap-ul dacă fișierele au fost re-scrise: acceptat); §13 testare (build, check_links, h1/title/desc/canonical/JSON-LD, preview mobil, Lighthouse, deploy checks) → Task 3, 7, 9, 10; §14 plan achiziție → Task 10 Step 9 (GBP) + README; restul e în spec ca acțiuni umane; §15 out of scope → respectat.

**Placeholder scan:** singurele marcaje sunt `TODO-MARINA` (poză, bio, testimoniale, e-mail Gmail, program), cerute explicit de spec ca placeholder-e vizibile. Brief-urile de conținut (Task 4 tabel, Task 5 tabel, Task 6 listă) dau titlu, unghi, FAQ și legături; implementatorul scrie textul după exemplul complet din fiecare task.

**Type consistency:** `cta_block(p, R)`, `faq_block(faqs)`, `product_card(p, R)`, `related_block(title, items, R)`, `page(title, desc, path, jsonld, R, body, wa_text, og_image, og_type)` folosite identic în Task 3–7. `ZONE_LINKS`, `ARTICLES_BY_SLUG`, `LATEST_ARTICLES_HTML`, `BY_SLUG`, `PRODUCTS`, `ZONES`, `PAGES_META` definite la nivel de modul în `build.py` înainte de utilizare (`ZONE_LINKS` e definit după `render_home` în Task 3, dar e folosit doar la apel, nu la definire: ok). `author_box(R)` definit în Task 4, folosit în Task 5–6. `check_site.py` primește `--no-links` din Task 3 până la Task 7.
