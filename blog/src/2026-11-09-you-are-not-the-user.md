---
title: rams-design-for-use — teaching an AI that it is not the user
description: A Claude Code plugin that hands Dieter Rams' way of thinking to an AI: you design for other people, never for yourself or the AI. Why an AI needs that reminder, what Braun teaches software, and how a rulebook became a way of thinking — tried out on this site.
---
[rams-design-for-use](https://github.com/SACRVM/rams-design-for-use) is a
Claude Code plugin with one skill. It applies Dieter Rams' design
philosophy to how software is used — apps, tools and games alike, through
every channel people operate them with: mouse, keyboard, controller, pen,
touch, voice. Not only the visible interface. Its one idea fits in a line:
you design for other people, never for yourself or for the AI.

Today it reviewed this site. More on that below.

# You are not the user

Every designer knows the trap: you know how the thing works, so it looks
obvious to you. An AI walks into that trap at full speed. It knows every
term in the code, because it read the code. It knows where everything is,
because it put it there. It is never tired, never interrupted, never on a
phone in the sun. And it looks at the result on its own screen, with its
own input, in its own language.

The people who will use the result have none of that. They arrive tired,
distracted, halfway through something else, with other eyes, other hands
and other words. Rams said it in a speech in 1976: "You cannot understand
good design if you do not understand people."

So the skill makes the AI do what a good designer does on purpose:

- **Ask who else will operate it**, and when, and why. If nobody can be
  named, assume the least favourable realistic person — first time, tired,
  no shortcuts — and say so.
- **Say every assumption out loud**, so the person in front of the screen
  can correct it.
- **Walk through it as them** — keyboard only, on a phone, by the names a
  screen reader would read — instead of judging from the code.
- **Treat their stumbling as a finding.** If the person working with the
  AI gets stuck, the design is wrong, not the person.

# What Braun teaches software

Rams designed radios, calculators and shelves, not software, and he wrote
no rules for screens. What crossed over is a way of thinking; Apple under
Jony Ive carried it into digital products most visibly. The skill hands
that thinking to an AI, and its reference file on Braun reads like a
manual for software:

- **A signal only where it tells you something.** Braun's palette was greys,
  whites and black. On the ET 66 calculator one key is yellow: the equals
  key, the function people use most. Colour, sound and vibration are
  signals, and signals are scarce.
- **There when needed, in the background otherwise.** Rams wanted his
  shelving system to behave like a good butler. An interface serves; it
  does not perform.
- **Design was company policy, not decoration.** At Braun, how a product
  was used was decided from the first decision on, not painted on at the
  end. In software that team is the AI and the person in front of the
  screen.
- **Not set in stone.** Rams himself asked each generation to review his
  principles. The skill is such a review, for software.

The plugin's icon is nine keys, the last one yellow — after the ET 66.

# From a rulebook to a way of thinking

The first version was a rulebook: Rams' ten principles translated into
UI rules for screens, dialogs and menus. The published version keeps the
ten principles, but it is something else:

- **No fixed values.** No pixel sizes, no timings, no colour tables. Good
  values follow from the people and their situation; platform guidelines
  and accessibility standards are the floor, not the goal.
- **Every channel, not just the screen.** Keyboard, controller, pen, touch
  and voice, and also what people hear, feel and type outside any window.
- **Together with the person in front of the screen.** The AI states its
  assumptions where they can be corrected, hands over something to try,
  and takes the answer seriously.

The rulebook was too specific. It prescribed things that should not be
prescribed: good design is not 20px of spacing here and 20px there. What I
wanted was awareness — of design, and of how things are operated.

It went through several rounds of rework and was reviewed by Fable, Grok
and an outside reader before it became a plugin and a marketplace.

# Tried on this site

Today the skill reviewed sacrvm.dev, keyboard and phone included. What it
found was not taste:

- **Grey text below what eyes can read.** The navigation, the footer and
  every date were ink at 45 %: 2.65:1 against the celadon, in 10px. All
  text is now at least 70 % ink.
- **Focus nobody could see.** On the map, the box the keyboard was on
  looked exactly like its eleven lit neighbours.
- **No way to write to me** — except the imprint. Home and CV now have
  one main action: "Write to me".
- **A third of the map on a phone**, with its centre off screen. Below
  720px it is a list now.
- **A card that blinked on hover.** I noticed it, not the AI. Measured,
  the fade carried text and background through the same grey at the same
  moment, and the card went blank for a frame. The swap is instant now.

And the site got its ET 66 key. It was two colours and nothing else; now
it has one signal, a red-orange, used only for the element the keyboard
is on and for the one thing each page is for. It is not yellow — what
matters is that there is only one.

One change was mine, against the skill's taste: links that leave the site
open a new tab. A new tab takes the Back button away, so the skill made
each of them say so, with an arrow for the eye and words for a screen
reader. The person's request wins; the tension gets named.

# Install

In Claude Code (2.1.275 or later):

```
/plugin install rams-design-for-use --marketplace SACRVM/rams-design-for-use
```

On older versions, add the marketplace first, then install:

```
/plugin marketplace add SACRVM/rams-design-for-use
/plugin install rams-design-for-use@rams-design-for-use
```

The skill is licensed CC BY 4.0. Questions and findings:
[mail@sacrvm.dev](mailto:mail@sacrvm.dev) or the
[repository](https://github.com/SACRVM/rams-design-for-use).

*Obvious to whom?*
