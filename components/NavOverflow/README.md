# NavOverflow

What a horizontal nav does when its items do not fit: the tail collapses into a **More** menu.

## Provenance

**Derived.** The reference contains no overflow control. It does contain the
closest precedent — the Breadcrumb's ellipsis button, which collapses the middle
of a trail — and this follows the same idea applied to the end of a nav.

Everything is assembled from extracted parts: Nav's item, Select's panel, and
the `overlay` elevation from the chart tooltip.

## Anatomy

| Part | Token |
|---|---|
| Trigger | Nav item geometry, plus a 16px chevron in `muted-foreground` |
| Chevron rotation | 180° when open |
| Panel | `popover`, `radius-14`, `shadow-overlay`, `space-6` padding |
| Panel offset | `space-4` |
| Menu item | 32px, `radius-pill`, `space-10` inline |
| Minimum panel width | 160px |

## It collapses the tail, breadcrumb collapses the middle

A breadcrumb hides the middle because its first and last items carry the most
meaning. A nav hides the **end**, because nav order is priority order — the
first items are the ones people use.

So: keep items from the left, collapse from the right, and never collapse the
active item. If the active item would fall into the overflow, promote it into
the visible set and collapse its neighbour instead. A nav whose current page is
hidden behind "More" has failed at its one job.

## The trigger says More, not ⋯

Breadcrumb's overflow is an icon because it sits between two labels and should
recede. A nav's overflow is a peer of the other items and gets a word.

It is also not a destination — it is a `<button>` with `aria-expanded`, while
its neighbours are links.

## Measuring

Collapse by measured width, not by a fixed item count: render the full set,
measure, then move items into the menu until the row fits. A breakpoint-based
rule breaks as soon as labels are translated — German nav labels are routinely
half again as long as English.

Panel items are full nav items, not a compressed list. They are the same
destinations.

## Guidelines

If more than about half the items end up in the menu, the nav is too long for a
bar — use Nav in a sidebar instead.

Do not animate the collapse. Items appearing and disappearing as the window
resizes is noise, and the reference defines no motion at all.

## Not yet tokenised

Minimum panel width (160).
