# Card

The system's primary surface, and where its 20px spacing unit is most visible.

## Anatomy

| Part | Token |
|---|---|
| Fill | `card` |
| Text | `card-foreground` |
| Shape | `radius-xl` (24px) |
| Elevation | `shadow-card` |
| Vertical padding | `space-20` |
| Horizontal padding | `space-20`, applied per section |
| Gap between header, body and footer | `space-20` |
| Gap between a title and its subtitle | `space-6` |
| Gap between sections inside the body | `space-24` |

**The same 20px does three jobs** — the card's vertical padding, its horizontal
padding, and the gap between its parts. That single relationship is most of what
makes the reference's cards look consistent. If you change one thing about this
component, change that value and let everything follow.

## Why padding is applied per section, not on the card

The card sets `padding-block` only; each of header, body and footer sets its own
`padding-inline`. That lets a section bleed to the card's edges — a table, an
image, a full-width divider — without fighting the container. The reference uses
this on every card that contains a table.

## Elevation

`shadow-card` is a 1px hairline ring plus two very soft drops. The ring is doing
nearly all the work; the drops are almost invisible and exist to keep the card
from looking pasted on.

It is the one elevation that changes between themes — the ring flips from
near-black at 5% to near-white at 10%, because a dark surface needs a light edge
to read as raised. On web that is automatic.

Do not add a `border` as well. The ring is already there, and doubling them
produces a visible 2px edge.

## Inner surfaces

A tile inside a card — a stat block, an icon square, a nested row — uses `muted`
with `radius-lg` (10px), not another `card` at `radius-xl`. Nesting the card
treatment makes the hierarchy ambiguous.

## Guidelines

One `heading` or `card-title` per card. Footer actions align right, with the
primary action last. Use 28px buttons in a card footer; 32px is for standalone
contexts.

## Not yet tokenised

Button heights, and the 1px hairline that `shadow-card` draws.
