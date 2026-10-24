# Drawer

A panel anchored to an edge, for work too long for a Dialog. **Derived** — the
reference draws no drawer.

## Anatomy

| Part | Token |
|---|---|
| Scrim | `foreground` at 50% |
| Surface | `popover` / `popover-foreground` |
| Radius | `radius-24` on the **inner** corners only |
| Shadow | `shadow-overlay` |
| Width (side) | 384px, `max-width: 100%` |
| Height (bottom) | `max-height: 85vh` |
| Header | `space-20` / `space-20` / `space-16` |
| Body | `space-20` inline, scrolls |
| Footer | `space-16` / `space-20` / `space-20` |
| Field gap | `space-16` |

## Only the inner corners are rounded

A right-side drawer takes `border-radius: var(--radius-24) 0 0 var(--radius-24)`.
The edges flush against the viewport stay square — a rounded corner against the
screen edge leaves a sliver of page showing through, which reads as a rendering
fault rather than a design.

## Three regions, and only the middle scrolls

Header and footer are fixed; the body takes `flex: 1; min-height: 0; overflow: auto`.
The `min-height: 0` is not optional — without it a flex child refuses to shrink
below its content and the whole panel scrolls, taking the footer actions off
screen. That is the single most common way this component breaks.

A footer that scrolls away in a long form is a form people cannot submit.

The footer carries a 1px `border` hairline on top. That is a **scroll edge**,
not a row separator — without it, content scrolling under the footer is clipped
mid-glyph against nothing and reads as a rendering fault. It does not make the
panel a Table.

## Edges

| Edge | Use |
|---|---|
| Right | The default. Detail, a multi-step form, filters |
| Bottom | Mobile. Below ~640px, a right drawer should become a bottom sheet |
| Left | Navigation only, and only when a NavBar already lives on the left |

Do not mix edges in one product for the same kind of content.

## Dialog or Drawer

| Situation | Use |
|---|---|
| One decision, a sentence of context | Dialog |
| 1–4 fields | Dialog |
| 5+ fields, or steps | Drawer |
| Content of unknown length | Drawer |
| Reading a record while keeping the list in view | Drawer |
| Something destructive | Dialog — it should interrupt |

A Drawer keeps the page visible at the edge, which is its advantage and its
limit: it is for continuing work, not for stopping it.

## Modal semantics

Same contract as Dialog: `role="dialog"`, `aria-modal="true"`,
`aria-labelledby`, focus into the panel on open, focus trapped, `Esc` to close
(unless there is unsaved input), focus restored to the trigger, background
`inert`, body `overflow: hidden`.

A non-modal variant — a filter panel that leaves the page usable — is a
different component. Do not get there by dropping `aria-modal` from this one:
it also needs no scrim, no focus trap, and it must not block the page.

## Steps

Put progress in the header as `space-2` under the title — "Step 2 of 3 —
Metadata", 14 / 22.75 in `muted-foreground`. The system has no stepper
component; a sentence does the job and never gets cramped.

## Not yet tokenised

Width (384), the 85vh bottom-sheet cap, the 640px breakpoint, the 50% scrim.
