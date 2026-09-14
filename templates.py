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
    # „<" escapat ca \u003c: JSON-ul rămâne valid, dar un „</script>" dintr-o valoare
    # nu poate închide blocul și nu poate ieși din <script>.
    body = json.dumps(obj, ensure_ascii=False, indent=2).replace("<", "\\u003c")
    return ('<script type="application/ld+json">\n' + body + '\n</script>')

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
            "sameAs": [P["facebook"]]}

def website_node():
    return {"@context": "https://schema.org", "@type": "WebSite", "name": S["brand"], "url": SITE + "/",
            "inLanguage": "ro-RO", "publisher": {"@id": AGENCY_ID}}

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
      <a href="{wa}" class="btn btn-wa" target="_blank" rel="noopener">{WA_SVG}<span>Cere ofertă pe WhatsApp</span></a>
      <a href="{ss}" class="btn btn-ghost-dark" target="_blank" rel="noopener">Formular de ofertă pe platformă</a>
      <p class="cta-note">Produs cu ofertă personalizată: Marina compară asigurătorii și îți trimite oferta pe WhatsApp sau e-mail. Gratuit.</p>
    </div>"""

def faq_block(faqs, heading="Întrebări frecvente"):
    # Întrebarea e escapată; RĂSPUNSUL e inserat brut, intenționat, ca să permită
    # markup inline (<strong>, <a>) scris în content/. Siguranța e asigurată de
    # teste: test_related_and_faq_answers_are_safe verifică toate răspunsurile
    # din products.json, zones.json, home.json și din frontmatter-ul articolelor.
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

def head(title, desc, path, jsonld, R, og_image="/assets/og-default.png", og_type="website", geo_region="RO-IS", geo_placename="Iași"):
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
  <meta name="geo.region" content="{html.escape(geo_region)}" />
  <meta name="geo.placename" content="{html.escape(geo_placename)}" />
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
      <a href="{R}index.html" class="brand">
        <span class="brand-mark" aria-hidden="true">Ia</span>
        <span class="brand-text"><strong>Iași<em>Asigură</em></strong><span class="sr-only"> — </span><small>{S['tagline']}</small></span>
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
        <p>Asigurări online pentru toată România, cu o persoană reală pe WhatsApp: {P['name']}, {P['job_title'].lower()}.</p>
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

def page(title, desc, path, jsonld, R, body, wa_text, og_image="/assets/og-default.png", og_type="website", geo_region="RO-IS", geo_placename="Iași"):
    return (head(title, desc, path, jsonld, R, og_image, og_type, geo_region, geo_placename)
            + header(R, wa_text) + body + footer(R, wa_text))
