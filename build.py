#!/usr/bin/env python3
"""Static site builder (Python 3 stdlib only).   python3 build.py   |   python3 build.py --prod
Reads data/resources.json + files/, writes the deployable site to ./site"""
import json, re, shutil, sys, html, datetime
from pathlib import Path

SITE = "https://www.example.com"   # CHANGE: your live domain, no trailing slash
BASE = ""                          # CHANGE only for sub-folder hosting, e.g. "/design"
NAME = "Designshelf"
EMAIL = "hello@example.com"        # CHANGE: shown on the Contact page
LEGAL_NOTE = '<p class="note"><strong>Template text, not legal advice.</strong> Review and edit this page before launch, then set LEGAL_NOTE = "" in build.py.</p>'
PROD = "--prod" in sys.argv
R = Path(__file__).parent; OUT = R / "site"; FILES = R / "files"
e = html.escape
UF = "'Noto Nastaliq Urdu','Jameel Noori Nastaleeq','Noto Naskh Arabic',Tahoma,serif"
CATS = [
 ("social-media-templates", "Social Media Templates", "سوشل میڈیا ٹیمپلیٹس", "Post, story and banner layouts for Instagram, Facebook and other networks."),
 ("business-cards", "Business Cards", "بزنس کارڈز", "Print-ready business card layouts you can customise with your own details."),
 ("flyers-and-posters", "Flyers and Posters", "فلائرز اور پوسٹرز", "Event, sale and announcement layouts in common print sizes."),
 ("youtube-thumbnails", "YouTube Thumbnails", "یوٹیوب تھمب نیلز", "1280 × 720 thumbnail layouts designed for clear titles and faces."),
 ("wedding-invitations", "Wedding Invitations", "شادی کے دعوت نامے", "Invitation and save-the-date designs for English and Urdu text."),
 ("certificates", "Certificates", "سرٹیفکیٹس", "Award and completion certificate layouts for schools, teams and events."),
 ("urdu-designs", "Urdu Designs", "اردو ڈیزائنز", "Designs built around right-to-left Urdu typography."),
 ("eid-and-islamic-greetings", "Eid and Islamic Greetings", "عید اور اسلامی گریٹنگز", "Greeting cards and banners for Eid, Ramadan and other occasions."),
]
CAT = {c[0]: c for c in CATS}
CCOL = {"social-media-templates":"#6d28d9","business-cards":"#0f766e","flyers-and-posters":"#c2410c","youtube-thumbnails":"#b91c1c","wedding-invitations":"#be185d","certificates":"#a16207","urdu-designs":"#1d4ed8","eid-and-islamic-greetings":"#047857"}
LIC = "Free for personal and commercial projects. You may edit the file, but you may not resell or redistribute it."
L = lambda p: BASE + p
today = datetime.date.today().isoformat()

def put(p):
    f = OUT / p.lstrip("/"); f.parent.mkdir(parents=True, exist_ok=True); return f
def has(n): return bool(n) and (FILES / n).is_file()
def altt(r): return ("Placeholder preview: " if r["_ph"] else "") + f'{r["title"]}, {CAT[r["cat"]][1]} design'

def svg(r):
    u = r.get("title_ur")
    ut = f'<text x="400" y="360" text-anchor="middle" direction="rtl" font-size="44" fill="#fff" font-family="{UF}">{e(u)}</text>' if u else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><rect width="800" height="600" fill="' + r.get("color", "#0f766e") +
            '"/><circle cx="690" cy="100" r="95" fill="#fff" fill-opacity=".18"/><circle cx="100" cy="510" r="120" fill="#000" fill-opacity=".14"/><rect x="70" y="70" width="80" height="80" rx="14" fill="#facc15" transform="rotate(14 110 110)"/><path d="M690 440l60 100h-120z" fill="#fff" fill-opacity=".25"/><rect x="30" y="30" width="740" height="540" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="4"/>'
            '<text x="400" y="280" text-anchor="middle" font-size="40" font-weight="700" fill="#fff" font-family="Arial,sans-serif">' + e(r["title"]) + '</text>' + ut +
            '<text x="400" y="540" text-anchor="middle" font-size="22" fill="#fff" font-family="Arial,sans-serif">PLACEHOLDER SAMPLE - replace with real artwork</text></svg>')

def ad(n):
    return (f'<!-- OPTIONAL AD SLOT "{n}" (inactive). After an ad network approves your site, remove the hidden attribute and paste its code inside. -->'
            f'<aside class="ad-slot" aria-label="Advertisement" hidden data-slot="{n}"><small>Advertisement</small></aside>')

def card(r):
    c = CAT[r["cat"]]; t = r["title"].lower()
    s = e(" ".join([t, r.get("title_ur", ""), c[1].lower()] + r.get("tags", [])).lower())
    meta = e(c[1] + ", " + "/".join(r["fmt"])) + (", placeholder" if r["_ph"] else "")
    return (f'<article class="card" style="--c:{CCOL[r["cat"]]}" data-n="{e(t)}" data-s="{s}" data-c="{r["cat"]}" data-d="{r["date"]}" data-f="{e(" ".join(x.lower() for x in r["fmt"]))}">'
            f'<a href="{L("/resources/" + r["slug"] + "/")}"><img src="{L(r["_p"])}" alt="{e(altt(r))}" width="800" height="600" loading="lazy" decoding="async"><h3>{e(r["title"])}</h3></a>'
            f'<p class="meta">{meta}</p></article>')

def grid(rs, gid=""): return f'<div class="grid"{gid}>' + "".join(card(r) for r in rs) + "</div>"

def page(path, title, desc, body, bc=None, ld=None, noindex=False, img=None, js=False, kind="website"):
    url = SITE + path; lds = [ld] if ld else []; nav = ""
    if bc:
        nav = '<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>' + "".join(
            f'<li><a href="{L(p)}">{e(n)}</a></li>' if p else f'<li aria-current="page">{e(n)}</li>' for n, p in bc) + "</ol></nav>"
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            dict({"@type": "ListItem", "position": i + 1, "name": n}, **({"item": SITE + p} if p else {})) for i, (n, p) in enumerate(bc)]})
    ldh = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False).replace("</", "<\\/") + "</script>" for x in lds)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    og = (f'<meta property="og:image" content="{SITE}{img}"><meta name="twitter:card" content="summary_large_image">' if img else '<meta name="twitter:card" content="summary">')
    cats = "".join(f'<li><a href="{L("/category/" + c[0] + "/")}">{e(c[1])}</a></li>' for c in CATS)
    legal = "".join(f'<li><a href="{L(p)}">{n}</a></li>' for p, n in [("/about/", "About"), ("/contact/", "Contact"), ("/privacy/", "Privacy Policy"), ("/terms/", "Terms of Use"), ("/license/", "Licence and Copyright")])
    script = f'<script src="{L("/js/app.js")}" defer></script>' if js else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">{robots}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="{kind}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="{NAME}">{og}
<link rel="icon" href="{L('/favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{L('/css/style.css')}">{ldh}</head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar"><a class="logo" href="{L('/')}">Design<span>shelf</span></a>
<nav aria-label="Main"><a href="{L('/browse/')}">Browse</a><a href="{L('/about/')}">About</a><a href="{L('/contact/')}">Contact</a></nav>
<form action="{L('/browse/')}" role="search"><label class="sr" for="hq">Search resources</label><input id="hq" name="q" type="search" placeholder="Search resources"><button type="submit">Search</button></form></div></header>
{nav}<main id="main" class="wrap">{body}</main>
<footer><div class="wrap"><nav aria-label="Categories"><strong>Categories</strong><ul>{cats}</ul></nav><nav aria-label="Legal"><strong>Site</strong><ul>{legal}</ul></nav><p>{NAME}. Sample resources are placeholders unless marked otherwise.</p></div></footer>{script}</body></html>"""

def emit(path, *a, **k): put(path + "index.html").write_text(page(path, *a, **k), "utf-8")
def simple(path, title, desc, h1, content):
    emit(path, title + f" | {NAME}", desc, f"<h1>{h1}</h1>{content}", bc=[("Home", "/"), (h1, None)])

# ---------- data ----------
data = json.loads((R / "data" / "resources.json").read_text("utf-8")); seen = set()
if OUT.exists(): shutil.rmtree(OUT)
for r in data:
    assert re.fullmatch(r"[a-z0-9-]+", r["slug"]) and r["slug"] not in seen and r["cat"] in CAT, "Bad record: " + r["slug"]
    seen.add(r["slug"]); r.setdefault("fmt", ["SVG"]); r.setdefault("tags", [])
    pv = r.get("preview")
    if has(pv): shutil.copy(FILES / pv, put("/assets/previews/" + pv)); r["_p"] = "/assets/previews/" + pv
    else: r["_p"] = f"/assets/previews/{r['slug']}.svg"; put(r["_p"]).write_text(svg(r), "utf-8")
    fl = r.get("file"); r["_ph"] = False; r["_d"] = None
    if has(fl): shutil.copy(FILES / fl, put("/downloads/" + fl)); r["_d"] = "/downloads/" + fl
    elif r.get("placeholder"): r["_d"] = f"/downloads/{r['slug']}-placeholder.svg"; put(r["_d"]).write_text(svg(r), "utf-8"); r["_ph"] = True
data.sort(key=lambda r: r["date"], reverse=True)
real = [r for r in data if not r["_ph"] and r["_d"]]

shutil.copy(R / "src/style.css", put("/css/style.css")); shutil.copy(R / "src/app.js", put("/js/app.js"))
put("/favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#6d28d9"/><circle cx="23" cy="9" r="5" fill="#f97316"/><path d="M9 9h8a7 7 0 010 14H9z" fill="#fff"/></svg>', "utf-8")

# ---------- home ----------
cl = "".join(f'<li><a style="--c:{CCOL[c[0]]}" href="{L("/category/" + c[0] + "/")}"><strong>{e(c[1])}</strong><span lang="ur" dir="rtl" class="ur">{c[2]}</span><small>{sum(1 for r in data if r["cat"] == c[0])} resources</small></a></li>' for c in CATS)
emit("/", f"Free Graphic Design Resources and Templates | {NAME}",
     "Download free design templates for social media, business cards, flyers, certificates, Urdu typography and Eid greetings, with clear licence and file details.",
     f'''<section class="hero"><h1>Free graphic design resources</h1><p>Templates for social media, print, certificates, Urdu typography and Eid greetings.</p>
<p lang="ur" dir="rtl" class="ur">مفت گرافک ڈیزائن وسائل</p>
<form action="{L("/browse/")}" role="search" class="big"><label class="sr" for="hq2">Search resources</label><input id="hq2" name="q" type="search" placeholder="Search Eid, thumbnail, certificate"><button type="submit">Search</button></form></section>
<h2>Browse by category</h2><ul class="cats">{cl}</ul>{ad("home-banner")}
<h2>Latest resources</h2>{grid(data[:6])}<p><a href="{L("/browse/")}">Browse all resources</a></p>''', kind="website")

# ---------- browse ----------
fmts = sorted({f.upper() for r in data for f in r["fmt"]})
opt = lambda xs: "".join(f'<option value="{v}">{e(t)}</option>' for v, t in xs)
emit("/browse/", f"Browse All Free Design Resources | {NAME}",
     "Search and filter every free design resource by title, category and file format, and sort by newest or A to Z.",
     f'''<h1>Browse all resources</h1>
<div class="filters" id="flt" hidden><label class="sr" for="q">Search by title or category</label><input id="q" type="search" placeholder="Search by title or category">
<label class="sr" for="cat">Category</label><select id="cat"><option value="">All categories</option>{opt([(c[0], c[1]) for c in CATS])}</select>
<label class="sr" for="fmt">Format</label><select id="fmt"><option value="">All formats</option>{opt([(f.lower(), f) for f in fmts])}</select>
<label class="sr" for="sort">Sort</label><select id="sort"><option value="new">Newest first</option><option value="az">A to Z</option></select></div>
<p id="count" aria-live="polite">{len(data)} resources</p><h2 class="sr">Results</h2>{grid(data, ' id="grid"')}{ad("browse-banner")}''',
     bc=[("Home", "/"), ("Browse", None)], js=True, noindex=not real)

# ---------- categories ----------
for c in CATS:
    rs = [r for r in data if r["cat"] == c[0]]
    emit(f"/category/{c[0]}/", f"{c[1]} - Free Design Downloads | {NAME}", c[3] + " Free files with format, size and licence details.",
         f'<div class="chead" style="--c:{CCOL[c[0]]}"><h1>{e(c[1])}</h1><p lang="ur" dir="rtl" class="ur">{c[2]}</p><p>{e(c[3])}</p></div><h2 class="sr">Resources</h2>' +
         (grid(rs) if rs else "<p>No resources in this category yet. Check back soon or browse <a href=\"" + L("/browse/") + "\">all resources</a>.</p>") + ad("category-banner"),
         bc=[("Home", "/"), ("Browse", "/browse/"), (c[1], None)], noindex=not any(r in real for r in rs))

# ---------- resources ----------
for r in data:
    c = CAT[r["cat"]]; path = f"/resources/{r['slug']}/"; ur = r.get("title_ur"); ph = r["_ph"]
    if r.get("premium"): dl = '<p class="note">Premium downloads are not active on this site yet.</p>'
    elif r["_d"]:
        dl = f'<a class="btn" href="{L(r["_d"])}" download>Download {"placeholder " if ph else ""}({"/".join(r["fmt"])})</a>' + ('<p class="note">This is a placeholder sample, not a finished design.</p>' if ph else "")
    else: dl = '<p class="note">Download not available yet.</p>'
    urt = f'<p class="ur" lang="ur" dir="rtl">{e(ur)}</p>' if ur else ""
    urd = f'<p class="ur" lang="ur" dir="rtl">{e(r["desc_ur"])}</p>' if r.get("desc_ur") else ""
    o = sorted([x for x in data if x is not r], key=lambda x: x["date"], reverse=True); o.sort(key=lambda x: x["cat"] != r["cat"])
    body = (f'<article style="--c:{CCOL[r["cat"]]}"><h1>{e(r["title"])}</h1>{urt}<div class="detail"><img class="pv" src="{L(r["_p"])}" alt="{e(altt(r))}" width="800" height="600" fetchpriority="high">'
            f'<div><dl><dt>Category</dt><dd><a href="{L("/category/" + r["cat"] + "/")}">{e(c[1])}</a></dd><dt>Formats</dt><dd>{e(", ".join(r["fmt"]))}</dd>'
            f'<dt>Dimensions</dt><dd>{e(r["dim"])}</dd><dt>Licence</dt><dd><a href="{L("/license/")}">Free licence</a></dd><dt>Added</dt><dd>{r["date"]}</dd></dl>{dl}</div></div>'
            f'<h2>About this resource</h2><p>{e(r["desc"])}</p>{urd}<h2>Licence</h2><p>{LIC} <a href="{L("/license/")}">Read the full policy</a>.</p></article>'
            f'{ad("resource-detail")}<h2>Related resources</h2>{grid(o[:3])}')
    ld = None if ph else {"@context": "https://schema.org", "@type": "CreativeWork", "name": r["title"], "description": r["desc"], "url": SITE + path,
                          "image": SITE + r["_p"], "datePublished": r["date"], "license": SITE + "/license/", "genre": c[1], "isAccessibleForFree": True}
    img = r["_p"] if r["_p"].lower().endswith((".png", ".jpg", ".jpeg", ".webp")) else None
    emit(path, f'{r["title"]} - Free {c[1]} | {NAME}', r["desc"], body,
         bc=[("Home", "/"), ("Browse", "/browse/"), (c[1], f"/category/{c[0]}/"), (r["title"], None)], ld=ld, noindex=ph, img=img, kind="article")

# ---------- static pages ----------
simple("/about/", "About", "About Designshelf, a free library of graphic design resources for English and Urdu-speaking creators.", "About Designshelf",
       f'''<p>{NAME} is a free library of graphic design resources for creators who work in English and Urdu: social media templates, print layouts, certificates, Urdu typography and Eid greetings.</p>
<h2>Current status</h2><p>The resources listed so far are original placeholders that demonstrate how the library works. They are labelled as placeholders and are not finished designs.</p>
<h2>What to expect</h2><p>Every resource shows its formats, dimensions and licence before you download. The <a href="{L("/license/")}">licence policy</a> explains what you can and cannot do.</p>
<p lang="ur" dir="rtl" class="ur">یہ ویب سائٹ انگریزی اور اردو بولنے والے ڈیزائنرز کے لیے مفت ڈیزائن وسائل فراہم کرنے کے لیے بنائی گئی ہے۔</p>''')
simple("/contact/", "Contact", "Contact Designshelf about questions, licensing or copyright takedown requests.", "Contact",
       f'''<p>For questions, licensing or copyright takedown requests, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<form action="mailto:{EMAIL}" method="get" enctype="text/plain" class="ed"><label>Subject<input name="subject" required></label><label>Message<textarea name="body" rows="5" required></textarea></label><button type="submit">Open in your email app</button></form>
<p class="note">This form opens your email app. The site has no server, so it cannot send messages itself.</p>''')
simple("/privacy/", "Privacy Policy", "How Designshelf handles visitor data, cookies and third-party services.", "Privacy Policy",
       f'''{LEGAL_NOTE}<h2>What we collect</h2><p>This site has no accounts and does not send form data to a server. We do not set cookies ourselves. Our hosting provider may keep standard server logs such as IP address and requested pages.</p>
<h2>Third-party services</h2><p>If we enable tools such as analytics, Google Search Console verification or an ad network, they may use cookies or collect data. This policy will be updated, and a consent notice added where the law requires it, before any such tool is switched on.</p>
<h2>Email</h2><p>If you email us, we use your message only to reply to you.</p><h2>Contact</h2><p>Questions about privacy: <a href="mailto:{EMAIL}">{EMAIL}</a>. Last updated: {today}.</p>''')
simple("/terms/", "Terms of Use", "Terms for using Designshelf and downloading its design resources.", "Terms of Use",
       f'''{LEGAL_NOTE}<h2>Using the site</h2><p>You may browse the site and download resources under the <a href="{L("/license/")}">licence policy</a>. Do not misuse the site or try to disrupt it.</p>
<h2>No warranty</h2><p>Resources are provided as they are, without warranty. You are responsible for checking that a design suits your purpose, including any names, logos and photos you add.</p>
<h2>Takedown</h2><p>If you believe a resource infringes your rights, follow the steps in the licence and copyright policy.</p><h2>Changes</h2><p>We may update these terms. Last updated: {today}.</p>''')
simple("/license/", "Licence and Copyright Policy", "What you may and may not do with Designshelf downloads, and how to report copyright concerns.", "Licence and Copyright Policy",
       f'''{LEGAL_NOTE}<h2>Free licence</h2><p>Unless a resource page says otherwise, you may use the file in personal and commercial projects, including client work, print and social media. You may edit and adapt it. Attribution is appreciated but not required.</p>
<h2>Not allowed</h2><p>Do not resell, redistribute or re-upload the file itself, alone or in packs. Do not present it as your own template product. Do not use it to imply endorsement by {NAME}.</p>
<h2>Placeholders</h2><p>Files marked as placeholders are samples created for this site. They are not finished designs and are not intended for final use.</p>
<h2>Third-party assets</h2><p>Fonts, photos or icons included in a resource keep their own licences. Each resource page should name any such asset.</p>
<h2>Report a copyright concern</h2><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> with the page URL, your contact details and a description of your ownership. We will review it promptly and remove infringing files.</p>''')
put("/404.html").write_text(page("/404.html", f"Page not found | {NAME}", "This page could not be found.", f'<h1>Page not found</h1><p><a href="{L("/")}">Go to the home page</a> or <a href="{L("/browse/")}">browse all resources</a>.</p>', noindex=True), "utf-8")

# ---------- sitemap, robots, editor ----------
urls = ["/", "/about/", "/contact/", "/privacy/", "/terms/", "/license/"]
if real: urls += ["/browse/"] + [f"/category/{c[0]}/" for c in CATS if any(r["cat"] == c[0] for r in real)] + [f"/resources/{r['slug']}/" for r in real]
put("/sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
    "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>", "utf-8")
put("/robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {SITE}/sitemap.xml\n", "utf-8")
if not PROD:
    put("/admin/index.html").write_text((R / "src/editor.html").read_text("utf-8").replace("__CATS__", json.dumps([[c[0], c[1]] for c in CATS])), "utf-8")
    shutil.copy(R / "data/resources.json", put("/data/resources.json"))
print(f"Built {len(data)} resources, {len(real)} real, {len(urls)} sitemap URLs -> {OUT}")
