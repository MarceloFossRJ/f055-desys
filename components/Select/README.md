# Select

A single-choice control. The trigger is an Input; the panel is an overlay.

## Anatomy

**Trigger** — identical to Input, with a chevron:

| Part | Token |
|---|---|
| Fill | `input` |
| Shape | `radius-pill` |
| Height | 32px |
| Padding | `space-10` leading, `space-8` trailing |
| Value | type style `text`, truncated with an ellipsis |
| Placeholder | `muted-foreground` |
| Chevron | 16×16 in `muted-foreground`, rotates 180° when open |
| Elevation | `none` |
| Focus | `ring` + `ring-offset` |

**Panel**:

| Part | Token |
|---|---|
| Fill | `popover` / `popover-foreground` |
| Shape | `radius-14` |
| Elevation | `shadow-overlay` |
| Padding | `space-6` |
| Gap between options | `space-2` |
| Option height | 32px, `radius-pill`, `space-10` inline padding |
| Selected option | `accent` / `accent-foreground` + a 16px tick |
| Disabled option | `muted-foreground` |
| Separator | 1px `border` with `space-4` above and below |
| Offset from trigger | `space-4` |

## radius-14 and shadow-overlay, not radius-24 and shadow-card

This is the distinction that matters. A **card** is a surface on the page:
`radius-24`, `shadow-card`. An **overlay** floats above it: `radius-14`,
`shadow-overlay`. The reference's chart tooltip establishes this pairing, and
every dropdown, popover and menu should follow it. Using card geometry on a
dropdown makes a small panel look like a misplaced card.

## This is where `accent` earns its place

`accent` and `muted` resolve to the same value today, and until now nothing used
`accent`. The selected option is its proper job: a highlighted row on a neutral
surface. Use `accent` here, not `muted` — when the two eventually diverge, this
is one of the places that should move.

## Guidelines

The panel matches the trigger's width; options are left-aligned with the trigger
value, which is why both use `space-10` inline padding.

Options are pills, like everything else interactive. A full-width square
highlight would be foreign here.

Separators group options; they do not decorate. If a panel has one separator and
no grouping reason, remove it.

Beyond about ten options add a search field at the top of the panel — reuse
Input's trailing-icon form.

## What is extracted and what is not

**Extracted:** the entire trigger, measured from the reference's order-type and
currency selects. The panel's elevation and radius, from the chart tooltip.

**Derived:** the panel's internal layout — option height, padding, selected
state and separator. The reference never draws an open dropdown. These follow
the system's own rules rather than another library's, but they are untested.

## Not yet tokenised

Trigger and option heights (32), chevron and tick sizes (16), separator width.
