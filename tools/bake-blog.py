"""Bake the blog: blog/src/*.md -> static pages, index, Atom feed, sitemap.

Source files are named YYYY-MM-DD-slug.md (the date in the name IS the
publication date) and start with a small frontmatter block:

    ---
    title: The entry's title
    description: One sentence for meta tags, the index and the feed.
    ---
    Markdown body...

Markdown subset (deliberately small, rendered by hand, no library):
  # ## ###   -> h2 h3 h4 (the page h1 is the title)
  **b** *i* `code`  [text](url)
  - item / 1. item  (one level)
  > quote
  ``` fenced code ```
  ---        -> horizontal rule
  everything else: paragraphs

Outputs: blog/<name>.html per entry, blog/index.html, blog/feed.xml,
and sitemap.xml is rewritten with all non-blog URLs preserved.
"""

import html
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "blog" / "src"
OUT = ROOT / "blog"
SITE = "https://sacrvm.dev"

# --- markdown ---------------------------------------------------------------

def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    parts = re.split(r"(`[^`]+`)", s)          # protect code spans
    for i, p in enumerate(parts):
        if p.startswith("`") and p.endswith("`"):
            parts[i] = "<code>" + p[1:-1] + "</code>"
        else:
            p = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', p)
            p = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", p)
            p = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", p)
            parts[i] = p
    return "".join(parts)


def render(md: str) -> str:
    out, i, lines = [], 0, md.replace("\r\n", "\n").split("\n")
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            code = html.escape("\n".join(lines[i + 1:j]), quote=False)
            out.append("<pre><code>" + code + "</code></pre>")
            i = j + 1
        elif re.fullmatch(r"-{3,}", line.strip()):
            out.append("<hr>")
            i += 1
        elif m := re.match(r"(#{1,3}) +(.*)", line):
            out.append("<h%d>%s</h%d>" % (len(m[1]) + 1, inline(m[2]), len(m[1]) + 1))
            i += 1
        elif line.startswith("> "):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i][2:] if lines[i].startswith("> ") else "")
                i += 1
            out.append("<blockquote>" + render("\n".join(block)) + "</blockquote>")
        elif re.match(r"[-*] |\d+\. ", line):
            ordered = bool(re.match(r"\d", line))
            items = []
            while i < len(lines) and re.match(r"[-*] |\d+\. ", lines[i]):
                item = re.sub(r"^([-*]|\d+\.) ", "", lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip():
                    item += " " + lines[i].strip()   # wrapped item continues
                    i += 1
                items.append("<li>" + inline(item) + "</li>")
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join(items), tag))
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(
                r"```|#{1,3} |> |[-*] |\d+\. ", lines[i]
            ):
                para.append(lines[i])
                i += 1
            out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "\n".join(out)


# --- templates --------------------------------------------------------------


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="SACRVM">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="{ogtype}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://sacrvm.dev/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
{extra}<link rel="alternate" type="application/atom+xml" title="SACRVM — Blog" href="/blog/feed.xml">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
</head>
<body>

<div class="page">

  <site-nav page="blog"><a href="/">SACRVM.DEV</a></site-nav>
"""

FOOT = """
  <site-footer page="blog"><a href="/">Home</a></site-footer>

</div>

</body>
</html>
"""


def head(title, description, url, ogtype, extra=""):
    return HEAD.format(
        title=html.escape(title), description=html.escape(description, quote=True),
        url=url, ogtype=ogtype, extra=extra,
    )


# --- read sources -----------------------------------------------------------

entries = []
for f in sorted(SRC.glob("*.md"), reverse=True):
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.md$", f.name)
    if not m:
        raise SystemExit(f"bad source name (want YYYY-MM-DD-slug.md): {f.name}")
    fm = re.match(r"---\n(.*?)\n---\n(.*)$", f.read_text(encoding="utf-8"), re.S)
    if not fm:
        raise SystemExit(f"missing frontmatter: {f.name}")
    meta = dict(
        (k.strip(), v.strip())
        for k, v in (l.split(":", 1) for l in fm[1].splitlines() if ":" in l)
    )
    entries.append({
        "date": m[1], "name": f"{m[1]}-{m[2]}.html",
        "title": meta["title"], "description": meta["description"],
        "body": render(fm[2]),
    })

# --- entry pages ------------------------------------------------------------

for idx, e in enumerate(entries):
    url = f"{SITE}/blog/{e['name']}"
    extra = f'<meta property="article:published_time" content="{e["date"]}">\n'

    # entries are newest-first: the neighbour above is newer, below is older.
    # The boxed BLOG link sits in the middle and is always there — after
    # reading, the way back matters most at the bottom.
    newer = entries[idx - 1] if idx > 0 else None
    older = entries[idx + 1] if idx + 1 < len(entries) else None
    hop_older = (
        f'<a rel="prev" href="/blog/{older["name"]}">'
        f'<span class="lbl">&larr; OLDER</span>'
        f'<span class="t">{html.escape(older["title"])}</span></a>'
        if older else "<span></span>"
    )
    hop_newer = (
        f'<a rel="next" class="newer" href="/blog/{newer["name"]}">'
        f'<span class="lbl">NEWER &rarr;</span>'
        f'<span class="t">{html.escape(newer["title"])}</span></a>'
        if newer else "<span></span>"
    )
    entry_nav = f"""
  <nav class="entry-nav">
    {hop_older}
    <a class="index" href="/blog/">&larr; BLOG</a>
    {hop_newer}
  </nav>
"""

    page = (
        head(f"{e['title']} — SACRVM", e["description"], url, "article", extra)
        + f"""
  <header class="blog-head">
    <a class="back" href="/blog/">&larr; BLOG</a>
    <div class="date">{e['date']}</div>
    <h1>{html.escape(e['title'])}</h1>
  </header>

  <article class="prose">
{e['body']}
  </article>
{entry_nav}"""
        + FOOT
    )
    (OUT / e["name"]).write_text(page, encoding="utf-8", newline="\n")

# entry pages whose source is gone are unpublished, not left to rot
current = {e["name"] for e in entries}
for f in OUT.glob("*.html"):
    if f.name != "index.html" and f.name not in current:
        f.unlink()

# --- index ------------------------------------------------------------------
# Deliberately one flat list for now. When it grows past roughly a year of
# entries, this is where the archive goes: per-year pages (/blog/2026.html),
# the index keeps the current year plus an archive row.

if entries:
    rows = "\n".join(
        f"""    <a class="entry-row" href="/blog/{e['name']}">
      <span class="date">{e['date']}</span>
      <span class="t">{html.escape(e['title'])}</span>
      <span class="sub">{html.escape(e['description'])}</span>
    </a>"""
        for e in entries
    )
else:
    rows = '    <p class="empty">No entries yet — the first one is being written.</p>'

index = (
    head("Blog — SACRVM", "Updates on the tools and libraries built here — releases, changes, plans.",
         f"{SITE}/blog/", "website")
    + f"""
  <header class="blog-head">
    <h1>Blog</h1>
    <p>Updates on the tools and libraries built here, one entry at a time.
       There is a <a href="/blog/feed.xml">feed</a>
       — that is the whole subscription model.</p>
  </header>

  <section class="entries">
{rows}
  </section>
"""
    + FOOT
)
(OUT / "index.html").write_text(index, encoding="utf-8", newline="\n")

# --- atom feed --------------------------------------------------------------

updated = (entries[0]["date"] if entries else date.today().isoformat()) + "T00:00:00Z"
items = "".join(
    f"""
  <entry>
    <title>{html.escape(e['title'])}</title>
    <link href="{SITE}/blog/{e['name']}"/>
    <id>{SITE}/blog/{e['name']}</id>
    <updated>{e['date']}T00:00:00Z</updated>
    <summary>{html.escape(e['description'])}</summary>
    <content type="html">{html.escape(e['body'])}</content>
  </entry>"""
    for e in entries
)
feed = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>SACRVM — Blog</title>
  <link href="{SITE}/blog/feed.xml" rel="self"/>
  <link href="{SITE}/blog/"/>
  <id>{SITE}/blog/</id>
  <author><name>SACRVM</name></author>
  <updated>{updated}</updated>{items}
</feed>
"""
(OUT / "feed.xml").write_text(feed, encoding="utf-8", newline="\n")

# --- sitemap: keep non-blog urls, rewrite the blog ones ---------------------

sm = ROOT / "sitemap.xml"
kept = [
    (loc, mod)
    for loc, mod in re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", sm.read_text())
    if not loc.startswith(f"{SITE}/blog/")
]
urls = kept + [(f"{SITE}/blog/", updated[:10])] + [
    (f"{SITE}/blog/{e['name']}", e["date"]) for e in entries
]
body = "\n".join(
    f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n  </url>"
    for loc, mod in urls
)
sm.write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"{body}\n</urlset>\n",
    encoding="utf-8", newline="\n",
)

print(f"baked {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}: index, feed, sitemap updated")
