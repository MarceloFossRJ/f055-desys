# Dashboard — Next.js

The first real screen built on F055. Modelled on
[shadcn's dashboard-01](https://ui.shadcn.com/view/new-york-v4/dashboard-01),
rebuilt with this system's tokens and specs.

```bash
npm install
npm run dev     # http://localhost:3000
npm run build   # static export to out/
```

Next.js App Router · Tailwind v4 · lucide-react · TypeScript.

## Why this stack first

`dist/web/tokens.css` is already shadcn v4 semantic naming with `@theme inline`,
so it drops into Tailwind v4 with **no adapter**. `app/globals.css` imports the
real generated file — not a copy — so the example cannot drift from the source:

```css
@import "tailwindcss";
@import "../../../dist/web/tokens.css";
```

That import needs `turbopack.root` set to the repo root in `next.config.ts`;
without it Turbopack rejects the file as "outside configured roots" and you are
pushed into vendoring a copy, which is exactly the drift this guards against.

Lucide turned out to already be the system's icon spec without anyone saying so:
24 viewBox, `stroke-width: 2`, round caps, `currentColor` — what every
`preview.html` hand-draws.

## What this exposed

Nine findings. The point of building a real screen was to produce this list.

### 1. Tailwind's own scales silently shadowed ours — fixed

`rounded-xl` resolved to **Tailwind's 12px**, which is not an F055 radius at all
(we have 10 and 14). The generated header comment even recommended it. Our
`--radius-5…24` coexisted with Tailwind's `--radius-sm…3xl` and the wrong one won
on a familiar name.

Fixed in `scripts/build_tokens.py`: the `@theme` block now clears
`--radius-*`, `--shadow-*` and `--text-*` before declaring ours. An off-system
utility now produces **no CSS at all** — a loud failure instead of a plausible
wrong value. `rounded-xl` and `shadow-md` are now dead names.

This was the most dangerous thing found, because nothing would ever have caught
it: the page renders, it just renders a radius the system does not contain.

### 2. The chart ramp is effectively one colour — FIXED

`chart-1…5` are `red.300 → red.800` — a **sequential** ramp doing **categorical**
work. Measured against the 3:1 non-text minimum, on `card`:

| token | light | dark |
|---|---|---|
| `chart-1` | **1.87 ✗** | pass |
| `chart-2` | pass | pass |
| `chart-3` | pass | pass |
| `chart-4` | pass | **2.71 ✗** |
| `chart-5` | pass | **2.08 ✗** |

Only `chart-2` and `chart-3` clear both themes, and they are adjacent reds —
indistinguishable as categories. **Five tokens, one usable mark colour.**

The chart therefore uses one red (`chart-3`) plus `muted-foreground`, with the
comparison series as a *dashed line* against a *filled area*. Different mark
types, so identity never rests on hue alone.

**Fixed 2026-10-24**, by splitting the two jobs apart rather than patching one
ramp. `chart-1..5` is now explicitly **sequential**, and the dark ramp is the
light one reversed, so step 1 is always nearest the surface: contrast climbs
1.92 → 8.36 in light and 2.15 → 9.34 in dark. A separate **categorical** set,
`series-1..3`, carries identity — brand red, full ink, muted ink — validated
all-pairs at 11.3 / 13.1 ΔE CVD separation with all three clearing 3:1 in both
themes.

This chart now uses `series-1` and `series-3`. `series-3` is the same value as
`muted-foreground`, which the axis labels also wear, so it keeps the dashed
mark — the token's own note requires it.

### 3. `muted-foreground` on `muted` fails AA in light

4.35:1 — under 4.5. On `card` the same ink is 4.74:1 and passes. This is a very
common pair: any secondary text inside a muted container.

The tab strip was where the example hit it. Fixed by moving the strip onto
`card` with a hairline border, which lets the **selected** tab be the `muted`
one — the system's own rule for current location, and better design than what
it replaced.

**Recommended fix:** either a darker light-mode `muted-foreground`, or document
the pair as prohibited.

### 4. No token outlines a small control in light mode

An unchecked Checkbox outlined in `border` is **1.03:1** against a light row —
invisible. There is nothing between `border` (1.03) and `muted-foreground`
(3.89) to reach for, so the Checkbox uses `muted-foreground`, which is heavier
than the reference's look.

**Recommended fix:** a control-border token that clears 3:1 in both themes.

### 5. Radius has three tiers, not two

The overlay batch recorded "radius follows size": `radius-14` for small floating
panels, `radius-24` for card-sized. Building Tooltip showed a third tier — at
28px tall, `radius-14` is a full pill. Tooltip uses `radius-8`.

So: **tooltip 8 · panel 14 · card and dialog 24.**

### 6. Light mode has no canvas separation

`background` and `card` are both white. The entire page layout rests on
`shadow-card`'s hairline ring. It works and looks clean, but there is no second
surface to fall back on — and `muted` as a canvas inverts in dark, where it is
*lighter* than `card`.

### 7. Size tokens, again — FIXED

Every control dimension here used to be a literal. **Fixed 2026-10-24**:
`tokens/size.json` has twelve steps and eighteen named roles, drawn from a
frequency tally across all forty previews (16px appears 124 times, 20px 65,
32px 40).

In Tailwind they are not utilities — there is no `--size-*` namespace, and
routing them through `--spacing-*` would silently redefine `p-32` from 128px to
32px, the same class of bug as finding 1. So the call sites use the
custom-property form, `h-(--control-button)`.

React cannot put a CSS variable in a prop, so `lib/tokens.ts` imports `control`
from the generated `dist/web/tokens.js` for lucide's `size`. That is what the JS
output is for, and this is the first thing to use it.

Layout widths — the 256px sidebar, the 1200px column — stay literal on purpose.
They belong to this screen, not to the system.

### 8. The font gap is real

`tokens.css` names the families and cannot load them. Bridged here with
`@fontsource/roboto` and `@fontsource/geist-mono`, self-hosted so the example
needs no network at build or run time.

### 9. No motion tokens

`transition-colors` and `duration-200` are literals. Spinner and the Placeholder
pulse already hard-code durations. Three call sites is now enough to design a
small motion scale from.

## Components this needed that the system does not have

Built here first, so their specs can be written from something that works rather
than from a screenshot:

| Component | Why nothing existing covered it |
|---|---|
| **Sidebar** | Nav is a vertical item list, NavBar a horizontal top bar. Neither is the app shell: groups, a collapsed icon rail, a footer identity block. |
| **Chart** | Nothing existed. |
| **Checkbox** | Toggle is a switch; Menu has a checkbox *item*. No standalone box. |
| **Tooltip** | Popover is interactive and dismissible. A tooltip is neither, and a collapsed rail cannot work without one. |

One thing the Sidebar taught: **the rail must not hide its own escape hatch.**
Collapsed, the sidebar's own toggle is gone, so the header carries one too.

## What held up

- The token file dropped into Tailwind v4 with zero adaptation.
- `track` and `muted-subtle`, both added speculatively, earned their place —
  `track` on the unchecked Checkbox, `muted-subtle` on table row hover and
  selection.
- "Current location is `muted`, a chosen value is `primary`" settled the active
  state for the sidebar, the tabs and the time-range group without a decision
  each time.
- Having no status palette forced the status column into dots plus words, which
  is more accessible than the colour-coded original.

## Deliberate exemption

Table row hairlines measure 1.26:1 (light) and 1.33:1 (dark), below the 3:1
non-text minimum. WCAG 1.4.11 covers non-text content *required* to understand
the interface; row separators are decorative, and row structure is carried by
position and content. Borders in this system are deliberately faint and are not
a load-bearing affordance.
