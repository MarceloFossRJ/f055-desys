# Spinner

A 270° arc that rotates. The one place the reference implies motion.

## Anatomy

| Part | Token |
|---|---|
| Size | 16px standard, 12px inline in small text |
| Stroke | 2px (2.5px at 12px), `currentColor` |
| Colour | `foreground`; `primary-foreground` on a primary button |
| Tile form | 40×40 `muted` at `radius-14`, icon 16px |

The glyph is a single arc — `M21 12a9 9 0 1 1-6.219-8.56` — open at roughly 90°,
with round caps. Not a ring with a gap, not a segmented circle.

## It inherits colour

`stroke: currentColor` with the colour set on the wrapper. That is what lets the
same spinner sit in a primary button (`primary-foreground`), on a page
(`foreground`), or inside a muted tile without a variant for each.

## The tile form is the reference's own

The reference puts the spinner in a 40×40 `muted` tile at `radius-14`, above a
title and a description — the same tile that carries the icon in every empty
state. Use that form for a whole-card or whole-page load, and the bare 16px arc
inline.

## Motion, in a system that defines none

The reference is a static file and the tokens define no motion. The spinner is
the one component where that is not sustainable — a stationary arc is not a
spinner, it is a comma.

So: **one second, linear, infinite.** Linear because any easing makes a
continuous rotation visibly stutter at the loop point.

Always honour `prefers-reduced-motion: reduce` by stopping the animation. A
stopped arc plus its label still communicates; a spinning one can be
genuinely unpleasant for some people.

```css
@media (prefers-reduced-motion: reduce) { svg { animation: none; } }
```

## Guidelines

A spinner alone says "wait" and nothing else. Pair it with a word — "Saving…",
"Checking" — wherever there is room.

**Prefer a Placeholder skeleton for content that has a shape.** A spinner is for
an action with no layout to predict; a list or a card that is about to appear
should show its own outline instead.

Give it `role="img"` and an `aria-label`, or `aria-hidden` when adjacent text
already says what is happening — a button reading "Saving…" does not need the
spinner announced as well.

Do not show one for under about 300ms. A flash of spinner reads as a glitch.

## Not yet tokenised

Stroke widths (2, 2.5) and the one-second duration.
