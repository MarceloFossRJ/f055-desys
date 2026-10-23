# Calendar

A month grid whose day cells are circles, selected in `primary`.

## Anatomy

| Part | Token |
|---|---|
| Header height | 40px |
| Month label | type style `button` (14 / 20 / 500) |
| Nav buttons | 24×24 at `radius-14` |
| Weekday row | `caption` in `muted-foreground` |
| Day cell | square, `radius-pill`, 40px minimum |
| Row gap | `space-8` |
| Day number | 14px at `line-height: 1` |
| Current-month day | `foreground` |
| Adjacent-month day | `muted-foreground` |
| Selected day | `primary` / `primary-foreground` |

## The cells are square, so pill makes them circles

Each day cell is `aspect-ratio: 1 / 1` at a 40px minimum with `radius-pill`.
Because 18px exceeds half of 40px... it does not — so the browser does *not*
clamp here, and a 40px cell at 18px radius would be a rounded square. The
reference sets the cells to a minimum of 40px wide but lets them grow with the
container, and at the width it actually renders they are circles.

**If your calendar is narrower than ~36px per cell, switch to `radius-full`**
so the selected day stays a circle rather than drifting into a squircle. This is
the one place in the system where `pill` does not reliably produce a pill.

## Line height 1 on the numbers

Day numbers set `line-height: 1`, not the `text` style's 20px. With a normal
line height the digit does not sit on the optical centre of the circle. Keep it.

## What the reference does and does not show

**Extracted:** the grid, cell geometry, both day colours, the selected state,
header and weekday styling.

**Not in the reference, so decide per project:** today's marker (distinct from
selected), range selection, disabled days, multi-month layout, keyboard focus
movement.

One observed detail worth knowing: the selected cell's wrapper carries a `muted`
background with no radius, behind the circular `primary` fill. On a single
selected date that is invisible; it is the shape a **range** highlight would
take. If you build range selection, that wrapper is where it goes — square
fill in `muted` spanning the run, circles in `primary` at each end.

## Deviation from the reference

The weekday row is specified at **12px**, the `caption` step. The reference uses
**12.8px**, which is not on the type scale at all and looks like a 0.8 scale
factor rather than a decision. This is the only place I have knowingly departed
from the source; revert it if the designer confirms 12.8px was deliberate.

## Not yet tokenised

Header height (40), nav button size (24), icon size (16), minimum cell width (40).
