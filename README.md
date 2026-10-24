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

## Using the tokens

Pick a token by the **role** it plays, not by how it looks.

Always pair a surface with its own foreground — `primary-foreground` on
`primary`, `card-foreground` on `card`. Those pairings are contrast-checked;
ad-hoc combinations are not. Putting plain `foreground` on `primary` is the most
common way to break this system.

One `primary` per view. If two things on screen are both primary red, neither
reads as the main action.

`muted` and `accent` currently resolve to the same value. They are still two
tokens — use the one that matches intent, so they can diverge later without a
find-and-replace.

Use a **named type style** (`label`, `button`, `eyebrow`, `numeric`) rather than
a raw size. The style bundles family, size, line height, weight and numeral
behaviour, which is what keeps a label in a Rails form and a label in a Compose
screen looking like the same thing.

The chart ramp runs light to dark, `chart-1` through `chart-5`. Use it in order.

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

**Radius is eight values, not a scale.** 5, 6, 8, 10, 14, 18, 24 and full have
no consistent ratio, so they are named by pixel value — with `pill` (18px) and
`full` keeping intent names, because those denote a shape rather than a size.

**Elevation is six levels, and `hairline` is the most-used of all** — a 1px ring
in the border colour with no drop, for elements that need an edge but no lift.
It is a shadow rather than a border so it costs no layout.

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

**`muted-subtle` is `muted` at 50%** — the fill under ListGroup rows, Accordion
items and Alerts. Measured at `#F5F5F580` light and `#26262680` dark; one step
lighter than `muted`, which is what stops a stack of rows reading as a wall of
grey.

**`track` was the first colour token added after the first pass.** The empty half
of a slider and the fill of an unchecked checkbox use `#E5E5E5E6` light and
`#FFFFFF22` dark — a third alpha ramp, distinct from both `border` (10% dark)
and `input` (15%). The values are extracted; only the name is mine.

**Provenance is recorded per token.** `extracted` means measured from the file;
`derived` means I filled it in. Five colour tokens are derived — `popover`,
`popover-foreground`, `destructive`, `ring` and `ring-offset`.

**Focus states need the offset.** `ring` is red, and so are `primary` and
`destructive`, so a ring drawn straight onto either of those buttons sits at
1.00:1. `ring-offset` puts a band of page colour in between. Every focus state
uses both tokens; one without the other is a bug.

## Consuming F055 in a project

Everything under `dist/` is generated from `tokens/` by
`python3 scripts/build_tokens.py`. Nothing under `dist/` is edited by hand.

**Never write a raw design value in application code** — no hex, `rgb()` or
`oklch()`; no Tailwind palette utilities like `bg-red-600`; no raw `font-size`,
`line-height`, `font-family`, `border-radius` or `box-shadow`. If no token fits,
add one under `tokens/` and rebuild rather than inlining a literal.

### Focus states

Every focusable control draws both tokens, always together:

```html
<button class="... focus-visible:ring-2 focus-visible:ring-ring
               focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset">
```

Or in hand-written CSS, as two shadows so the ring stays outside the box model:

```css
box-shadow: 0 0 0 2px var(--ring-offset), 0 0 0 4px var(--ring);
```

`:focus-visible`, not `:focus`, so pointer users don't see rings on click.

### TypeScript · Next.js · Tailwind

Tailwind v4 — import the stylesheet once, after `@import "tailwindcss";`:

```css
@import "tailwindcss";
@import "../design-system/dist/web/tokens.css";
```

Every token is then a utility: `bg-background`, `text-muted-foreground`,
`border-border`, `ring-ring`, `fill-chart-1`, `font-mono`, `text-sm`,
`rounded-pill`, `rounded-xl`, `shadow-card`, `shadow-raised`.

Spacing needs no configuration — the eleven steps are exactly Tailwind's own, so
`p-5` is the card padding and `gap-1.5` the button gap.

**The stylesheet declares the font families but does not load them.**
`--font-sans` and `--font-mono` name Roboto and Geist Mono with fallback stacks;
nothing fetches the faces. Without this line you silently get the fallbacks,
which is a visible downgrade that no check will catch:

```css
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap');
```

Those are the only weights the system uses — Roboto 400/500/600, Geist Mono
400/500. Self-host instead if you prefer; the point is that loading is the
consumer's job on every platform, KMP and SwiftUI included.

The file also defines `.type-*` classes (`type-label`, `type-display`,
`type-numeric`) that bundle family, size, line height, weight and numerals. In a
template those save repeating four utilities on every label; in React, composing
utilities or wrapping a component is equally fine. Pick one approach per project
— mixing both makes the type layer impossible to audit.

Tailwind v3 projects consume `dist/web/tokens.js` from the config instead.

### Python · FastAPI · Jinja2 · Tailwind

Styling goes through the same Tailwind classes. Use `dist/python/tokens.py` only
when a value must exist server-side — mailers, generated SVG or charts, PDF
export, a `theme-color` tag:

```python
from design_system.tokens import jinja_globals
templates.env.globals.update(jinja_globals())
```

```jinja
<meta name="theme-color" content="{{ colors.light.background.hex }}">
<span style="{{ type.label.css }}">Email</span>
```

`.css` on a text style emits an inline declaration — the only thing that works
in email, where classes do not apply.

### Ruby on Rails · Tailwind

Same split. Views use the Tailwind classes; `dist/ruby/f055_tokens.rb` covers
mailers, generated SVG and PDF export:

```ruby
F055::Tokens.scheme(:dark)[:background].hex  # => "#0A0A0A"
F055::Tokens::TYPE[:label].css
F055::Tokens::RADIUS[:pill]                  # => "18px"
```

Unknown scheme names fall back to light rather than raising, so a bad param
cannot take a page down.

### KMP · iOS · Android · Web

```kotlin
F055Theme(dark = isSystemInDarkTheme(), sans = robotoFamily, mono = geistMono) {
    // LocalF055Colors.current, LocalF055Type.current, F055Space, F055Radius
}
```

Pass real `FontFamily` values — the defaults fall back to system faces, which is
a visible downgrade. `MaterialTheme` is wired up (colours, typography, shapes)
for Material 3 components, but Material's slots cannot express `muted`, the
chart ramp, or styles like `eyebrow`; go through the F055 locals for those.

Two platform caveats: Compose has no `textTransform`, so `eyebrow` carries none
— uppercase at the call site. And `F055Elevation` only approximates the
shadows, drawing the hairline ring as a border that affects layout.

`dist/swift/F055Tokens.swift` is for native SwiftUI surfaces outside the shared
module — widgets, App Clips, a host screen. Shared UI belongs in Kotlin so both
platforms move together.

### AI-assisted coding

`CLAUDE.md` carries these rules written for an agent, plus the greps that catch
violations and the two commands that must be run after any token change.

## Open decisions

1. **Destructive and primary are both red.** The reference never defined a
   destructive colour — its "Danger Zone" row uses plain `foreground` — and
   because the brand *is* red, a destructive button
   currently looks much like a primary one. The current value reaches AA-large
   only. If delete actions need to be unmistakable, a non-red destructive —
   amber or orange — is the stronger call.

2. **The chart ramp is a single red ramp.** Adjacent steps differ by 1.25–1.35:1.
   Good for sequential data, weak for 4–5 categorical series.

3. **Two type styles are fractional.** `prose` at 22.75px and `label` at
   19.25px. Round to 23/19, or normalise to 24/20 for a 4px grid.

4. **`space-10` is thin** — two uses, both as input inner padding. Kept because
   inputs matter, but it is not a general step.

5. **Compose cannot reproduce the elevation shadows.** Each level is a hairline
   ring plus coloured drops; Compose offers a single `shadow(dp, shape)`. The
   Kotlin output approximates and turns the ring into a border, which — unlike
   the CSS version — affects layout. SwiftUI reproduces the drops faithfully but
   draws the ring as an inset stroke.

## Sizes

`tokens/size.json` — twelve steps (4, 6, 8, 12, 14, 16, 20, 24, 28, 32, 40, 64)
and eighteen named roles on top of them. The steps are named by pixel value, as
radius and spacing are, because they form no consistent ratio; the roles are the
counterpart to radius's `pill`/`full`, so a button does not have to be
remembered as 32.

They were prose under `controlHeights` in `tokens/radius.json` from the first
extraction, flagged as "not yet tokens" in every README since. The values come
from a frequency tally across all forty previews: 16px appears 124 times, 20px
65, 32px 40, 28px 24, 24px 18. 36, 48 and 80 appear once or twice and were left
out.

Reach for the role, not the step — `--control-button`, not `--size-32`. When a
density variant arrives the role moves and the call sites do not.

Layout widths are deliberately absent. A 256px sidebar or a 1200px content
column belongs to a screen, not to the system; see below on why no containers or
breakpoints were taken from the reference.

## Data colour

Two families doing two different jobs. `chart-1..5` is a **sequential** ramp for
magnitude — the dark ramp is the light one reversed, so step 1 is always nearest
the surface and step 5 always the most prominent, in both themes. `series-1..3`
is the **categorical** set for identity: brand red, full ink, muted ink.

The split came out of building the dashboard. The five chart tokens were
theme-invariant and, measured against 3:1, yielded exactly one usable mark
colour. A one-hue palette cannot do categorical work by hue, so the third slot
carries a hard requirement — a distinct mark type — and there is no fourth.

## Examples

`examples/dashboard-next/` is the first screen actually built on this system — a
dashboard on Next.js + Tailwind v4 + lucide-react, modelled on shadcn's
dashboard-01. `npm install && npm run dev` inside that folder.

It exists to be a test, and it found things. The token file dropped into
Tailwind v4 with no adapter, and `track` and `muted-subtle` both earned their
keep. But `rounded-xl` turned out to resolve to Tailwind's own 12px rather than
any F055 radius — the generator now clears Tailwind's radius, shadow and text
scales so an off-system utility fails loudly instead of quietly. The five chart
tokens turned out to yield one usable colour once measured against 3:1 in both
themes. `muted-foreground` on `muted` fails AA in light. And `border` is too
faint to outline a checkbox. That example's README has the full list with the
measurements.

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

The overlay set — Menu, Dialog, Drawer, Toast, on top of Popover — settles two
rules the rest of the system depends on. **Radius follows size; shadow follows
whether it floats**: Menu, Popover and Toast take `radius-14`, Dialog and Drawer
take `radius-24`, all five take `shadow-overlay`. And a **scrim is
`var(--foreground)` at 50% opacity**, never a new colour, so it inverts with the
theme — a dark scrim over a dark page does not read as a scrim at all.

Those three overlays are also the weakest provenance here. The reference has an
"Alert Dialog" button and draws no dialog; a page-wide search for a scrim fill
found nothing. Treat Dialog, Drawer and Toast as proposals.

Motion arrived with this set, in exactly two places. Spinner needs it to be a
spinner, and the reference's skeleton bars carry opacities of 0.892, 0.881,
0.869 and 0.857 — one staggered pulse caught mid-frame, which is the only
animation the file implies anywhere. Both are hard-coded durations; there is
still no motion token, and two components is not yet enough to design one from.

What is *not* there, and should not be invented from this reference, is layout:
the source is a 3000px presentation artboard with seven columns of 375px
specimen cards. That is how a designer arranged a catalogue for viewing, not an
application layout. Containers, gutters and breakpoints belong to the first real
screen in a real stack.

## Verifying against the source

Light reference: artboard `D5-0` · Dark: `3JI-0` · Palette cards: `1O9-0` /
`2LV-0` · Type specimen: `1PS-0`, in Paper file `01M5M3N461Y0VSS854R6G5S86K`.

`Archivo` was declared in that file's font list and used on zero nodes, so it was
never tokenised. It has since been removed from the file, which settles it.

The file also had a fifth artboard, "Hello World" (1440×900) — the one place a
horizontal nav bar would plausibly have lived. It was deleted before it could be
examined, which is why NavBar is derived rather than extracted.

The browsable version of this system — the same tokens with live component
previews in both themes — is published as a Claude design-system artifact. Its
prose is a presentation layer; this file and `CLAUDE.md` are the source of
truth, and the artifact's token data comes from `dist/artifact/tokens.json`.
