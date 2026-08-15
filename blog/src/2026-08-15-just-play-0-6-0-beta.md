---
title: JUST PLAY 0.6.0 beta — The Library
description: JUST TAG ships — multi-file tag editing, pattern renaming, previewed file operations. Plus the indexed Pre-Cue Finder and one shared track table.
---
[JUST PLAY](https://just.sacrvm.dev/) is the music player for DJs and music
lovers. Drop tracks in, double-click to play. Camelot key, BPM and energy
detected on the spot — no library to build, no sign-in, no nag.

# JUST TAG ships

The tag editor is packaged, installed and on the Start menu for the first
time. It browses the disk, not a library — the tool for a download that just
landed somewhere no index has seen.

- Multi-file editing, a tick per field. Fields the selection disagrees on say
  *different values*, so nothing is flattened by accident.
- `%artist% - %title%` builds a file name from tags, or reads tags out of a
  name. Both directions, one language.
- Move, copy and delete, every one previewed. There is no overwrite, ever — a
  taken name is a collision, and the answer is "leave both alone" or
  "keep both".
- Search that reads as a sentence: sixteen fields, seven comparisons,
  including *is empty*. "Genre is empty" is the one that finds the damage.

# Also in 0.6

- The Pre-Cue Finder gained the index. Folders paint instantly and verify
  behind you, and you can filter across every playlist below a folder.
- One track table across queue, finder and JUST TAG — same rows, same widths,
  sized to what is actually in them.
- JUST STREAM shows the listener count, with no admin password stored.

# Still pre-1.0

What is not done, said up front:

- Nothing watches your library folder yet. The index catches up when you
  press Scan.
- A scan indexes, it does not analyse. Use right-click *Analyse*, or the CLI.
- macOS and Linux share the codebase and are not validated.

---

One installer, four tools, one shared runtime: JUST PLAY, JUST STREAM,
JUST TAG and the headless CLI. Per-user, no admin prompt.

[Download 0.6.0-beta.1](https://github.com/SACRVM/just-play/releases/tag/v0.6.0-beta.1)
— feedback and bug reports to [info@sacrvm.dev](mailto:info@sacrvm.dev) or the
[issue tracker](https://github.com/SACRVM/just-play/issues).

*From DJs to DJs.*
