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
    r = subprocess.run([sys.executable, "scripts/check_site.py", "--no-links", str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr

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

def test_related_and_faq_answers_are_safe(out):
    for p in build.PRODUCTS:
        assert len(p["related"]) == 3 and all(s in build.BY_SLUG for s in p["related"]), p["slug"]
        for _, a in p["faq"]:
            assert "<" not in a and "&" not in a, (p["slug"], a)
    for z in build.ZONES:
        assert all(s in build.BY_SLUG for s in z["products"]), z["slug"]
        assert len(z["faq"]) == 4, z["slug"]
        for _, a in z["faq"]:
            assert "<" not in a and "&" not in a, (z["slug"], a)


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
