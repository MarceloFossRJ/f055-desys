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
diverged. Sizes are tokens as of 2026-10-24, so a dimension written as a literal
in a preview is now a deviation too, though the checker does not yet catch it.

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
| `track` | The off state of a control: empty slider groove, unchecked box |
| `muted-subtle` | Row and disclosure-item fills: ListGroup, Accordion, Alert |
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

**Loading the fonts is the consumer's job.** `tokens.css` declares the families
but fetches nothing, so a project that does not load Roboto and Geist Mono
silently renders in the fallback stack. On web that is one `@import` from Google
Fonts (README has the line, with the exact weights); in KMP, pass real
`FontFamily` values to `F055Theme`; in SwiftUI, bundle the faces or
`Font.custom` falls back. No check catches this — it looks fine, just wrong.

## Radius

| Token | Value | For |
|---|---|---|
| `radius-5` | 5px | Checkboxes, and nothing else |
| `radius-6` | 6px | Chart bars |
| `radius-8` | 8px | Small tiles: swatches, compact grid cells, toolbar icon buttons |
| `radius-10` | 10px | Inner tiles inside a card |
| `radius-14` | 14px | 40px icon tiles, small bordered cards, **overlays** |
| `radius-pill` | 18px | **Every interactive control** |
| `radius-24` | 24px | Cards, panels, sheets, dialogs |
| `radius-full` | 9999px | Circles: radio dots, avatars, status dots |

These are not a scale — the values have no consistent ratio — so they are named
by pixel value, except `pill` and `full`, which name a shape intent.

**A floating panel uses `radius-14` with `shadow-overlay`, not `radius-24` with
`shadow-card`.** Cards and overlays are different surfaces in this system.

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
| `hairline` | An edge with no lift: swatches, chart cells, bordered grid items. The most-used level in the system |
| `card` | Every card and panel |
| `thumb` | A switch knob, an active tab — the card drops, no ring |
| `raised` | Slider thumbs |
| `overlay` | Dropdowns, popovers, menus, tooltips, date pickers |

`hairline`, `card` and `overlay` flip their ring between themes — dark surfaces
need a light edge to read as raised. `thumb` and `raised` do not vary. On web
all of this is automatic via `.dark`.

The ring is part of the shadow, not a CSS border, so it stays outside the box
model and never shifts layout. **Do not reimplement it as a border** unless the
platform forces you to — Compose does, and `F055Elevation` documents that
trade-off. SwiftUI stacks the drops faithfully but draws the ring as an inset
stroke.

## Examples

`examples/dashboard-next/` is the first real screen: a dashboard on Next.js +
Tailwind v4 + lucide-react, modelled on shadcn's dashboard-01. Its README lists
nine findings; four change how you use this system:

- **Tailwind's own `--radius-*`, `--shadow-*` and `--text-*` are now cleared** in
  the `@theme` block. `rounded-xl` used to resolve to Tailwind's 12px, which is
  not an F055 radius. Off-system utilities now produce no CSS at all. Use
  `rounded-5/6/8/10/14/pill/24/full` and `shadow-hairline/card/thumb/raised/overlay`.
- **Data colour is two families now, and they are not interchangeable.**
  `chart-1..5` is **sequential**, for magnitude; `series-1..3` is **categorical**,
  for identity. Picking a `chart-*` step for a second series is the mistake this
  split exists to prevent. (Fixed 2026-10-24; see Data colour below.)
- **`border` is decorative; `border-strong` is operable.** `border` measures
  1.26:1 on card — fine for a separator, invisible as a control outline, and a
  failure of WCAG 1.4.11. Anything a person must see in order to operate it —
  an unchecked checkbox or radio, an unselected segment — takes `border-strong`.
- **Destructive is two tokens.** `destructive` is the FILL and carries
  `destructive-foreground` (white, 4.77:1). `destructive-text` is destructive as
  INK on a neutral surface. One token could not do both: a fill has to be dark
  enough for white to read on it, ink has to be bright enough to read on a dark
  page. Neither goes on `muted` or `accent` — a destructive row rings, never tints.
- **`muted-foreground` is neutral.600 in light, not the extracted neutral.500.**
  Corrected after measurement; it now clears every surface including `input`.

Radius gained a third tier there: **tooltip 8 · panel 14 · card and dialog 24.**

## Size

`--size-4 … --size-64` are the raw steps; `--control-<role>` says what each one
is FOR. **Reach for the role.** A button is `--control-button`, not `--size-32`;
when a density variant arrives, the role moves and the call sites do not.

In Tailwind these are **not** utilities — Tailwind has no `--size-*` namespace,
and routing them through `--spacing-*` would silently redefine `p-32` from 128px
to 32px, which is the same class of bug as the `rounded-xl` one above. Use the
custom-property form:

```
h-(--control-button)   size-(--control-icon)   size-(--control-dot)
```

In the other stacks they are ordinary constants: `F055Control.button` (Kotlin,
Swift), `CONTROL["button"]` (Python, Ruby), `control.button` (JS). React cannot
put a CSS variable in a prop, so `examples/dashboard-next/lib/tokens.ts` imports
`control` from the generated JS for lucide's `size` — that is what the JS output
is for.

Layout widths are deliberately absent. A 256px sidebar or a 1200px column
belongs to a screen, not to the system.

## The native outputs

`dist/kotlin` and `dist/swift` are the two outputs no browser renders and no
test imported, until now. Three things cover them, and they cover different
depths:

- **`check_kotlin_tokens.py`** — every `F055Radius.x`, `F055Control.x`,
  `colors.x`, `type.x` a Kotlin source names exists. Runs anywhere.
- **`check_native_values.py`** — the numbers match `dist/tokens.flat.json`.
  Not circular: the native outputs go through `px()`, dp/sp conversion,
  camelCase renaming and ARGB packing, which is where a unit slip or a dropped
  alpha channel lives. 241 comparisons. Runs anywhere.
- **`examples/login-compose` `:composeApp:desktopTest`** — compiles the
  generated Kotlin, lays the screen out, asserts geometry against the token
  objects, renders PNGs. **Needs Maven Central, so it runs in CI and not in the
  sandbox**, where the egress proxy refuses it.

**Assert against the token, never the number.** `assertDp(F055Control.button, …)`
fails when the token moves; `assertDp(32.dp, …)` does not, which is the whole
point of having a token.

## Contrast is a build gate

`scripts/check_contrast.py` resolves the cascade, composites alpha and measures
every text node against WCAG AA in both themes — across the 40 previews **and
the two built screens**. Standard library only.

**Run it before claiming a component or a screen is done.** It found thirty
failures the first time, across seven components, and every one became a token
change rather than a note in a README.

It runs six self-test fixtures first, and refuses to report a pass for a screen
whose stylesheet yielded almost no colour rules. Both guards exist because the
screens half once reported a clean pass while silently discarding the whole
stylesheet. If you extend the CSS reader, extend the fixtures: a checker that
cannot fail is worse than no checker.

Screens are skipped when their build output is missing, so `check_contrast.py`
alone proves the previews only. The `screens` CI job builds both examples first.

Two of those reversed earlier decisions in this file. That is the point of
measuring: an extracted value is evidence about the reference, not proof that
the reference was accessible.

## Data colour

Two families, two jobs. Do not substitute one for the other.

**`chart-1..5` — sequential.** Magnitude: heatmaps, intensity, a single series.
The dark ramp is the light one **reversed**, so step 1 is always the step nearest
the surface and step 5 always the most prominent. Contrast against the surface
climbs monotonically in both themes (light 1.92 → 8.36, dark 2.15 → 9.34).

**`series-1..3` — categorical.** Identity. Assign **in order, never cycled** —
colour follows the entity, not its rank, so removing a series must not repaint
the survivors.

| slot | light | dark | note |
|---|---|---|---|
| `series-1` | red.700 | red.500 | the only slot with the brand hue |
| `series-2` | neutral.950 | neutral.50 | full ink |
| `series-3` | neutral.500 | neutral.400 | **needs a distinct mark type** |

`series-3` is the same value as `muted-foreground`, which axis labels and legend
text also wear, so hue alone cannot separate it from the chart's own furniture.
Give it a dashed line against a solid, or a hollow marker against a filled one.

**There is no `series-4`.** The palette has one hue. A fourth series folds into
"Other" or becomes a facet.

Validated all-pairs: worst CVD separation 11.3 ΔE deutan (light) and 13.1 (dark)
against a target of 8; normal-vision 21.4 and 24.8 against a floor of 15; all
three slots clear 3:1 on `card` in both themes.

## Components

Forty components are **specified, not implemented**: Button, ButtonGroup,
CloseButton, Toolbar, Badge, Chip, Avatar, Input, Password, PasswordStrength,
Validation, OTPInput, Select, MultiSelect, DatePicker, Slider, Range, Toggle,
Calendar, Card, Table, ListGroup, Carousel, Alert, Accordion, Collapse, Popover,
Menu, Dialog, Drawer, Toast, Placeholder, Spinner, Nav, NavBar, NavOverflow,
Scrollspy, Tabs, Breadcrumb, Pagination.

Twenty-two are extracted. The rest are **derived or composed** — the reference
contains none of them: MultiSelect, NavBar, NavOverflow, Pagination, Collapse,
Alert, Range, PasswordStrength, Validation, OTPInput, Carousel, Scrollspy,
Dialog, Drawer and Toast; DatePicker, Popover and Menu compose extracted parts.
Their READMEs say so at the top.

**Dialog, Drawer and Toast are the thinnest provenance in the system.** The
reference has an "Alert Dialog" button but draws no dialog, and a page-wide
search for a scrim fill returned nothing. Every value in those three is a
decision, not an extraction.
Two rules the overlay set settles, both load-bearing:

- **Radius follows size; shadow follows whether it floats.** Menu, Popover and
  Toast are small, so `radius-14`; Dialog and Drawer are card-sized, so
  `radius-24`. All five take `shadow-overlay`.
- **A scrim is `var(--foreground)` at 50% opacity**, never a new colour. It
  inverts with the theme, which is the point: a dark scrim over a dark page
  does not read.

Motion exists in exactly two components — Spinner and the Placeholder pulse,
both implied by the reference (a rotated arc; bars caught at 0.892/0.881/0.869/
0.857 opacity). There is still no motion token. Everything else is static.

Treat them as provisional against anything a designer produces. Each has a `README.md` under `components/<Name>/`
covering anatomy, variants, which token every part uses, and the decisions that
are easy to get wrong — plus a `preview.html` that renders it from the real
tokens.

Before building any of these in a stack, **read that component's README** and
implement what it says. Do not infer the component from the reference images or
from another design system; the spec records choices that are specific to F055
(the pill on every control, the checkbox being the one square thing, `none` as a
real elevation for inputs, tabular numerals on every numeric cell).

If a component you need is not among these, say so rather than inventing one —
the pattern for adding it is to write the spec first.

**A floating panel (dropdown, popover, menu, tooltip, date picker) uses
`popover` + `radius-14` + `shadow-overlay`.** Not card geometry. Select's README
explains why.

**Every control is `box-sizing: border-box`.** Heights in the specs are the
rendered height, border included. Without it a 32px control with a 1px border
renders at 34px, and one with block padding is far worse.

**There is no error colour beyond a hairline ring.** The reference has no
validation states at all — no red borders anywhere. An invalid field keeps its
`input` fill and gains a 1px `destructive` ring; the message is 14px, never
12px, because `destructive` only reaches AA-large. Every error carries an icon,
so colour is never the only channel. Validation's README has the table.

**There is no success green, and no amber.** A verified field gets a `border`
ring and a tick in `foreground`. A password strength meter carries its meaning
in how many segments are filled plus a word — not in hue. One hue means the
text is the primary channel, not a fallback.

**There is no alert banner, and adding one would break the palette.** The
reference marks severity with an icon, a Badge or an action — never a tinted
fill. A red or amber banner is decorative red, which is the one thing `primary`
may not be. Alert's README has the severity table.

**Chip and Badge look identical and are not the same.** A Badge is a label with
no interaction; a Chip is a value the person set or can remove. If clicking does
nothing, it is a Badge.

**An icon-only button has three shapes depending on where it sits.** In a
toolbar it is `radius-8` with `shadow-hairline` and no fill; alone on a surface
(CloseButton) it is a `muted` pill; inline in text (Breadcrumb overflow) it is a
transparent pill. Toolbar's README has the table.

**Current location is `muted`; a chosen value is `primary`.** Nav, NavBar, Tabs
and Pagination all mark where you are with a `muted` pill and a weight shift.
Calendar marks a selected date with `primary`, because a date is data. Do not
mark a current page in red.

**Nav, ListGroup and Tabs look alike and mean different things.** Nav is
destinations in page chrome; ListGroup is rows inside a page; Tabs switch
between views of one thing. Nav's README has the test.

**Rows separated by space are a ListGroup; rows separated by hairlines are a
Table.** If you are adding a `border-bottom` between list rows, you want a
Table. If you are putting a `muted` pill around each table row, you want a
ListGroup.

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
4. **`space-10` is thin** — two uses, both input inner padding.
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

`Archivo` was declared in the Paper file's font list and used on zero nodes, so
it was never tokenised. It has since been removed from the file, which settles
the question.

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
