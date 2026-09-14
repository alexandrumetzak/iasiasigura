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

# ---------------------------------------------------------------- PRODUSE
ARTICLES_BY_SLUG = {}  # populat în Task 6 (blog)

def author_box(R):
    P = T.P
    return f"""<div class="author-box"><img src="{R}assets/marina.webp" alt="{html.escape(P['name'])}" width="76" height="76" loading="lazy" />
      <div><strong>{P['name']}</strong>, {P['job_title'].lower()} (RAF {P['raf']})<br /><span class="article-meta">{html.escape(P['bio_short'])}</span><br /><a href="{R}despre.html">Despre Marina →</a></div></div>"""

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

# ---------------------------------------------------------------- BUILD
def build(root=ROOT):
    WRITTEN.clear()
    write(root, "/index.html", render_home())
    write(root, "/asigurari/index.html", render_catalog())
    for p in PRODUCTS:
        write(root, f"/asigurari/{p['slug']}.html", render_product(p, ARTICLES_BY_SLUG))
    return list(WRITTEN)

if __name__ == "__main__":
    for p in build(ROOT if len(sys.argv) < 2 else sys.argv[1]):
        print("scris:", p)
