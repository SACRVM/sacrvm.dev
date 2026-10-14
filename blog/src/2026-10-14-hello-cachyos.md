---
title: Hello, CachyOS — new machine, new OS, one move
description: Why I left Windows for CachyOS: a laptop screen I could barely use, a desktop I wanted anyway, and the wish to own my system again — swapped in one go.
---
Two days ago this site moved house. Not the server — GitHub Pages still
serves it — but the machine it is written on. The Windows laptop is
retired, a new AMD desktop runs [CachyOS](https://cachyos.org/), and this
is the first entry written on it.

# Why leave

The short answer: control over my own system. The long answer has a
switch in it.

My laptop is an ASUS gaming machine — sinfully expensive, once. It pairs
an Intel iGPU with an NVIDIA card and a MUX chip, the piece of hardware
that decides which of the two drives the built-in display. Windows and
that wretched MUX stopped getting along, to the point where I could
barely use the laptop's own screen. A machine you have to work around is
not quite your machine anymore.

Linux has a fix for that MUX, down at the kernel level. But Intel
plus NVIDIA on Linux is a chapter of its own, I wanted a desktop again
anyway, and hardware prices were only going one way. So the computer and
the operating system changed in one move.

# The machine

- **AMD all the way.** Ryzen 9 9900X, Radeon RX 9070 XT, 32 GB of RAM.
  The graphics driver ships with the kernel and Mesa — nothing to
  download, nothing to install separately.
- **CachyOS.** Arch underneath, with its own tuned kernel, an LTS kernel
  next to it as the fallback, and package repositories built
  specifically for Zen 4 and Zen 5 CPUs.
- **KDE Plasma on Wayland.** The desktop closest to what a Windows user
  already knows.
- **btrfs with Snapper.** Every package transaction leaves a snapshot
  behind, and the Limine boot menu lists them. A bad update is a reboot
  away from undone.

# Games

Steam runs with CachyOS's own Proton build; Lutris and Heroic cover
everything outside Steam, with Wine underneath. Cyberpunk 2077 and
Onimusha: Way of the Sword are the first two on the drive.

# Work

- **.NET** runs natively — SDK, runtime, the lot. Most of what I build is
  .NET or vanilla JavaScript, and both are at home here.
- **VS Code, git and the GitHub CLI**, the same tools as before.
- **fish** as the shell.
- **The repositories** moved from `D:\repos` to `~/Projects/repos`.

# The rough edges

Not everything is smooth. The UI is fiddly now and then. Discord wants a
different launcher — here it is Vesktop. Some things don't run on the
first try.

None of it was big. And this is where the old line "Linux is for people
who enjoy fixing Linux" stops being true: with Claude in the terminal, an
error message becomes a conversation, and a Linux is tamed in no time.

---

Questions, or your own switch story:
[mail@sacrvm.dev](mailto:mail@sacrvm.dev).

*Mine again.*
