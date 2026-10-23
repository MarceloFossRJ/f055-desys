# F055 Design System

Tokens extracted from the Paper file **F055 Desys 1**, generated out to four
target stacks.

**Defined: colour, typography, radius, spacing, elevation** — everything the
reference contains. Motion is not defined and cannot be extracted from a static
file; nor can page containers, grid gutters or breakpoints. Components are not
started — see the note at the end.

Focus states are resolved: `ring` plus `ring-offset`, passing in both modes.

## Layout

```
tokens/color.json          <- hand-edit
tokens/typography.json     <- hand-edit
tokens/radius.json         <- hand-edit
tokens/spacing.json        <- hand-edit
tokens/elevation.json      <- hand-edit
components/<Name>/         <- component specs + live previews (hand-written)
scripts/build_tokens.py    <- regenerates everything below
dist/
  web/tokens.css           <- Tailwind v4 (Next.js, Rails, FastAPI+Jinja2)
  web/tokens.js            <- Tailwind v3 config fallback
  python/tokens.py         <- FastAPI + Jinja2
  ruby/f055_tokens.rb      <- Rails
  kotlin/F055Colors.kt     <- KMP: colours + theme wrapper
  kotlin/F055Type.kt       <- KMP: type styles
  kotlin/F055Shapes.kt     <- KMP: radii
  swift/F055Tokens.swift   <- native SwiftUI surfaces only
  artifact/tokens.json     <- feeds the browsable design system page
  tokens.flat.json         <- resolved values, for any other consumer
CLAUDE.md                  <- rules for Claude CLI and other AI-assisted coding
```

## Build

```sh
python3 scripts/build_tokens.py
```

No dependencies — standard library only.

## What the system is

A near-monochrome system. Everything structural is neutral grey; a single red
ramp carries brand, action and data. There is no second hue.

The practical consequence: **red means action or data, never decoration.** A red
surface here is a button you can press or a value you can read.

Three more things define the look. Every interactive control is a **pill** —
18px radius against control heights of 20–32px, so they render fully rounded;
cards sit at 24px. The type scale is **tight**: six steps, 12 through 30px, with
no 20px step at all. And surfaces are defined by a **crisp 1px edge** rather
than by lift — every elevation is a hairline ring with a drop shadow doing very
little behind it.

## Design decisions worth knowing

**Naming follows shadcn/ui v4** for colour. The reference already used those
names, so the web output drops into any shadcn project unchanged, and the Kotlin
and Swift outputs stay recognisable to anyone who has seen the web side.

**The reference is built on Tailwind primitives throughout.** All six type steps
match Tailwind's defaults exactly. So do all eleven spacing steps (0.5 through
10). So do the shadows — `card` and `thumb` are `shadow-sm`, `raised` is
`shadow-md`, each with a ring added. A Tailwind project therefore needs almost
no configuration; everything is written out anyway so the other three stacks
share the same numbers.

**Spacing is a 2px grid, not 4px.** 2, 6, 10 and 14 are all in real use, and
there is no 32px step — the scale jumps 24 → 40. 20px is the card unit: both a
card's inner padding and the gap between its parts. Tokens are named by pixel
value (`space-20`), not by Tailwind step, because step names are fractional and
`var(--space-1.5)` is not a valid identifier without escaping; each token
records its Tailwind step in a field instead.

**Values are faithful to the reference, including its quirks.** `primary` is
darker in dark mode than light. `secondary` sits on a zinc ramp while everything
else is neutral. Two type styles land on fractional pixels. All preserved, all
flagged.

**Provenance is recorded per token.** `extracted` means measured from the file;
`derived` means I filled it in. Five colour tokens are derived — `popover`,
`popover-foreground`, `destructive`, `ring` and `ring-offset`.

**Focus states need the offset.** `ring` is red, and so are `primary` and
`destructive`, so a ring drawn straight onto either of those buttons sits at
1.00:1. `ring-offset` puts a band of page colour in between. Every focus state
uses both tokens; one without the other is a bug.

## Open decisions

1. **Destructive and primary are both red.** The reference never defined a
   destructive colour, and because the brand *is* red, a destructive button
   currently looks much like a primary one. The current value reaches AA-large
   only. If delete actions need to be unmistakable, a non-red destructive —
   amber or orange — is the stronger call.

2. **The chart ramp is a single red ramp.** Adjacent steps differ by 1.25–1.35:1.
   Good for sequential data, weak for 4–5 categorical series.

3. **Two type styles are fractional.** `prose` at 22.75px and `label` at
   19.25px. Round to 23/19, or normalise to 24/20 for a 4px grid.

4. **`radius-md` (8px) may be incidental** — two decorative rectangles use it
   and nothing else does. `space-2.5` (10px) is similarly thin, with two uses.

5. **Compose cannot reproduce the elevation shadows.** Each level is a hairline
   ring plus coloured drops; Compose offers a single `shadow(dp, shape)`. The
   Kotlin output approximates and turns the ring into a border, which — unlike
   the CSS version — affects layout. SwiftUI reproduces the drops faithfully but
   draws the ring as an inset stroke.

## Sizes are not tokenised

Writing the seven component specs exposed one real gap: control geometry has no
tokens. Heights, icon sizes, the switch's dimensions, border widths and the
focus geometry are all literals in the specs, listed under "Not yet tokenised"
in each component README.

Survivable for one implementation, a liability across four — it is exactly the
kind of value that drifts when the same component is written in Compose and in
React by different hands. Worth adding before the second implementation.

## On components

Tokens travel across all four stacks. Components do not: a button in Jinja2,
ERB, React and Compose is four implementations. What can realistically be shared
is this token layer plus a written spec per component — anatomy, states, and
which tokens each part uses — with four thin implementations under it.

The reference's control geometry is already recorded in `tokens/radius.json`
under `controlHeights`, and the component-level spacing conventions are in
`tokens/spacing.json` — buttons at `px-3`, table cells at `p-2`, bordered rows
at `py-3.5 px-4`. Together those are the raw material for that spec whenever it
gets written.

What is *not* there, and should not be invented from this reference, is layout:
the source is a 3000px presentation artboard with seven columns of 375px
specimen cards. That is how a designer arranged a catalogue for viewing, not an
application layout. Containers, gutters and breakpoints belong to the first real
screen in a real stack.

## Verifying against the source

Light reference: artboard `D5-0` · Dark: `3JI-0` · Palette cards: `1O9-0` /
`2LV-0` · Type specimen: `1PS-0`, in Paper file `01M5M3N461Y0VSS854R6G5S86K`.
