---
title: The Fishbowl — your memory lives here, you don't
description: A self-hosted home for notes, calendar, contacts, mail and files: every workspace a folder of its own, search that finds what you mean on your own CPU, and an MCP server that lets an agent work in it without letting it loose.
---
The Fishbowl is where my notes, todos, calendar, contacts, mail and files
live. It runs on my own machine, it is open source, and an AI agent can
work in it — remember things, find them, sort the mail, build a small app
for a shared space — without getting more than I hand it. I started it in
April, v0.6.0 is out, and the
[repository](https://github.com/SACRVM/the-fishbowl) is public.

# Why

Tools like this exist, and the pattern is familiar: free to start, useful
enough to depend on, and then exports get harder and features move behind
a price. The Fishbowl starts from the other end. A tool that earns its
keep doesn't need to hold your data to keep you, so leaving has to cost
nothing.

- **Every workspace is a folder.** My personal one and every shared space
  is one SQLite database with its files beside it, in a folder of its
  own. Stop the host and that folder is the whole workspace; while it
  runs, export hands out the same as a ZIP, any time, without asking.
- **Files stay files.** What goes into Files lies on disk under its real
  name, in a real folder tree, not as blobs in a table.
- **Nothing phones home.** The interface loads nothing from anyone else's
  servers. What talks to the outside world is what I set up: my mail
  servers, Discord, a Google sign-in if I want one — and, once, the
  download of the search model.

# What is in the bowl

One desktop in the browser, built on
[SACRVM APPKIT](https://github.com/SACRVM/sacrvm-appkit): tiles that show
what is in them — the next dates, open todos, unread mail — and a command
palette (Ctrl/⌘K) that searches everything as you type.

- **Notes** in markdown, with `:::secret` blocks encrypted in the browser.
  The key opens with a passphrase, 24 recovery words or a passkey; the
  server only ever stores ciphertext, and neither search nor an agent
  sees what is inside.
- **Calendar** with full recurrence rules, `.ics` import and export,
  subscription links for the phone, and the contacts' birthdays.
- **Contacts**: people and organisations, vCard and CSV both ways,
  duplicates found and merged.
- **Mail** from iCloud, Gmail, IONOS or any IMAP server, every account in
  one list. The Fishbowl keeps its own copy and uses IMAP only as the
  transport, so search, tags and rules work across accounts. New mail
  arrives by push, and writing is markdown. Spam is read live from the
  server and never stored, so it never reaches search or an agent.
- **Files**: a two-pane commander, made for the keyboard.
- **Todos**, in the order I drag them.

And the conversation: a Discord bot to remember something, search, see
what is coming, get reminders and a short morning digest. It answers with
titles only; the content stays in the bowl.

# Finding by meaning

Search blends two rankings: the words, from SQLite's full-text index, and
the meaning, from
[multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small).
That small model runs on the machine's own CPU and turns every note, mail
and searchable table row into a vector. "That thing about the venue last
month" finds the note even when it used other words. German works as well
as English, which the first, English-only model never managed. A hit with
all the words still comes first: a name means little to a model.

# Spaces

A space is a workspace shared with others: the family, a club, a team.
Roles go from Reader to Owner, and invitations are links. Each space is
its own folder again, with its own notes, calendar, mail and files, plus
tables.

Tables are a small database the space defines for itself: typed columns,
and links that work like foreign keys, so nothing that is linked to can
be deleted. On top of them a space can have its own **apps**: plain
JavaScript files in the space's `.apps` folder, run in a sandboxed frame,
with the space's data handed in through one object. A table can have
**triggers**, small scripts in a JavaScript sandbox that check or change
a row before it is written.

# Built for agents

The Fishbowl is an MCP server: 40 tools over notes, contacts, the
calendar, mail, files, tables and a space's apps. The calendar is
read-only on purpose: an agent scheduling your days has sharper
consequences than one remembering a note. Claude Code connects with one
command:

```
claude mcp add --transport http fishbowl https://<your-host>/mcp \
  --header "Authorization: Bearer <key>"
```

On a public HTTPS host, claude.ai connects as a custom connector with
OAuth instead. Either way the same rules hold:

- **A key is one workspace and a list of scopes**: read notes, write
  contacts, read mail. Sending mail is a scope of its own and part of no
  default level, because a key that can read mail and send it could be
  steered by a crafted mail. On every request a key is cut down to what
  its owner may still do in that space.
- **What an agent writes waits for review.** A note from an agent carries
  `review:pending` until a person edits it.
- **Secrets never cross the wire**, and mail reaches an agent marked as
  untrusted: data from its sender, never an instruction.
- **An agent can build an app for a space.** `space_guide` writes it the
  space's tables, apps, house rules and latest errors as one page of
  markdown; the file tools write the code; `app_errors` tells it what
  broke when someone opened it.

The agents find the gaps, too. On 29 October one asked which account it
should send a mail from instead of guessing. The tool took only an
internal id and fell back to the first account, so that was the tool's
fault, not the agent's. Now an agent names the address, and in a
workspace with several accounts Fishbowl refuses to pick one for it.

# How it is made

.NET 10 and ASP.NET Core on the server; SQLite through Dapper, with
sqlite-vec for the vectors; MailKit for mail and Ical.Net for calendars.
The interface is vanilla JavaScript without a build step, on SACRVM
APPKIT, with [sac-md-editor](https://github.com/SACRVM/sac-md-editor) for
notes and [sac-data-grid](https://github.com/SACRVM/sac-data-grid) for
tables, in English and German. It ships as one self-contained binary for
Windows, Linux and macOS and runs under
[Husky](https://github.com/SACRVM/husky), which supervises it and installs
updates from GitHub Releases. It fetches its own HTTPS certificate. About
1,300 tests keep it honest, 154 of them in a real browser. The licence is
AGPL-3.0.

# Where it stands

[v0.6.0](https://github.com/SACRVM/the-fishbowl/releases/tag/v0.6.0) came
out on 2 November, and it is the release with everything above: mail, the
multilingual search, the full calendar and the space apps arrived after
v0.5.0. It is early, and kept small on purpose: external sync, a
scripting layer and a plugin ecosystem were planned and dropped rather
than half-built.

Questions: [mail@sacrvm.dev](mailto:mail@sacrvm.dev).
