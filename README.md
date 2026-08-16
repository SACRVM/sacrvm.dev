# sacrvm.dev

Personal site — the business card, and the hub that points at everything else.

Hand-written HTML. No build step, no framework, no images, and **no external
requests**: the fonts are served from this host (`assets/fonts/`), nothing is
loaded from third-party servers, no cookies are set — the legal page says so
out loud, and the browser's network tab proves it.

Two colours and nothing else — celadon paper `#A1C9C8`, near-black ink
`#121211`; every grey is the ink at reduced opacity, every hover swaps the two.
Thin 1px boxes, zero border-radius anywhere. Type: Martian Mono for the
wordmark and labels, Instrument Sans for prose.

The signature is the wordmark: SACRVM is MARCVS rearranged, and every so often
the page solves itself — the letters rattle, settle into MARCVS, hold, the
Roman V becomes U, hold, then shuffle back to the name. Each letter sits in a
fixed `1ch` monospace cell so the rattle never shifts layout. Timing lives in
the `<script>` at the bottom of `index.html`; `prefers-reduced-motion` gets a
static page.

## Structure

| File | What |
|------|------|
| `index.html` | the card: wordmark, intro, projects, principles |
| `cv.html` | the résumé (career data only — no birth date, no phone, no references) |
| `imprint.html` | Impressum & Disclaimer, German, § 5 DDG |
| `assets/site.css` | shared base: fonts, tokens, sections/tabs, chips, component styles |
| `assets/site.js` | vanilla web components: `<site-nav>`, `<site-footer page="…">` |
| `assets/fonts/` | self-hosted variable woff2 (Martian Mono, Instrument Sans) |
| `blog/src/*.md` | blog sources, `YYYY-MM-DD-slug.md`; everything else under `blog/` is baked |
| `tools/` | the generators: blog baker, favicons, ASCII portrait, IndexNow ping |
| `<key>.txt` | IndexNow ownership key — the file name **is** the key; never rename or delete it |

The components are light-DOM custom elements on purpose — every page links one
stylesheet, and a shadow root would wall it off. The markup inside the tags is
the no-JS fallback, so the imprint link stays reachable without scripting.

## Deploy

GitHub Pages, custom domain, free certificate.

1. Push this repository to `github.com/SACRVM/sacrvm.dev`.
2. Settings → Pages → Source: `main`, folder `/` (root).
3. Settings → Pages → Custom domain: `sacrvm.dev`. That writes/keeps the `CNAME`
   file in this repository.
4. DNS at the registrar:

   | Type  | Name | Value |
   |-------|------|-------|
   | A     | `@`  | the four GitHub Pages IPs — **take them from the Pages settings page, not from memory** |
   | CNAME | `www`| `SACRVM.github.io` |

5. Tick **Enforce HTTPS** once the certificate is issued (a few minutes).

`.dev` is on the HSTS preload list, so browsers refuse plain HTTP for it
outright. That is a feature here and costs nothing: Pages issues and renews the
certificate itself.

Deployment after that is `git push`.

## Publishing a blog entry

1. Write `blog/src/YYYY-MM-DD-slug.md` with a `title:` / `description:`
   frontmatter block. The date in the file name is the publication date.
2. `python tools/bake-blog.py` — renders the entry page, rebuilds the index,
   the Atom feed and the sitemap. A deleted source unpublishes its page.
3. Commit and push, then wait for Pages to serve the change.
4. `python tools/indexnow.py` — tells IndexNow (Bing, Yandex, Seznam and the
   other participants) what changed. **After** the deploy, never before: the
   ping makes them fetch the URL right away, so an early ping indexes the old
   page. Google ignores IndexNow and comes via the sitemap.

## Editing

- Projects live in the **WHAT I BUILD** section. One `<a class="project">` per
  project. The `SHIPPING` chip is for things a visitor can actually download
  today — everything else gets no chip rather than an optimistic one.
- Do not list a repository that is still private. A card that 404s is worse than
  no card.

## Open

- The Impressum carries the private home address and the personal e-mail from
  the CV. Both are what the law wants — but confirm they should be public, or
  swap in a Postfach / dedicated alias before pushing.
