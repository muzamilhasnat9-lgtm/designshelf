# Designshelf: static graphic design resource library

HTML5, CSS3, vanilla JS. No server, database or paid API. `build.py` (Python 3, standard library only) turns `data/resources.json` into plain static pages in `site/`.

## Run it
    python3 build.py                      # builds ./site (includes the local editor)
    python3 -m http.server -d site 8000   # open http://localhost:8000
    python3 build.py --prod               # deployable build, no editor

Before launch edit the top of `build.py`: `SITE` (your domain), `EMAIL`, `BASE` (only for sub-folder hosting), and review the privacy, terms and licence text (then set `LEGAL_NOTE = ""`).

## File tree
    build.py              page templates, sitemap, robots, validation
    data/resources.json   the resource catalogue (edit this)
    files/                your real downloads and preview images
    src/style.css, app.js, editor.html
    site/                 generated output (upload this)
      index.html  browse/  category/<slug>/  resources/<slug>/
      about/ contact/ privacy/ terms/ license/  404.html
      css/ js/ assets/previews/ downloads/ sitemap.xml robots.txt admin/ (local only)

## Add a resource
1. Copy your file into `files/` (e.g. `files/eid-card-2027.zip`) and a 4:3 preview (e.g. `files/eid-card-2027.webp`, about 800x600, under 100 KB; use .jpg/.png/.webp if you want Open Graph images).
2. Add a record to `data/resources.json` (or use `/admin/` locally and download the JSON):

       {"slug":"eid-card-2027","title":"Eid Card 2027","title_ur":"عید کارڈ","cat":"eid-and-islamic-greetings",
        "desc":"Short unique description.","desc_ur":"","dim":"1080 × 1350 px","fmt":["PSD","PNG"],
        "tags":["eid"],"date":"2027-03-01","file":"eid-card-2027.zip","preview":"eid-card-2027.webp"}

   Required: slug (a-z, 0-9, hyphens; never change it once published), title, cat (one of the 8 category slugs), desc, dim, fmt, date.
3. Run `python3 build.py`. Rules the build enforces: a download button appears only if the file exists in `files/` (or the record is `"placeholder": true`, which generates a labelled sample SVG). Otherwise the page says "Download not available yet". `"premium": true` hides the button and shows an inactive notice.

## SEO and indexing
- Every page has its own title, description, canonical URL and Open Graph tags; resource pages have BreadcrumbList and CreativeWork JSON-LD.
- Placeholder resources, and category/browse pages with no real resources, are `noindex` and left out of `sitemap.xml`, so the sample site does not publish thin pages. They become indexable automatically once real files are added.
- Search Console: add your domain at search.google.com/search-console, verify (DNS TXT record, or upload the HTML verification file into `site/`), then Sitemaps > submit `sitemap.xml`. Use URL Inspection on a few pages after each deploy.
- Deploy `site/` to any static host (Cloudflare Pages, Netlify, GitHub Pages) with HTTPS.

## Ads and premium
Ad containers are hidden, labelled comments plus empty `<aside class="ad-slot" hidden>` elements. After an ad network approves you, remove `hidden` and paste its code; update the privacy policy and add consent handling where required. No payment system exists; premium records only show an inactive notice.

## Testing checklist
- [ ] `python3 build.py` finishes without errors; run `python3 -m http.server -d site`
- [ ] Every header, footer, breadcrumb, category and related link opens a real page
- [ ] Browse: search (try "eid", an Urdu title), category, format and sort controls work; `/browse/?q=eid` and `?cat=certificates` pre-filter
- [ ] Each Download button saves a file; placeholder downloads are labelled
- [ ] A record with no `file` and no `placeholder` shows no button
- [ ] Urdu text displays right-to-left; test at 360 px width and with keyboard only (skip link, visible focus)
- [ ] `view-source:` shows unique title, description and canonical on each page
- [ ] `/admin/` loads, edits, downloads JSON; it is absent after `--prod`
- [ ] After deploy: set `SITE`, rebuild, check `/sitemap.xml` and `/robots.txt`, run Lighthouse

## Limitations
- Static output needs a rebuild (Python 3) after catalogue changes; there is no live database or upload form.
- The editor is a local tool with no authentication; never deploy `admin/`.
- The interface is English; Urdu is supported for resource titles, descriptions and key headings. A full Urdu interface is not included.
- Sample resources are generated SVG placeholders, not real designs. SVG previews cannot be used as Open Graph images; use raster previews for social sharing.
- Urdu text uses installed system fonts (Noto Nastaliq Urdu if present). Self-host a font file for consistent appearance.
- The contact form opens the visitor's email app. The legal pages are templates, not legal advice. Ads, AdSense approval, payments and analytics are not configured.
- The browse page lists all resources on one page; add pagination if the catalogue grows beyond a few hundred.
