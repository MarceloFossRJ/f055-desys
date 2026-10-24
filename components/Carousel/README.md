# Carousel

A horizontal run of slides with edge controls and a dot index.

## Provenance

**Derived.** The reference has no carousel. Its idiom for a set of comparable
things is a **grid of cards** — savings targets, holdings, contributors are all
laid out, not paged.

Read that as a hint: a carousel hides content behind an interaction, and this
system's own instinct is to show it. Use one when the set is genuinely long and
secondary, not to tidy up four cards.

## Anatomy

| Part | Token |
|---|---|
| Slide | `muted`, `radius-14`, `space-16` padding |
| Slide gap | `space-16` |
| Upcoming slide | `opacity: .5` |
| Nav button | 28×28, `radius-pill`, `card` fill, `shadow-overlay` |
| Nav offset | `space-8` outside the viewport edge |
| Dot | 6×6, `radius-full`, `track` |
| Active dot | `foreground` |
| Dot gap | `space-6` |

## The nav buttons float, so they take `overlay`

A control sitting on top of content is a floating element, which in this system
means `shadow-overlay` — the same elevation as a Popover. `shadow-card` would
make them look pasted onto the slide rather than hovering over it.

They are `card`-filled, not `muted`, so they stay legible over a slide of any
fill.

## Dots are `track` and `foreground`, not `primary`

A dot index marks **where you are**, which this system paints `muted` or
`foreground` — never red. Same rule as Pagination and Nav. The inactive dots use
`track`, because an unfilled indicator is the same idea as an empty slider
groove.

A row of red dots would spend the system's one signal on a position indicator.

## Peek, don't crop

The next slide is partly visible at 50% opacity. That is what tells someone
there is more — more reliably than arrows, which people read as decoration.

Do not fade slides out to the container edge with a gradient mask: the reference
defines no gradients, and a hard edge with a peeking neighbour says the same
thing.

## Guidelines

Never auto-advance. The reference has no motion at all, and auto-advancing
carousels are read past, not read.

Dots work up to about six slides. Beyond that use a count ("3 of 24") or
reconsider whether this should be a list.

Make it work by scroll as well as by button — `scroll-snap-type: x mandatory`
on the viewport with `scroll-snap-align: start` on the slides. Touch users will
swipe regardless of whether you planned for it.

Each dot is a real button naming its slide. Arrows get `aria-label` and go
`disabled` at the ends rather than wrapping — wrapping loses people.

## Not yet tokenised

The peek opacity.
