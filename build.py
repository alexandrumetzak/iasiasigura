#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator IașiAsigură. Rulează: python3 build.py  (scrie HTML în rădăcina repo-ului)."""
import html, json, os, re, shutil, subprocess, sys, datetime
import markdown
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
ZONES = load_json("zones.json")
ZONE_LINKS = [(z["slug"], z["name"]) for z in ZONES]
PAGES_META = load_json("pages/meta.json")
STATIC = ["css", "js", "assets", "site.webmanifest"]
WRITTEN = []
LASTMOD = {}   # path generat -> data ISO a SURSEI (pentru sitemap; nu mtime-ul fișierului generat)
TODAY = datetime.date.today().isoformat()
_GIT_DATE_CACHE = {}

def source_date(path):
    """Data ultimului commit pentru o sursă din repo (YYYY-MM-DD).

    Folosită pentru <lastmod> în sitemap: derivă din sursă, nu din mtime-ul
    fișierului generat, ca două build-uri consecutive să dea același sitemap.
    Dacă git lipsește sau fișierul nu e urmărit, cade pe data de azi.
    """
    if path in _GIT_DATE_CACHE:
        return _GIT_DATE_CACHE[path]
    d = ""
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                           cwd=ROOT, capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            d = r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        d = ""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        d = TODAY
    _GIT_DATE_CACHE[path] = d
    return d

def write(root, path, content, lastmod=None):
    full = os.path.join(root, path.lstrip("/"))
    os.makedirs(os.path.dirname(full) or root, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    WRITTEN.append(path)
    LASTMOD[path] = lastmod or TODAY

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
    testi = testimonials_html()
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
  <section id="asigurari"><div class="container"><p class="eyebrow">Asigurări</p><h2>Ce asigurare îți trebuie?</h2>
    <p>Cele marcate <strong>Online</strong> le închei direct pe platforma brokerului. La cele cu <strong>Ofertă pe WhatsApp</strong> îmi scrii, iar eu cer ofertele, le compar și ți le trimit.</p>
    <div class="grid">{cards}</div></div></section>
  <section class="section-alt" id="de-ce"><div class="container"><p class="eyebrow">De ce prin intermediul meu</p><h2>Ce este diferit când lucrezi cu mine</h2><div class="grid">{why}</div></div></section>
  <section id="cum"><div class="container"><p class="eyebrow">Cum funcționează</p><h2>Ce ai de făcut</h2><div class="steps">{steps}</div></div></section>
  <section class="section-alt"><div class="container container-narrow">{T.faq_block(HOME['faq'])}</div></section>
  <section id="testimoniale"><div class="container"><p class="eyebrow">Clienți</p><h2>Ce spun clienții</h2><div class="grid">{testi}</div></div></section>
  <section class="section-alt" id="zone"><div class="container"><p class="eyebrow">Zone</p><h2>Unde lucrez</h2>
    <p>La Iași ne putem întâlni, cu programare. Cu clienții din restul țării lucrez pe WhatsApp și pe platforma brokerului, la fel de bine.</p><ul class="grid" style="list-style:none;padding:0">{zones}</ul></div></section>
  <section id="blog"><div class="container"><p class="eyebrow">Blog</p><h2>Articole despre întrebările pe care le primesc des</h2><div class="grid" id="home-articles">{LATEST_ARTICLES_HTML[0]}</div><p><a href="blog/">Toate articolele →</a></p></div></section>"""
    jsonld = [T.website_node(), T.agency_node(), T.person_node(), T.faqpage([tuple(x) for x in HOME["faq"]])]
    return T.page(HOME["title"], HOME["desc"], "/", jsonld, R, body, WA_DEFAULT)

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
    nots = "".join(f"<li>{html.escape(x)}</li>" for x in p.get("not_covers", []))
    nots_col = f'<div><h2>Ce nu acoperă</h2><ul class="cross">{nots}</ul></div>' if nots else ""
    docs = "".join(f"<li>{html.escape(x)}</li>" for x in p["docs"])
    steps = "".join(f'<div class="step"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for t, d in p["steps"])
    steps_title = "Cum o închei, pas cu pas" if p["type"] == "online" else "Cum ajungem la ofertă"
    rel_products = [(f"asigurari/{s}.html", BY_SLUG[s]["name"]) for s in p["related"] if s in BY_SLUG]
    rel_articles = [(f"blog/{s}.html", articles_by_slug[s]["title"]) for s in p.get("articles", []) if s in articles_by_slug]
    body = f"""
  <section class="page-hero"><div class="container">{crumbs_html(crumbs, R)}
    <h1>{html.escape(p['h1'])}</h1><p class="lead">{html.escape(p['answer'])}</p>{T.cta_block(p, R)}</div></section>
  <div class="container prose">
    <div class="two-col"><div><h2>Ce acoperă</h2><ul class="check">{covers}</ul></div>{nots_col}</div>
    <h2>Acte necesare</h2><ul>{docs}</ul>
    <h2>{steps_title}</h2><div class="steps">{steps}</div>
    {T.faq_block([tuple(x) for x in p['faq']])}
    {T.related_block("Asigurări conexe", rel_products, R)}{T.related_block("Citește și", rel_articles, R)}
    {author_box(R)}
    {T.cta_block(p, R)}
  </div>"""
    service = {"@context": "https://schema.org", "@type": "Service", "name": p["name"], "serviceType": p["service_type"],
               "provider": {"@id": T.AGENCY_ID}, "areaServed": {"@type": "Country", "name": "România"},
               "url": T.SITE + path, "description": p["answer"]}
    # agency_node primul, ca provider @id din Service să se rezolve pe pagină
    jsonld = [T.agency_node(), service, T.faqpage([tuple(x) for x in p["faq"]]), T.breadcrumb(crumbs)]
    return T.page(p["title"], p["desc"], path, jsonld, R, body, p["wa_text"], og_image="/assets/og-produs.png")

def render_catalog():
    R = "../"; path = "/asigurari/"
    pf = "".join(T.product_card(p, R) for p in PRODUCTS if "pf" in p["group"])
    pj = "".join(T.product_card(p, R) for p in PRODUCTS if "pj" in p["group"])
    crumbs = [("Acasă", "/"), ("Asigurări", None)]
    body = f"""
  <section class="page-hero"><div class="container">{crumbs_html(crumbs, R)}<h1>Toate asigurările</h1>
    <p class="lead">Cele marcate Online le închei direct pe platforma brokerului. La celelalte îmi scrii pe WhatsApp, iar eu cer ofertele, le compar și ți le trimit.</p></div></section>
  <section><div class="container"><h2>Pentru tine și familia ta</h2><div class="grid">{pf}</div></div></section>
  <section class="section-alt"><div class="container"><h2>Pentru firma ta</h2><div class="grid">{pj}</div></div></section>"""
    return T.page("Toate asigurările, online sau cu ofertă | IașiAsigură",
                  "Tot ce închei: RCA, CASCO, locuință, PAD, călătorie, sănătate, viață, pensii, malpraxis, răspundere civilă, taxi/Uber, ROTR, CMR, IMM, agricole.",
                  path, [T.breadcrumb(crumbs)], R, body, WA_DEFAULT)

# ---------------------------------------------------------------- ZONE
def render_zone(z):
    R = "../"; path = f"/zone/{z['slug']}.html"
    crumbs = [("Acasă", "/"), ("Zone", "/#zone"), (z["name"], None)]
    local = "".join(f"<p>{html.escape(x)}</p>" for x in z["local"])
    cards = "".join(T.product_card(BY_SLUG[s], R) for s in z["products"] if s in BY_SLUG)
    others = [(f"zone/{s}.html", n) for s, n in ZONE_LINKS if s != z["slug"]]
    wa = f"Bună Marina, sunt din {z['name']} și vreau informații despre o asigurare."
    outro = f"<p>{html.escape(z['outro'])}</p>" if z.get("outro") else ""
    body = f"""
  <section class="page-hero"><div class="container">{crumbs_html(crumbs, R)}<h1>{html.escape(z['h1'])}</h1><p class="lead">{html.escape(z['answer'])}</p>
    <div class="cta-row"><a href="{T.wa_link(wa)}" class="btn btn-wa" target="_blank" rel="noopener">{T.WA_SVG}<span>Scrie pe WhatsApp</span></a><a href="{R}asigurari/" class="btn btn-primary">Vezi asigurările</a></div></div></section>
  <div class="container prose"><h2>Ce contează la asigurări în {html.escape(z['name'])}</h2>{local}
    <h2>Cele mai cerute asigurări în {html.escape(z['name'])}</h2><div class="grid">{cards}</div>
    {T.faq_block([tuple(x) for x in z['faq']])}
    {outro}
    {T.related_block("Alte zone", others, R)}{author_box(R)}</div>"""
    service = {"@context": "https://schema.org", "@type": "Service", "name": f"Asigurări {z['name']}",
               "serviceType": "Intermediere asigurări", "provider": {"@id": T.AGENCY_ID},
               "areaServed": {"@type": "City", "name": z["name"], "containedInPlace": {"@type": "AdministrativeArea", "name": f"Județul {z['county']}"}},
               "url": T.SITE + path}
    # agency_node primul, ca provider @id din Service să se rezolve pe pagină
    jsonld = [T.agency_node(), service, T.faqpage([tuple(x) for x in z["faq"]]), T.breadcrumb(crumbs)]
    return T.page(z["title"], z["desc"], path, jsonld, R, body, wa,
                  geo_region=z["geo_region"], geo_placename=z["name"])


# ---------------------------------------------------------------- BLOG
BLOG_DIR = os.path.join(CONTENT, "blog")

def load_articles():
    arts = []
    for f in sorted(os.listdir(BLOG_DIR)):
        if not f.endswith(".md"): continue
        raw = open(os.path.join(BLOG_DIR, f), encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m: raise SystemExit(f"{f}: frontmatter lipsă")
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{f}: frontmatter JSON invalid: {e}")
        if "date" not in meta:
            raise SystemExit(f"{f}: frontmatter fără 'date'")
        body = m.group(2)
        meta["slug"] = f[:-3]
        meta["html"] = markdown.markdown(body, extensions=["tables"])
        meta["words"] = len(re.sub(r"<[^>]+>", " ", meta["html"]).split())
        meta.setdefault("updated", meta["date"])
        arts.append(meta)
    return sorted(arts, key=lambda a: a["date"], reverse=True)

RO_MONTHS = ["ianuarie","februarie","martie","aprilie","mai","iunie","iulie","august","septembrie","octombrie","noiembrie","decembrie"]

def ro_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {RO_MONTHS[int(m)-1]} {y}"

def article_card(a, R):
    return (f'<a class="card article-card" href="{R}blog/{a["slug"]}.html"><time datetime="{a["updated"]}">{a["category"]} · {ro_date(a["updated"])}</time>'
            f'<h3>{html.escape(a["title"])}</h3><p>{html.escape(a["desc"])}</p></a>')

def render_article(a, all_articles):
    R = "../"; path = f"/blog/{a['slug']}.html"
    crumbs = [("Acasă", "/"), ("Blog", "/blog/"), (a["title"], None)]
    rel_products = [(f"asigurari/{s}.html", BY_SLUG[s]["name"]) for s in a.get("related_products", []) if s in BY_SLUG]
    same = [x for x in all_articles if x["slug"] != a["slug"] and x["category"] == a["category"]]
    rest = [x for x in all_articles if x["slug"] != a["slug"] and x["category"] != a["category"]]
    others = (same + rest)[:3]
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
    return T.page(a["title"][:60] if len(a["title"]) <= 60 else a["title"][:57].rsplit(" ", 1)[0] + "…", a["desc"], path, jsonld, R, body, wa,
                  og_image="/assets/og-articol.png", og_type="article")

def render_blog_index(arts):
    R = "../"; crumbs = [("Acasă", "/"), ("Blog", None)]
    cards = "".join(article_card(a, R) for a in arts)
    body = f"""<section class="page-hero"><div class="container">{crumbs_html(crumbs, R)}<h1>Blog: răspunsuri la întrebările despre asigurări</h1>
    <p class="lead">Scriu aici răspunsurile pe care le dau des pe WhatsApp: ce acoperă o asigurare, ce nu acoperă și când nu are rost să plătești pentru ea. Le actualizez când se schimbă ceva.</p></div></section>
  <section><div class="container"><div class="grid">{cards}</div></div></section>"""
    return T.page("Blog: ghiduri de asigurări explicate simplu | IașiAsigură",
                  "Ce am scris despre RCA, CASCO, locuință, PAD, călătorie, sănătate, malpraxis, pensii și asigurări pentru firme. Marina Metzak, asistent în brokeraj.",
                  "/blog/", [T.breadcrumb(crumbs)], R, body, WA_DEFAULT)

# ---------------------------------------------------------------- PAGINI STATICE
def testimonials_html():
    return "".join(f'<blockquote class="testimonial"><p>{html.escape(q)}</p><cite>{html.escape(w)}</cite></blockquote>'
                   for q, w in HOME["testimonials"])

def fill_tokens(frag, key):
    """Înlocuiește tokenurile {{...}} din fragmentele content/pages (fără motor de template)."""
    P = T.P
    repl = {"{{TESTIMONIALS}}": testimonials_html(), "{{WA_LINK}}": T.wa_link(WA_DEFAULT),
            "{{PHONE}}": P["phone_display"], "{{PHONE_E164}}": P["phone_e164"],
        "{{EMAIL}}": P["email"],
            "{{RAF}}": P["raf"], "{{BROKER}}": T.S["broker"]["name"], "{{ASF_REGISTRY}}": T.S["links"]["asf_registry"],
            "{{SMARTSALES_TERMS}}": T.smartsales_url("/privacy/terms", "legal")}
    for k, v in repl.items():
        frag = frag.replace(k, v)
    rest = re.findall(r"\{\{[^}]+\}\}", frag)
    if rest:
        raise SystemExit(f"pages/{key}.html: tokenuri necunoscute: {sorted(set(rest))}")
    return frag

def render_static(key):
    R = ""; m = PAGES_META[key]; path = f"/{key}.html"
    with open(os.path.join(CONTENT, "pages", f"{key}.html"), encoding="utf-8") as f:
        frag = fill_tokens(f.read(), key)
    crumbs = [("Acasă", "/"), (m["h1"], None)]
    body = f"""<section class="page-hero"><div class="container container-narrow">{crumbs_html(crumbs, R)}<h1>{html.escape(m['h1'])}</h1></div></section>
  <div class="container container-narrow prose">{frag}</div>"""
    extra = {"despre": [T.person_node()], "contact": [T.agency_node()]}.get(key, [])
    return T.page(m["title"], m["desc"], path, extra + [T.breadcrumb(crumbs)], R, body, WA_DEFAULT)

def render_404():
    body = """<section class="page-hero"><div class="container container-narrow"><h1>Pagina nu există</h1><p class="lead">Este posibil să fi fost mutată sau linkul să fie greșit. Paginile cele mai căutate:</p>
    <ul><li><a href="/asigurari/rca.html">Asigurare RCA</a></li><li><a href="/asigurari/locuinta.html">Asigurare locuință</a></li><li><a href="/asigurari/">Toate asigurările</a></li><li><a href="/blog/">Blog</a></li></ul></div></section>"""
    # R="/" — 404 e servit de pe orice cale, deci toate linkurile din head/header/footer trebuie absolute
    out = T.page("Pagina nu există | IașiAsigură", "Pagina nu există sau a fost mutată. Vezi asigurările sau scrie-mi pe WhatsApp.", "/404.html", [], "/", body, WA_DEFAULT)
    return out.replace('content="index, follow,', 'content="noindex, follow,')

# ---------------------------------------------------------------- FIȘIERE TEHNICE
def render_sitemap(paths):
    """<lastmod> vine din LASTMOD (data sursei), nu din mtime-ul fișierului generat."""
    urls = []
    for p in paths:
        if p.endswith("404.html"): continue
        loc = T.SITE + (p[:-len("index.html")] if p.endswith("index.html") else p)
        lastmod = LASTMOD.get(p, TODAY)
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"

def render_robots():
    bots = ["*", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "PerplexityBot", "Google-Extended", "CCBot", "Bingbot"]
    # sursele repo-ului ajung pe GitHub Pages odată cu output-ul generat; nu au ce căuta în index
    rules = "Allow: /\nDisallow: /content/\nDisallow: /docs/\nDisallow: /scripts/\nDisallow: /tests/\n"
    return "".join(f"User-agent: {b}\n{rules}\n" for b in bots) + f"Sitemap: {T.SITE}/sitemap.xml\n"

def render_llms(arts):
    P = T.P
    lines = [f"# {T.S['brand']}", "", f"> Site de prezentare: {P['name']}, {P['job_title'].lower()} (cod RAF {P['raf']}) înregistrat la ASF, în numele {T.S['broker']['name']} ({T.S['broker']['rbk']}). Asigurări online pentru toată România; întâlniri la Iași cu programare. Contact: WhatsApp {P['phone_display']}, {P['email']}.", "",
             "Site-ul nu afișează prețuri; cumpărarea se face pe platforma brokerului (metzak-marina.smartsales.ro). Serviciul e gratuit pentru client: comisionul e plătit de asigurător.", "", "## Asigurări"]
    lines += [f"- [{p['name']}]({T.SITE}/asigurari/{p['slug']}.html): {p['short']} ({'cumpărare online' if p['type']=='online' else 'ofertă pe WhatsApp'})" for p in PRODUCTS]
    lines += ["", "## Zone"] + [f"- [Asigurări {n}]({T.SITE}/zone/{s}.html)" for s, n in ZONE_LINKS]
    lines += ["", "## Articole"] + [f"- [{a['title']}]({T.SITE}/blog/{a['slug']}.html): {a['desc']}" for a in arts]
    lines += ["", "## Despre", f"- [Despre Marina]({T.SITE}/despre.html)", f"- [Contact]({T.SITE}/contact.html)", ""]
    return "\n".join(lines)

def copy_static(root):
    """La build în alt director (teste), copiază fișierele statice ca site-ul să fie complet."""
    if os.path.abspath(root) == ROOT: return
    for name in STATIC:
        src = os.path.join(ROOT, name)
        if not os.path.exists(src): continue
        dst = os.path.join(root, name)
        if os.path.isdir(src): shutil.copytree(src, dst, dirs_exist_ok=True)
        else: shutil.copy2(src, dst)

# ---------------------------------------------------------------- BUILD
def build(root=ROOT):
    WRITTEN.clear(); LASTMOD.clear()
    arts = load_articles()
    ARTICLES_BY_SLUG.clear(); ARTICLES_BY_SLUG.update({a["slug"]: a for a in arts})
    LATEST_ARTICLES_HTML[0] = "".join(article_card(a, "") for a in arts[:3])
    d_products = source_date("content/products.json")
    d_zones = source_date("content/zones.json")
    write(root, "/index.html", render_home(), lastmod=source_date("content/home.json"))
    write(root, "/asigurari/index.html", render_catalog(), lastmod=d_products)
    for p in PRODUCTS:
        write(root, f"/asigurari/{p['slug']}.html", render_product(p, ARTICLES_BY_SLUG), lastmod=d_products)
    for z in ZONES:
        write(root, f"/zone/{z['slug']}.html", render_zone(z), lastmod=d_zones)
    write(root, "/blog/index.html", render_blog_index(arts), lastmod=max(a["updated"] for a in arts))
    for a in arts:
        write(root, f"/blog/{a['slug']}.html", render_article(a, arts), lastmod=a["updated"])
    for k in PAGES_META:
        write(root, f"/{k}.html", render_static(k), lastmod=source_date(f"content/pages/{k}.html"))
    write(root, "/404.html", render_404())
    copy_static(root)
    write(root, "/.nojekyll", "")   # GitHub Pages: fără Jekyll (altfel content/blog/*.md ar fi randate)
    write(root, "/robots.txt", render_robots())
    write(root, "/llms.txt", render_llms(arts))
    write(root, "/sitemap.xml", render_sitemap([p for p in WRITTEN if p.endswith(".html")]))
    return list(WRITTEN)

if __name__ == "__main__":
    for p in build(ROOT if len(sys.argv) < 2 else sys.argv[1]):
        print("scris:", p)
