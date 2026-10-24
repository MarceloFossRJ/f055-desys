# Placeholder

Two forms, both extracted: a **skeleton** for content with a shape, and an **empty state** for content that will not arrive on its own.

## Skeleton

| Part | Token |
|---|---|
| Bar fill | `muted` |
| Bar shape | `radius-pill` (`radius-full` for an avatar) |
| Title bar | 16px tall |
| Body bar | 12px tall |
| Button bar | 32 × 80 |
| Avatar bar | 40 × 40 |
| Gap between bars | `space-8` |
| Gap avatar → text | `space-12` |
| Gap between blocks | `space-16` |

**Widths are uneven on purpose** — 75%, 50%, 100%, 100%, 80% in the reference.
A stack of identical full-width bars reads as a chart, not as text.

### The reference implies a pulse

Its bars carry opacities of 0.892, 0.881, 0.869 and 0.857, descending down the
card. That is not four chosen values — it is one staggered pulse caught
mid-animation. Along with Spinner, it is the only motion the whole reference
implies.

So: a slow opacity pulse, roughly 1.6s, with a small stagger between rows, and
`prefers-reduced-motion` honoured by stopping at a flat 0.9.

### The skeleton must match what loads

Same number of lines, same rough widths, same button count. A skeleton that
does not match causes a visible jump when the real content lands, which is worse
than a spinner. If you cannot predict the shape, use a Spinner.

## Empty state

The reference uses one layout for every empty card — Distribute Track, No
codespaces, No Team Members, Explore Catalog, 404.

| Part | Token |
|---|---|
| Icon tile | 40 × 40 `muted` at `radius-14`, 16px icon, `space-8` below |
| Title | 18 / 28 / 500, letter-spacing **−0.45px**, `text-wrap: balance` |
| Description | 14 / 22.75 (`prose`) in `muted-foreground`, balanced |
| Action | 28px Button, `space-8` above |
| Gap | `space-8` |
| Max width | 384px |
| Alignment | centred |

The title is the one place in the system with **negative tracking**. At 18px
weight 500 centred, −0.45px tightens a short heading so it does not read as
spaced-out. Keep it; it is why these cards look composed rather than assembled.

`text-wrap: balance` on both title and description is also the reference's —
centred text that breaks unevenly is the main way this layout goes wrong.

## Which one

| Situation | Use |
|---|---|
| Content is loading and you know its shape | Skeleton |
| Content is loading and you do not | Spinner |
| There is nothing, and the person can change that | Empty state with an action |
| There is nothing, and they cannot | Empty state, no action |

An empty state without an action and without an explanation is a dead end —
say why it is empty.

## Guidelines

Mark skeletons `aria-hidden` and give the region `aria-busy="true"`. Announcing
bars is noise.

Never animate a skeleton into the real content. The swap should be instant; a
cross-fade draws attention to the moment of loading.

## Not yet tokenised

The 384px max width, the −0.45px tracking, and the pulse duration.
