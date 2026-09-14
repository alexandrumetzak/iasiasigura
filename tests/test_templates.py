import json
import templates as T

RCA = {"slug": "rca", "name": "Asigurare RCA", "type": "online", "path": "/rca",
       "wa_text": "Bună Marina, vreau ofertă RCA.", "short": "Obligatorie pentru orice vehicul.", "icon": "🚗"}
IMM = {"slug": "imm", "name": "Asigurări IMM", "type": "consultanta", "path": "/home/asigurari#asigurariPj",
       "wa_text": "Bună Marina, vreau ofertă pentru firma mea.", "short": "Bunuri, răspundere, angajați.", "icon": "🏢"}

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

def test_ldjson_escapes_angle_bracket_so_script_cannot_break_out():
    s = T.ldjson({"a": "</script>"})
    inner = s.split(">", 1)[1].rsplit("<", 1)[0]
    assert "</script>" not in inner and "\\u003c" in inner
    assert json.loads(inner)["a"] == "</script>"

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

def test_cta_online_primary_is_smartsales_secondary_wa():
    h = T.cta_block(RCA, "../")
    assert 'class="btn btn-primary"' in h and "utm_campaign=rca" in h
    assert h.index("smartsales.ro") < h.index("wa.me")
    assert "Cumpără online" in h

def test_cta_consultanta_primary_is_wa_secondary_smartsales_form():
    h = T.cta_block(IMM, "../")
    assert h.index("wa.me") < h.index("smartsales.ro")
    assert "Cere ofertă pe WhatsApp" in h and "#asigurariPj" in h and "utm_campaign=imm" in h
    assert "Sau completezi datele pe platformă" in h and "Formular" not in h

def test_faq_block_uses_h3_questions():
    h = T.faq_block([("Cât durează?", "5 minute.")])
    assert "<h3>Cât durează?</h3>" in h and "5 minute." in h

def test_product_card_links_and_badge():
    h = T.product_card(RCA, "")
    assert 'href="asigurari/rca.html"' in h and "Online" in h
    assert "Ofertă pe WhatsApp" in T.product_card(IMM, "")

def test_related_block_renders_items_and_empty_returns_blank():
    h = T.related_block("Citește și", [("blog/x.html", "Articol <1>")], "../")
    assert '<aside class="related">' in h and "<h2>Citește și</h2>" in h
    assert 'href="../blog/x.html"' in h and "Articol &lt;1&gt;" in h
    assert T.related_block("Gol", [], "") == ""
