#!/usr/bin/env python3
"""Render a self-contained AliExpress listing HTML report from report.json."""
import argparse
import html
import json
import sys
from pathlib import Path

TEMPLATE_NAME = "report_template.html"

def esc(v):
    if v is None:
        return ""
    return html.escape(str(v), quote=True)

def desc_to_paragraphs(text):
    """Split a description string into paragraphs by newlines."""
    if not text:
        return []
    return [p.strip() for p in text.split("\n") if p.strip()]

def render_description_html(desc_foreign, desc_cn):
    """Build desc-section divs: foreign paragraphs first, divider, then CN paragraphs."""
    fp = desc_to_paragraphs(desc_foreign)
    cp = desc_to_paragraphs(desc_cn)
    parts = []
    if fp:
        en_inner = "".join(f'<p class="desc-en">{esc(p)}</p>' for p in fp)
        parts.append(f'<div class="desc-section">{en_inner}</div>')
    if cp:
        if parts:
            parts.append('<hr class="desc-divider">')
        cn_inner = "".join(f'<p class="desc-cn">{esc(p)}</p>' for p in cp)
        parts.append(f'<div class="desc-section">{cn_inner}</div>')
    if not parts:
        return '<div class="desc-section"><p class="desc-en">N/A</p></div>'
    return "".join(parts)

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def render(data, template):
    product = data.get("product", {})
    keywords = data.get("keywords", [])
    attrs = data.get("attributes", [])
    fabe = data.get("fabe", [])
    driver = data.get("conversion_driver", {})
    buyer = data.get("buyer_reason", {})
    ae_standard = data.get("aliexpress_standard", {})
    ae_geo = data.get("aliexpress_geo", {})
    consumer = data.get("consumer_insight", {})
    market = data.get("market", "North America")
    language = data.get("language", "English")
    assumptions = data.get("assumptions", [])

    # Attribute rows
    attr_rows = ""
    for i, a in enumerate(attrs, 1):
        src = a.get("source", "")
        src_class = src.split("/")[0].strip().replace(" ", "")
        src_label = src
        attr_rows += f'<tr><td>{i}</td><td class="cn">{esc(a.get("name_cn",""))}</td><td class="en">{esc(a.get("name_en",""))}</td><td class="cn">{esc(a.get("value_cn",""))}</td><td class="en">{esc(a.get("value_en",""))}</td><td><span class="src {src_class}">{esc(src_label)}</span></td></tr>\n'

    # Keyword rows
    kw_rows = ""
    for i, k in enumerate(keywords, 1):
        tier = k.get("tier", "")
        tier_class = tier.replace(" ", "")
        kw_rows += f'<tr><td>{i}</td><td class="en">{esc(k.get("keyword",""))}</td><td>{esc(k.get("score",""))}</td><td><span class="tier {tier_class}">{esc(tier)}</span></td><td class="en">{esc(k.get("placement",""))}</td></tr>\n'

    # FABE items
    fabe_html = ""
    for f in fabe:
        fabe_html += '<div class="fabe-item">'
        fabe_html += f'<div class="row"><span class="label f">F</span><span class="cn">{esc(f.get("feature_cn",""))}</span><span class="en">{esc(f.get("feature_en",""))}</span></div>'
        fabe_html += f'<div class="row"><span class="label a">A</span><span class="cn">{esc(f.get("advantage_cn",""))}</span><span class="en">{esc(f.get("advantage_en",""))}</span></div>'
        fabe_html += f'<div class="row"><span class="label b">B</span><span class="cn">{esc(f.get("benefit_cn",""))}</span><span class="en">{esc(f.get("benefit_en",""))}</span></div>'
        fabe_html += f'<div class="row"><span class="label e">E</span><span class="en">{esc(f.get("evidence",""))}</span></div>'
        fabe_html += '</div>\n'

    # Selling points
    sp_html = ""
    for sp in data.get("selling_points", []):
        sp_html += f'<li><span class="cn">{esc(sp.get("cn",""))}</span><span class="en">{esc(sp.get("en",""))}</span></li>\n'

    # AliExpress standard listing
    ae_title = ae_standard.get("title", "")
    ae_title_len = len(ae_title)
    ae_title_cn = ae_standard.get("title_cn", ae_standard.get("title_chinese", ""))

    # Item Specifics: two-column grid (foreign left, CN right)
    ae_specs_twocol = ""
    for s in ae_standard.get("item_specifics", []):
        en_val = esc(s.get("en", s.get("value_en", "")))
        cn_val = esc(s.get("cn", s.get("value_cn", "")))
        ae_specs_twocol += f'<div class="spec-row"><div class="spec-cell en">{en_val}</div><div class="spec-cell cn">{cn_val}</div></div>\n'
    if not ae_specs_twocol:
        ae_specs_twocol = '<div class="spec-row"><div class="spec-cell en">N/A</div><div class="spec-cell cn">N/A</div></div>'

    # Description: foreign paragraphs first, then CN paragraphs
    ae_description_html = render_description_html(
        ae_standard.get("description", ae_standard.get("description_en", "")),
        ae_standard.get("description_cn", "")
    )

    ae_sku_html = ""
    for s in ae_standard.get("sku", []):
        ae_sku_html += f'<tr><td>{esc(s.get("color",""))}</td><td>{esc(s.get("spec",""))}</td><td>{esc(s.get("price",""))}</td><td>{esc(s.get("stock",""))}</td></tr>\n'

    # GEO FAQ: split into foreign Q&A group and CN Q&A group
    geo_faq_en = ""
    geo_faq_cn = ""
    for q in ae_geo.get("faq", []):
        q_en = esc(q.get("q_en", q.get("q_foreign", "")))
        a_en = esc(q.get("a_en", q.get("a_foreign", "")))
        q_cn = esc(q.get("q_cn", ""))
        a_cn = esc(q.get("a_cn", ""))
        if q_en or a_en:
            geo_faq_en += f'<div class="qa"><div class="q"><span class="en">{q_en}</span></div><div class="a"><span class="en">{a_en}</span></div></div>\n'
        if q_cn or a_cn:
            geo_faq_cn += f'<div class="qa"><div class="q"><span class="cn">{q_cn}</span></div><div class="a"><span class="cn">{a_cn}</span></div></div>\n'
    if not geo_faq_en:
        geo_faq_en = '<div class="qa"><div class="q"><span class="en">N/A</span></div></div>'
    if not geo_faq_cn:
        geo_faq_cn = '<div class="qa"><div class="q"><span class="cn">N/A</span></div></div>'

    geo_nl_html = ""
    for n in ae_geo.get("natural_language", []):
        geo_nl_html += f'<span class="kw"><span class="en">{esc(n)}</span></span>\n'

    # Market / Language tag
    market_lang_tag = f"Market: {market} | Lang: {language}"

    # Consumer Insight HTML
    consumer_html = ""
    if consumer:
        consumer_html = '<div class="section">'
        consumer_html += '<h2><span class="cn">目标市场消费者分析</span> | Consumer Insight</h2>'
        consumer_html += '<div class="consumer-card">'
        for key, label_en in [
            ("target_persona", "Target Persona"),
            ("purchase_motivation", "Purchase Motivation"),
            ("cultural_preference", "Cultural Preference"),
            ("search_habits", "Search Habits"),
            ("competitive_landscape", "Competitive Landscape"),
            ("viral_potential", "Viral Potential"),
        ]:
            val = consumer.get(key, "")
            if not val:
                continue
            consumer_html += f'<div class="ccard"><strong>{label_en}</strong><span class="en">{esc(val)}</span></div>'
        consumer_html += '</div></div>'

    # Assumptions
    asump_html = ""
    for a in assumptions:
        asump_html += f'<li><span class="cn">{esc(a.get("cn",""))}</span><span class="en">{esc(a.get("en",""))}</span></li>\n'

    # Hero image
    hero = product.get("hero_image", "")
    hero_html = f'<img src="{esc(hero)}" alt="Product" />' if hero else '<div class="empty">No image</div>'

    repl = {
        "{{TITLE_CN}}": esc(product.get("title_cn", "")),
        "{{TITLE_EN}}": esc(product.get("title_en", "")),
        "{{HERO_IMAGE}}": hero_html,
        "{{OFFER_ID}}": esc(product.get("offer_id", "")),
        "{{PRICE}}": esc(product.get("price_text", "")),
        "{{MOQ}}": esc(product.get("moq_text", "")),
        "{{SUPPLIER}}": esc(product.get("supplier_text", "")),
        "{{SOURCE_URL}}": esc(product.get("url", "")),
        "{{DATE}}": esc(data.get("generated_at", "")),
        "{{MARKET_LANG_TAG}}": esc(market_lang_tag),
        "{{CONSUMER_INSIGHT_HTML}}": consumer_html,
        "{{ATTR_ROWS}}": attr_rows,
        "{{KW_ROWS}}": kw_rows,
        "{{FABE_ITEMS}}": fabe_html,
        "{{DRIVER_PRIMARY}}": esc(driver.get("primary", "")),
        "{{DRIVER_REASON_CN}}": esc(driver.get("reason_cn", "")),
        "{{DRIVER_REASON_EN}}": esc(driver.get("reason_en", "")),
        "{{BUYER_TARGET}}": esc(buyer.get("target_buyer", "")),
        "{{BUYER_TRIGGER}}": esc(buyer.get("purchase_trigger", "")),
        "{{BUYER_BELIEF}}": esc(buyer.get("belief_shift", "")),
        "{{BUYER_REASON}}": esc(buyer.get("primary_reason", "")),
        "{{BUYER_PROOF}}": esc(buyer.get("proof", "")),
        "{{SELLING_POINTS}}": sp_html,
        "{{AE_TITLE}}": esc(ae_title),
        "{{AE_TITLE_CN}}": esc(ae_title_cn),
        "{{AE_TITLE_LEN}}": str(ae_title_len),
        "{{AE_SPECS_TWOCOL}}": ae_specs_twocol,
        "{{AE_SKU}}": ae_sku_html,
        "{{AE_DESCRIPTION_HTML}}": ae_description_html,
        "{{AE_KEYWORDS}}": esc(ae_standard.get("search_keywords", "")),
        "{{AE_IMAGE_NOTES}}": esc(ae_standard.get("image_notes", "")),
        "{{GEO_TITLE}}": esc(ae_geo.get("title", "")),
        "{{GEO_FAQ_EN}}": geo_faq_en,
        "{{GEO_FAQ_CN}}": geo_faq_cn,
        "{{GEO_NL}}": geo_nl_html,
        "{{GEO_SITUATIONAL_CN}}": esc(ae_geo.get("situational_cn", "")),
        "{{GEO_SITUATIONAL_EN}}": esc(ae_geo.get("situational_en", "")),
        "{{GEO_COMPARISON_CN}}": esc(ae_geo.get("comparison_cn", "")),
        "{{GEO_COMPARISON_EN}}": esc(ae_geo.get("comparison_en", "")),
        "{{GEO_JSONLD}}": esc(ae_geo.get("jsonld", "")),
        "{{GEO_MULTILANG}}": esc(ae_geo.get("multilang", "")),
        "{{ASSUMPTIONS}}": asump_html,
    }

    output = template
    for k, v in repl.items():
        output = output.replace(k, v)
    return output

def main(argv):
    parser = argparse.ArgumentParser(description="Render AliExpress listing HTML report")
    parser.add_argument("report_json")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--template", default="")
    args = parser.parse_args(argv[1:])
    skill_dir = Path(__file__).resolve().parent.parent
    template_path = Path(args.template) if args.template else skill_dir / "assets" / TEMPLATE_NAME
    template = template_path.read_text(encoding="utf-8")
    data = load_json(Path(args.report_json))
    Path(args.output).write_text(render(data, template), encoding="utf-8")
    print(args.output)
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
