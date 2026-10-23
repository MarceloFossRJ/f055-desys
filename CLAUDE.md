# F055 Design System — rules for AI-assisted coding

Read this before writing or changing any UI code in a project that consumes F055.
These rules apply to all four target stacks.

Defined so far: **colour, typography, radius, spacing, elevation.** That is
everything the reference contains. Motion is not defined and cannot be extracted
— the source is a static file. Nor are page containers, grid gutters or
breakpoints. If a task needs one of those, say so rather than inventing values
that will conflict with real tokens later.

## The one rule that matters

**Never write a raw design value in application code.** That means no hex,
`rgb()` or `oklch()`; no Tailwind palette utilities like `bg-red-600` or
`border-neutral-200`; no raw `font-size`, `line-height` or `font-family`; no raw
`border-radius`. Every value comes from a token.

If you find yourself reaching for a literal, the correct move is one of:

1. An existing token already covers it — use that.
2. It is a genuinely new role — add it to the right file under `tokens/`,
   re-run the build, and say so in your summary. Do not quietly inline it.

Grep for violations before you finish:

```sh
# raw colours
grep -rEn '#[0-9a-fA-F]{3,8}\b|rgba?\(|oklch\(' src/ app/
# palette utilities that bypass the semantic layer
grep -rEn '\b(bg|text|border|ring|fill)-(red|zinc|neutral|slate|gray)-[0-9]{2,3}' src/ app/
# raw type, radius, spacing and shadow
grep -rEn '(font-size|line-height|font-family|border-radius|box-shadow)\s*:' src/ app/
grep -rEn '(padding|margin|gap)\s*:\s*[0-9]+px' src/ app/
```

All four should come back empty outside `dist/`.

## Where tokens are defined

Hand-edit only these three:

```
tokens/color.json
tokens/typography.json
tokens/radius.json
tokens/spacing.json
tokens/elevation.json
```

Then regenerate every platform output and validate the result:

```sh
python3 scripts/build_tokens.py   # regenerates everything under dist/
python3 scripts/check_tokens.py   # validates component previews against the tokens
```

Never hand-edit a file under `dist/` — the next build overwrites it, and CI
fails the moment the two diverge.

**Both commands must be run before you finish any change to `tokens/` or
`components/`, and the result committed.** `dist/` is generated *and* committed,
so a token change that is not rebuilt leaves four consuming stacks reading stale
values. The `tokens` GitHub Action enforces this: it rebuilds, fails if `dist/`
comes back dirty, then runs the preview check.

`check_tokens.py` catches two things that fail silently otherwise: a `var()`
pointing at a token that does not exist (CSS drops the declaration and the
element renders with an inherited value, which often looks almost right), and a
raw colour literal in a preview, which means the spec and the tokens have
diverged. It does not check sizes — control geometry has no tokens yet.

## Colour

Pick a token by the *role* it plays, not by how it looks.

| Token | Use for |
|---|---|
| `background` / `foreground` | The page itself and its default text |
| `card` / `card-foreground` | Raised surfaces: cards, panels, sheets |
| `popover` / `popover-foreground` | Overlays: dropdowns, tooltips, menus |
| `primary` / `primary-foreground` | The main action in a view. One per view |
| `secondary` / `secondary-foreground` | Supporting actions sitting next to primary |
| `muted` / `muted-foreground` | De-emphasised fills and secondary text |
| `accent` / `accent-foreground` | Hover and active states on neutral surfaces |
| `destructive` / `destructive-foreground` | Delete, revoke, other irreversible actions |
| `border` | Hairlines and dividers |
| `input` | Form field fills |
| `ring` | Focus rings only |
| `ring-offset` | The gap between a control and its focus ring |
| `chart-1…5` | Data series, in order |

Always pair a surface with its own foreground. `primary-foreground` on
`primary`, never `foreground` on `primary` — the pairings are contrast-checked,
ad-hoc combinations are not.

### Focus states

**Always draw a focus ring with its offset.** On web:

```html
<button class="... focus-visible:ring-2 focus-visible:ring-ring
               focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset">
```

The offset is not cosmetic. `ring` is red and so are `primary` and
`destructive`, so a ring drawn directly on either of those buttons sits at
1.00:1 — completely invisible. The offset puts a 2px band of page colour between
the control and the ring, which is what makes the ring legible on every surface.
A focus state without an offset is a bug in this system.

Use `focus-visible`, not `focus`, so pointer users don't see rings on click.

`muted` and `accent` currently resolve to the same value. They are still two
tokens; use the one that matches intent so they can diverge later.

## Typography

Two families. `sans` is Roboto and carries everything; `mono` is Geist Mono and
appears only at 12px, for code, identifiers and figures that must align in a
column.

Use a **named style**, not a size:

| Style | For |
|---|---|
| `display` | The one big figure on a card. Tabular numerals |
| `heading` | Largest card title |
| `title` | Stat values and prominent section titles |
| `card-title` | Default card and panel title |
| `body` | Introductory copy under a title |
| `text` | The default — table cells, list rows, descriptions |
| `prose` | Long-form paragraphs running several lines |
| `label` | Form field labels and switch titles |
| `button` | All button and tab labels |
| `caption` | Help text, timestamps, axis labels |
| `eyebrow` | Small uppercase label above a title |
| `badge` | Badge and pill text |
| `code` | Identifiers and keys |
| `code-value` | The value beside a code key |
| `numeric` | Figures in meters and dense tables |

The six size steps coincide exactly with Tailwind's own defaults
(`xs`/`sm`/`base`/`lg`/`2xl`/`3xl`); the reference skips Tailwind's `xl` (20px).
So on web you can compose utilities (`text-sm font-medium`) or use the generated
`.type-*` classes. Pick one approach per project and stay with it — mixing both
makes the type layer impossible to audit.

In Compose there is no `textTransform`, so `eyebrow` carries none: uppercase the
string at the call site.

## Radius

| Token | Value | For |
|---|---|---|
| `sm` | 5px | Checkboxes |
| `md` | 8px | Rare; two decorative rects in the reference. Confirm before use |
| `lg` | 10px | Inner tiles: icon squares, avatars, swatches |
| `pill` | 18px | **Every interactive control** |
| `xl` | 24px | Cards, panels, sheets, dialogs |
| `full` | 9999px | Circles: radio dots, avatars, status dots |

`pill` is the system's defining shape. At the reference's control heights
(20/28/32px) 18px exceeds half the height, so controls render as true pills.
A square-cornered button will look wrong in this system.

## Spacing

Eleven steps on a **2px grid** — 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 40. Not a
4px grid: 2, 6, 10 and 14 are all in real use. There is no 32px step; the scale
jumps 24 → 40.

**Tokens are named by pixel value**: `--space-20` is 20px, `F055Space.s20` is
20dp. Each token also records its Tailwind step in `tailwindStep`, because every
value maps exactly onto Tailwind's scale — so on web use the utilities (`p-5`,
`gap-1.5`) and ignore `--space-*` entirely.

Naming by pixel rather than by step is deliberate: step names are fractional
(0.5, 1.5, 2.5) and `.` is not valid in a CSS custom-property identifier without
escaping, which makes `var(--space-1.5)` a footgun.

**20px is the card unit** and the most load-bearing value in the system: it is
both a card's inner padding and the gap between its header, body and footer.
Other conventions: buttons take 12px horizontal padding at every height, table
cells 8px, bordered rows 14px vertical and 16px horizontal.

## Elevation

Four levels. Each is a Tailwind shadow with a **1px hairline ring in front of
it**, and the ring is what carries the look — surfaces here are defined by a
crisp edge, with the drop doing very little.

| Token | For |
|---|---|
| `none` | Inputs and textareas. They sit flush; their fill distinguishes them |
| `card` | Every card and panel |
| `thumb` | A switch knob — the card drops, no ring |
| `raised` | Slider thumbs, and the right choice for popovers and dropdowns |

`card` is the only elevation that changes between themes: its ring flips from
near-black at 5% to near-white at 10%, because a dark surface needs a light edge
to read as raised. On web that is automatic via `.dark`.

The ring is part of the shadow, not a CSS border, so it stays outside the box
model and never shifts layout. **Do not reimplement it as a border** unless the
platform forces you to — Compose does, and `F055Elevation` documents that
trade-off. SwiftUI stacks the drops faithfully but draws the ring as an inset
stroke.

## Components

Seven base components are **specified, not implemented**: Button, Badge, Input,
Card, Toggle, Table, Tabs. Each has a `README.md` under `components/<Name>/`
covering anatomy, variants, which token every part uses, and the decisions that
are easy to get wrong — plus a `preview.html` that renders it from the real
tokens.

Before building any of these in a stack, **read that component's README** and
implement what it says. Do not infer the component from the reference images or
from another design system; the spec records choices that are specific to F055
(the pill on every control, the checkbox being the one square thing, `none` as a
real elevation for inputs, tabular numerals on every numeric cell).

If a component you need is not among the seven, say so rather than inventing
one — the pattern for adding it is to write the spec first.

### Sizes are not tokenised

Control geometry has no tokens: heights (20 / 28 / 32 / 40 / 64), icon sizes
(14 / 16), the switch's 32×20 and its 8px dot, border widths (1 / 2px), and the
focus geometry (2px ring, 2px offset). Every component README lists the literals
it uses under "Not yet tokenised".

When implementing, take those values from the README rather than measuring them
off a preview, and flag it if you find yourself needing one the spec does not
give.

## Per-stack usage

Terse rules below. `README.md` has the same ground with working code examples
per stack — read that if you need the actual wiring rather than the constraint.


**Next.js / Rails / FastAPI+Jinja2 (anything with Tailwind)**

Import `dist/web/tokens.css` once, after `@import "tailwindcss";`. Then:
`bg-background`, `text-muted-foreground`, `border-border`, `font-mono`,
`text-sm`, `rounded-pill`, `rounded-xl`, `shadow-card`, `shadow-raised`, `p-5`,
`gap-1.5`, plus the `.type-*` classes.

Tailwind v3 projects consume `dist/web/tokens.js` from the config instead.

Reach for the server-side modules only when a value must exist outside CSS —
mailers, generated SVG, PDF export, a `theme-color` meta tag:

- **FastAPI/Jinja2** — `dist/python/tokens.py`, via `jinja_globals()`
- **Rails** — `dist/ruby/f055_tokens.rb`, via `F055::Tokens`

Both expose `.css` on a text style, which emits an inline declaration — the only
thing that works in email.

**KMP (Android / iOS / Web)**

Wrap the app in `F055Theme(dark = isSystemInDarkTheme(), sans = …, mono = …)`,
passing real `FontFamily` values. Read colours from `LocalF055Colors.current`,
type from `LocalF055Type.current`, radii from `F055Radius`, spacing from
`F055Space`, elevation from `F055Elevation`.

`MaterialTheme` is wired up (colour scheme, typography, shapes) for Material 3
components, but Material's slots cannot express `muted`, the chart ramp, or
styles like `eyebrow` — go through the F055 locals for those.

`dist/swift/F055Tokens.swift` is only for native SwiftUI surfaces outside the
shared module. Shared UI belongs in Kotlin so both platforms move together.

## Dark mode

Colour is defined in both modes; correct token use makes dark mode work for
free. Type and radius do not vary by mode. Two things to know:

- `primary` gets **darker** in dark mode, not lighter. Faithful to the
  reference — do not "correct" it.
- `border` and `input` are white alphas in dark mode. Keep them as alphas; they
  are designed to composite over both `card` and `background`.
- `elevation.card` is the one shadow that varies by mode. The others do not.

Type, radius and spacing do not vary by mode at all.

## Known issues — read before relying on these

1. **Destructive actions only reach AA-large** (4.36:1 light, 3.48:1 dark).
   Fine for 14px+ semibold button labels, not for small text.
2. **The chart ramp is monochrome red** — adjacent steps separate by only
   1.25–1.35:1. Fine for 2–3 series or sequential data. For 4–5 categorical
   series, add shape, pattern or direct labels.
3. **Two type styles land on fractional pixels.** `prose` is 22.75px and `label`
   is 19.25px, because the reference sets them as percentages (162.5%, 137.5%)
   against 14px. Faithful, but worth normalising — 23/19px, or 24/20px for a 4px
   grid.
4. **`radius-md` (8px) may be incidental** — it appears on two decorative
   rectangles and nothing else.
5. **`space-2.5` (10px) is nearly unused** — two occurrences, both as input
   inner padding. Kept because inputs matter, but it is not a general step.
6. **Compose cannot reproduce the elevation shadows.** Each level is a hairline
   ring plus coloured drops; Compose offers a single `shadow(dp, shape)`. The
   generated values approximate, and the ring becomes a layout-affecting border.

`popover`, `popover-foreground`, `destructive`, `ring` and `ring-offset` are
**derived, not extracted** — the reference never declared them. Their `origin`
field says so. Treat them as provisional.

The dark-mode ring deliberately steps *up* to a brighter red while `primary`
steps *down*. That asymmetry is intentional: it is what clears the 3:1 non-text
minimum on dark surfaces (5.20:1 on background, 3.97:1 on muted). Do not
"correct" it to match primary.

`Archivo` is declared in the Paper file's font list but used on zero nodes. It
is deliberately not a token.

## Why the system looks the way it does

Three facts explain most of the decisions above, and are worth holding when you
are deciding how something should look rather than looking up a value:

- **One hue.** Everything structural is neutral; a single red ramp carries
  brand, action and data. So **red means action or data, never decoration** — a
  red surface is a button you can press or a value you can read. Using it to
  liven up a panel spends the one signal the system has.
- **Everything is a pill.** Controls are fully rounded at every height; cards
  are 24px. A square corner reads as foreign.
- **Edges, not lift.** Surfaces separate with a 1px hairline ring; the drop
  shadow behind it does almost nothing. Reach for a border or a heavier shadow
  and the result stops looking like F055.
