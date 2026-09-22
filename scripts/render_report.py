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
    ae_specs_html = ""
    for s in ae_standard.get("item_specifics", []):
        ae_specs_html += f'<li><span class="cn">{esc(s.get("cn",""))}</span><span class="en">{esc(s.get("en",""))}</span></li>\n'
    ae_sku_html = ""
    for s in ae_standard.get("sku", []):
        ae_sku_html += f'<tr><td>{esc(s.get("color",""))}</td><td>{esc(s.get("spec",""))}</td><td>{esc(s.get("price",""))}</td><td>{esc(s.get("stock",""))}</td></tr>\n'

    # AliExpress GEO listing
    geo_faq_html = ""
    for q in ae_geo.get("faq", []):
        geo_faq_html += f'<div class="qa"><div class="q"><span class="cn">{esc(q.get("q_cn",""))}</span><span class="en">{esc(q.get("q_en",""))}</span></div><div class="a"><span class="cn">{esc(q.get("a_cn",""))}</span><span class="en">{esc(q.get("a_en",""))}</span></div></div>\n'
    geo_nl_html = ""
    for n in ae_geo.get("natural_language", []):
        geo_nl_html += f'<span class="kw"><span class="en">{esc(n)}</span></span>\n'

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
        "{{AE_TITLE_LEN}}": str(ae_title_len),
        "{{AE_SPECS}}": ae_specs_html,
        "{{AE_SKU}}": ae_sku_html,
        "{{AE_DESCRIPTION_CN}}": esc(ae_standard.get("description_cn", "")),
        "{{AE_DESCRIPTION_EN}}": esc(ae_standard.get("description_en", "")),
        "{{AE_KEYWORDS}}": esc(ae_standard.get("search_keywords", "")),
        "{{AE_IMAGE_NOTES}}": esc(ae_standard.get("image_notes", "")),
        "{{GEO_TITLE}}": esc(ae_geo.get("title", "")),
        "{{GEO_FAQ}}": geo_faq_html,
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
