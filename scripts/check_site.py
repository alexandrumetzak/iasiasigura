#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifică output-ul generat. Folosire: python3 scripts/check_site.py [--online] [--no-links] [root]"""
import json, os, re, sys, urllib.request

ONLINE = "--online" in sys.argv
CHECK_LINKS = "--no-links" not in sys.argv
args = [a for a in sys.argv[1:] if a not in ("--online", "--no-links")]
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
        elif len(d) > 155: problems.append(f"{r}: description {len(d)} caractere")
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
        if CHECK_LINKS:
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
