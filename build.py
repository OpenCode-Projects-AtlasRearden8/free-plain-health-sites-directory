#!/usr/bin/env python3
"""Generate SOURCES.md and site/index.html from data/sources.json.

Stdlib only. No network. Collects no data. Run: python3 build.py
"""

import json
import os
from html import escape
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "sources.json")
SITE_DIR = os.path.join(ROOT, "site")
MD_OUT = os.path.join(ROOT, "SOURCES.md")
HTML_OUT = os.path.join(SITE_DIR, "index.html")

CATEGORIES = {
    "government": ("Government & NIH health sites", "Ad-free, public-domain teaching material from NIH, NLM, CDC, and USDA."),
    "hospital": ("Hospital teaching libraries", "Clinician-reviewed article libraries from major hospitals."),
    "tracker": ("Free meal & medication trackers", "Free tools for logging meals or meds. Account/privacy flags are called out explicitly."),
}

EDU_NOTICE = "Education only — never medical advice. This site collects no data: no cookies, no analytics, no accounts."


def load_data():
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    for s in d["sources"]:
        u = urlparse(s["url"])
        if u.scheme != "https" or not u.netloc:
            raise ValueError(f"Non-HTTPS or malformed URL for {s['name']}: {s['url']}")
    return d


def md_out(d):
    lines = [
        f"# {d['title']}",
        "",
        f"_Updated {d['updated']}_. Published by Asdale Dynamics, LLC. MIT licensed.",
        "",
        "> " + d["disclaimer"],
        ">",
        "> **How ratings work:** reading levels are plain-language approximations —",
        "> **Easy** (~5th–6th grade), **Moderate** (~8th–9th), **Advanced** (10th+).",
        "> **Ad density** is what a reader actually sees around the content.",
        "",
        "## Government & NIH health sites",
        "Ad-free, public-domain teaching material from NIH, NLM, CDC, and USDA.",
        "",
    ]
    group = lambda cats: [s for s in d["sources"] if s["category"] == cats]
    for i, s in enumerate(group("government")):
        if i:
            lines.append("---")
        lines += ["", "### " + s["name"], "", f"- **Link:** {s['url']}",
                  f"- **Publisher:** {s['publisher']}",
                  f"- **Reading level:** {s['reading_level']}",
                  f"- **Ad density:** {s['ad_density']}",
                  f"- **Account required:** {'yes' if s['account_required'] else 'no'}",
                  f"- **Collects personal data:** {'yes' if s['collects_data'] else 'no'}"]
        if s["flags"]:
            lines.append("- **Flags:** " + "; ".join(s["flags"]))
        lines += ["", s["what"], "", s["notes"], ""]
    lines += ["## Hospital teaching libraries",
              "Clinician-reviewed article libraries from major hospitals.", ""]
    for i, s in enumerate(group("hospital")):
        if i:
            lines.append("---")
        lines += ["", "### " + s["name"], "", f"- **Link:** {s['url']}",
                  f"- **Publisher:** {s['publisher']}",
                  f"- **Reading level:** {s['reading_level']}",
                  f"- **Ad density:** {s['ad_density']}",
                  f"- **Account required:** {'yes' if s['account_required'] else 'no'}",
                  f"- **Collects personal data:** {'yes' if s['collects_data'] else 'no'}"]
        if s["flags"]:
            lines.append("- **Flags:** " + "; ".join(s["flags"]))
        lines += ["", s["what"], "", s["notes"], ""]
    lines += ["## Free meal & medication trackers",
              "Free tools for logging meals or meds. Account/privacy flags are called out explicitly.", ""]
    for i, s in enumerate(group("tracker")):
        if i:
            lines.append("---")
        lines += ["", "### " + s["name"], "", f"- **Link:** {s['url']}",
                  f"- **Publisher:** {s['publisher']}",
                  f"- **Reading level:** {s['reading_level']}",
                  f"- **Ad density:** {s['ad_density']}",
                  f"- **Account required:** {'yes' if s['account_required'] else 'no'}",
                  f"- **Collects personal data:** {'yes' if s['collects_data'] else 'no'}"]
        if s["flags"]:
            lines.append("- **Flags:** " + "; ".join(s["flags"]))
        lines += ["", s["what"], "", s["notes"], ""]
    lines += ["---", "",
              "## The fine print",
              "", d["disclaimer"],
              "",
              "Ratings are informed human estimates as of " + d["updated"] +
              "; sites redesign constantly, so treat the labels as a starting judgment call, not a guarantee.",
              "",
              "© Copyright (c) 2026 Asdale Dynamics, LLC — MIT licensed. Distinct from the",
              "general-purpose `free-official-help-directory` project; this one is health reading",
              "and self-tracking tools only.", ""]
    return "\n".join(lines)


def badge(label, kind):
    cls = {"Easy": "b-easy", "Moderate": "b-mod", "Advanced": "b-adv",
           "None": "b-none", "Low": "b-low", "High": "b-high"}.get(kind, "b-default")
    return f'<span class="badge {cls}">{escape(label)}</span>'


def card(s):
    acct = "yes" if s["account_required"] else "no"
    data_c = "yes" if s["collects_data"] else "no"
    flags = ""
    if s["flags"]:
        flags = '<ul class="flags">' + "".join(
            f"<li>{escape(f)}</li>" for f in s["flags"]) + "</ul>"
    return f"""<article class="card" id="{escape(s['name'].lower().replace(' ', '-'))}">
<h3><a href="{escape(s['url'])}" rel="noopener noreferrer">{escape(s['name'])}</a></h3>
<p class="publisher">{escape(s['publisher'])}</p>
<p class="ratings">Reading level: {badge(s['reading_level'], s['reading_level'])}
&nbsp; Ad density: {badge(s['ad_density'], s['ad_density'])}
&nbsp; Account: <strong>{acct}</strong>
&nbsp; Collects personal data: <strong>{data_c}</strong></p>
<p>{escape(s['what'])}</p>
<p class="notes">{escape(s['notes'])}</p>
{flags}
</article>"""


def html_out(d):
    groups = []
    for key, (title, blurb) in CATEGORIES.items():
        items = [card(s) for s in d["sources"] if s["category"] == key]
        groups.append(f'<section class="group" id="{key}"><h2>{escape(title)}</h2>'
                      f'<p class="blurb">{escape(blurb)}</p>{"".join(items)}</section>')
    nav = "".join(
        f'<a href="#{key}">{escape(CATEGORIES[key][0])}</a>' for key in CATEGORIES)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escape(d['title'])} — free plain-English health sites rated for reading level and ad density. Education only, never medical advice, no data collection.">
<title>{escape(d['title'])}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Ctext y='13' font-size='13'%3E%F0%9F%A9%BA%3C/text%3E%3C/svg%3E">
<style>
:root {{ --ink:#1c2530; --paper:#fafbfd; --card:#ffffff; --line:#dfe5ec; --accent:#1a6b5a; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Georgia, 'Times New Roman', serif; color:var(--ink); background:var(--paper); line-height:1.6; }}
header, footer {{ background:var(--card); border-bottom:1px solid var(--line); padding:2rem 1.25rem; text-align:center; }}
header h1 {{ margin:.2em 0; font-size:1.9rem; }}
.notice {{ max-width:46rem; margin:.8rem auto 0; font-size:.95rem; background:#f2f8f6; border:1px solid #cfe4dd; border-radius:8px; padding:.7rem 1rem; }}
main {{ max-width:52rem; margin:0 auto; padding:1.5rem 1.25rem; }}
nav.jump {{ text-align:center; margin:.9rem 0 1.6rem; font-family: Verdana, sans-serif; font-size:.9rem; }}
nav.jump a {{ margin:0 .5em; color:var(--accent); }}
.group h2 {{ border-bottom:2px solid var(--accent); padding-bottom:.3rem; font-size:1.35rem; }}
.blurb {{ font-size:.95rem; color:#4c5a68; margin-top:0; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:1rem 1.2rem; margin:1rem 0; }}
.card h3 {{ margin:0 0 .2rem; font-size:1.15rem; }}
.card h3 a {{ color:var(--accent); text-decoration:none; }}
.card h3 a:hover {{ text-decoration:underline; }}
.publisher {{ margin:.1rem 0 .6rem; color:#5a6773; font-size:.9rem; font-family: Verdana, sans-serif; }}
.ratings {{ font-family: Verdana, sans-serif; font-size:.82rem; background:#f4f6f9; border-radius:6px; padding:.45rem .6rem; }}
.badge {{ display:inline-block; border-radius:999px; padding:.05em .7em; font-weight:bold; font-family: Verdana, sans-serif; font-size:.78rem; }}
.b-easy {{ background:#e2f4e6; color:#1c5e2e; }}
.b-mod {{ background:#fdf3d7; color:#7a5b00; }}
.b-adv {{ background:#fbe4d8; color:#8a3b12; }}
.b-none {{ background:#e2f4e6; color:#1c5e2e; }}
.b-low {{ background:#e7f0fb; color:#1f4e79; }}
.b-high {{ background:#fbe4d8; color:#8a3b12; }}
.notes {{ font-size:.93rem; color:#4c5a68; }}
.flags {{ font-size:.85rem; color:#8a3b12; font-family: Verdana, sans-serif; }}
footer {{ border-bottom:0; border-top:1px solid var(--line); font-size:.9rem; }}
</style>
</head>
<body>
<header>
<h1>{escape(d['title'])}</h1>
<p>Free, trustworthy, plain-English health reading — with honest ratings for reading level and ad density.</p>
<div class="notice">{escape(EDU_NOTICE)}</div>
</header>
<nav class="jump">{nav}</nav>
<main>
{"".join(groups)}
<div class="notice"><strong>About the ratings:</strong> reading levels are informed estimates
(Easy ≈ 5th–6th grade, Moderate ≈ 8th–9th, Advanced = 10th+); ad density is what a reader
actually sees around the content, as of {escape(d['updated'])}. Websites redesign, so treat
these as judgment calls, not guarantees.</div>
</main>
<footer>
<p>{escape(EDU_NOTICE)}</p>
<p>{escape(d['title'])} — © Copyright (c) 2026 Asdale Dynamics, LLC — MIT licensed.
Generated by a build script, offline, from <code>data/sources.json</code>. No cookies, no analytics, no accounts.</p>
</footer>
</body>
</html>
"""


def main():
    d = load_data()
    md = md_out(d)
    html = html_out(d)
    os.makedirs(SITE_DIR, exist_ok=True)
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(md)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html)
    # A tiny text copy ensures the generated site carries zero executable payload.
    with open(os.path.join(SITE_DIR, "README.txt"), "w", encoding="utf-8") as f:
        f.write("This folder is generated output (from build.py). Open index.html "
                "in any browser.\nIt is a static page: no JavaScript, no cookies, "
                "no data collection.\n")
    total = len(d["sources"])
    print(f"OK: built {MD_OUT} and {HTML_OUT} ({total} sources)")


if __name__ == "__main__":
    main()
