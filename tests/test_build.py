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
