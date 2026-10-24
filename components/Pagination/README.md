# Pagination

Numbered pages as 32px pills. The current page is `muted`, not `primary`.

## Provenance

**Derived.** The reference contains no pagination — I checked the whole file for
it. What it *does* contain is the system's own idiom for long lists: a **View
All** link in a card header, and **+810 contributors** at the end of a list.
Both are load-more patterns, not numbered pages.

That is worth knowing before you reach for this component. The last block of the
preview shows the alternative, which is closer to what the reference actually
does.

## Anatomy

| Part | Token |
|---|---|
| Page button | 32px min-width, 32px height, `radius-pill` |
| Padding | `space-8` inline, so 3-digit pages still fit |
| Gap | `space-2` |
| Number | type style `text` with **tabular numerals** |
| Current page | `muted` fill, weight 500 |
| Disabled arrow | `muted-foreground` |
| Ellipsis | 32px wide, `muted-foreground`, not interactive |
| Arrows | 16×16 chevrons |

## Current page is `muted`, deliberately not `primary`

Calendar marks its selected day with `primary`, and the temptation is to do the
same here. Don't — they mean different things.

A selected calendar date is **a value the person chose**: data, which is what
red means in this system. A current page is **where the person is**: a location,
which Nav and Tabs both mark with a `muted` fill and a weight shift.

Pagination is navigation, so it follows Nav. Same 32px pill, same `muted`, same
400 → 500 weight change.

## Tabular numerals are not optional

Without them the row visibly reflows as you page from 9 to 10, and a column of
pills changes width. Same rule as Table.

The `min-width: 32px` with `space-8` padding is what lets a 3-digit page grow
without the single digits looking cramped.

## Guidelines

Show first, last, current and one neighbour either side; collapse the rest to an
ellipsis. The ellipsis is a `<span>`, not a button — if it is clickable, it is a
menu, which is a different component.

Previous and Next are icon-only and disabled at the ends — disabled, not hidden,
so the control does not change width at the boundaries.

For an infinite or very long list, prefer Load more with a count. Numbered pages
earn their place when people need to return to a specific page.

Mark the current page `aria-current="page"` and give every arrow an
`aria-label`.

## Not yet tokenised

Button size (32), arrow size (16), the Load more button's 28px height.
