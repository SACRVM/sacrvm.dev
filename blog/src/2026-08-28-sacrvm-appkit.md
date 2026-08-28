---
title: SACRVM APPKIT — the kit, a desktop, and two apps to prove it
description: A zero-dependency HTML UI kit — forty-one web components, one-variable theming, install-by-URL apps — with a live desktop at desktop.sacrvm.dev to try in the browser.
---
[SACRVM APPKIT](https://github.com/SACRVM/sacrvm-appkit) is a UI kit for the
web with no build step: some forty `sac-*` web components, a theming engine
that derives every colour from one `--accent` variable, and an app system
that installs apps by URL. You vendor one folder of plain files, link one
stylesheet and one script, and write HTML. No framework, no bundler, no
node_modules — F5 is the toolchain.

# Try it before reading on

The proof runs at [desktop.sacrvm.dev](https://desktop.sacrvm.dev/): a
desktop in your browser. It is a **host, not an app** — it owns the home
screen and the bare stage, and every app on it is installed by URL from
somebody else's repository. Reading a manifest and running code are two
separate steps: the desktop shows what it found, names the origin on every
tile, and asks before anything executes. The app list lives in your
browser's localStorage — no server, no account.

On your first visit the desktop offers its two reference apps, so the
stage does not start empty:

- [Calculator](https://github.com/SACRVM/sacrvm-calculator) — a `window`
  app: one custom element, one classic script, and a proper two-register
  pocket-calculator brain in ~400 dependency-free lines.
- [Notes](https://github.com/SACRVM/sacrvm-notes) — a `view` app: it draws
  its own chrome, the note list is the rail, and every note gets its own
  link.

Their repos are worked examples — see it done properly. To start your own
app, don't strip a calculator down to a skeleton; there is a starting
point built for the job. Zero to running on the desktop is three steps:

1. **Use this template** on
   [sacrvm-app-template](https://github.com/SACRVM/sacrvm-app-template) —
   a clean repo with the right shape from commit one: `app.json`,
   `app.js`, `app.css`, a vendored `kit/`. Rename five strings.
2. **Enable GitHub Pages** — now your app has a URL.
3. **Hand out the link** —
   `https://desktop.sacrvm.dev/?install=<your-pages-url>` runs the
   ordinary confirm flow, and your app is on the desktop.

# The kit itself

- **Two files.** `kit/css/ui.css` carries the design tokens and the global
  stylesheet, `kit/js/all.js` carries every component. The `kit/` folder is
  vendored verbatim; `kit/VERSION` says which release you hold.
- **The components.** Floating draggable windows, a nav ribbon with burger
  panel, sidebar and split workspace layouts, dialogs, menus, toasts,
  tooltips, tabs — and form controls down to a colour picker and a date
  field.
- **Seed-derived theming.** Light, dark and auto via `data-theme`; every
  colour is `color-mix()`-derived from one `--accent`. An app re-themes
  from a single variable, at runtime, with no build.
- **A runtime, not just widgets.** `window.sac.*` brings the router, the
  dialog and toast services, a Ctrl-K command palette, sandboxed storage,
  and `sac.apps` — the install-by-URL system the desktop is built on.
- **Scaffolds included.** `kit/templates/` ships complete app skeletons
  and page-level scaffolds — the folder of plain files contains its own
  starting points.

# No build step, on purpose

Vendoring is the whole upgrade story: delete `kit/`, unzip the new release,
F5. The kit ships as a ZIP of plain files from
[GitHub Releases](https://github.com/SACRVM/sacrvm-appkit/releases), MIT
licensed. Nothing is transpiled, nothing is locked — what you commit is
what runs.

---

The style guide with every token and component lives in the
[appkit repo](https://github.com/SACRVM/sacrvm-appkit); the desktop's
long-form "How this works" is at
[desktop.sacrvm.dev/how.html](https://desktop.sacrvm.dev/how.html).
Feedback and bug reports to the
[issue tracker](https://github.com/SACRVM/sacrvm-appkit/issues) or
[mail@sacrvm.dev](mailto:mail@sacrvm.dev).

*F5 is the toolchain.*
