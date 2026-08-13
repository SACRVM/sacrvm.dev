# sacrvm.dev

Personal site — the business card, and the hub that points at everything else.

One hand-written `index.html`. No build step, no framework, no images: the mark
is an inline SVG path, so it scales to any DPI and takes the text colour. Same
palette as the JUST product pages, deliberately quieter — a product page sells,
a business card states.

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

## Editing

- Projects live in the `.projects` grid. One `<a class="project">` per project.
  The `shipping` tag is for things a visitor can actually download today —
  everything else gets no tag rather than an optimistic one.
- Do not list a repository that is still private. A card that 404s is worse than
  no card.

## Open

- The contact link in **Elsewhere** is a TODO — decide which address goes public.
- An Impressum will be needed here the moment anything is sold from this domain
  (name plus a summonable address). Worth settling before the store, not after.
