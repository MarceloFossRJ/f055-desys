# Nav

A grouped list of destinations. The active item is a `muted` pill; everything else is bare.

## Anatomy

| Part | Token |
|---|---|
| Item height | 32px |
| Item padding | `space-8` block, `space-10` inline |
| Item shape | `radius-pill` |
| Icon-to-label gap | `space-8` |
| Icon | 16×16 in `currentColor` |
| Label | 14 / 20, weight **400** inactive, **500** active |
| Active fill | `muted` |
| Gap between items | `space-2` |
| Gap between groups | `space-16` |
| Group label | 12 / 16 / 500 in `muted-foreground`, inset by `space-10` |

## Weight carries the active state, not just colour

An inactive item is weight 400 on no background; the active item is weight 500
on `muted`. Both the fill and the weight change together. Using only the fill
leaves the active item feeling unemphasised at this size; using only the weight
makes it hard to spot while scanning.

The label colour does **not** change — both are `foreground`. Do not also
darken or tint the active label; three things shifting at once is heavier than
this system wants.

## The group label is inset, not flush

Group labels take the same `space-10` inline padding as the items, so the label
and the item text share a left edge. A flush-left label over inset items looks
like a mistake.

## Nav versus ListGroup versus Tabs

Three components here look similar and mean different things:

- **Nav** — destinations in a persistent sidebar. One active at a time, marked
  by a `muted` pill.
- **ListGroup** — rows that are each a destination or action, on their own
  `muted` pills with descriptions and chevrons. Used *inside* a page, not as the
  page's chrome.
- **Tabs** — switching between views of the same thing, in a `muted` track.

If the item needs a description, it is a ListGroup. If the options are views of
one page rather than separate pages, they are Tabs.

## Measured, and not

**Measured:** item height, padding, radius, icon size, both label weights, the
active fill, and the 2px gap between items (taken from the 34px pitch between
adjacent item baselines against a 32px item).

**Not measured:** the gap between groups and the space under a group label. The
Paper session hit its limit before I could read the list container, so
`space-16` and `space-4` are reasonable readings of the rendered design rather
than extracted values. Worth confirming.

## Two deviations from the reference

The reference sets the item radius to **19.6px**, which is not on the radius
scale — the same kind of off-scale artifact as the calendar's 12.8px weekday
text. At a 32px item height anything above 16px renders identically, so this
spec uses `radius-pill` (18px). No visual difference.

The active label is `#171717` in the reference where this spec uses `foreground`
(`#0A0A0A`) — one step apart and imperceptible, but recorded.

The group label is `foreground` at 70% in the reference; this spec uses
`muted-foreground`, which is slightly lighter. If group labels need to read
stronger, that is the value to revisit.

## Not yet tokenised

Item height (32), icon size (16).
