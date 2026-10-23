# MultiSelect

Several choices at once: chips in the trigger, checkboxes in the panel.

## Anatomy

**Trigger** — Select's trigger, but it grows:

| Part | Token |
|---|---|
| Fill | `input` |
| Shape | `radius-pill` |
| Height | `min-height: 32px`, grows as chips wrap |
| Padding | `space-4` block, `space-10` leading, `space-8` trailing |
| Chip gap | `space-4` |
| Chip | 20px pill in `secondary`, `badge` type style, 12px remove icon |
| Placeholder | `muted-foreground` |
| Chevron | 16×16 in `muted-foreground` |

**Panel** — Select's panel, with a checkbox per row:

| Part | Token |
|---|---|
| Fill | `popover`, `radius-14`, `shadow-overlay` |
| Option | 32px, `radius-pill`, `space-10` inline |
| Checkbox | 16×16 at `radius-5`, `primary` when checked |
| Checkbox-to-label gap | `space-10` |

## Why chips rather than "3 selected"

Chips show *what* is selected and let one be removed without opening the panel.
The cost is a trigger whose height changes, which shifts everything below it.
That is a real trade-off: in a dense form, or where more than about five values
are likely, a summary ("3 selected") in a fixed-height trigger is the better
choice. The system supports both; this spec documents the chip form because it
reuses existing parts exactly.

**`min-height`, never `height`.** A fixed height clips the second row of chips
with no warning.

## Why checkboxes and not the tick Select uses

Select marks its one choice with a tick in `accent`. MultiSelect uses real
checkboxes, because a tick reads as "this is the current value" while a checkbox
reads as "toggle this one". Do not use `accent` on selected rows here — with
several rows highlighted at once the panel becomes a block of colour and the
checkboxes stop being the thing you read.

## Guidelines

Chips are `secondary`, never `primary`. They are data, not actions — a row of
red chips would spend the system's one signal on a list of tags.

The remove icon is 12px inside a 20px chip, which is below any reasonable touch
target. On touch, drop the per-chip remove and rely on the panel.

Order chips by selection order, not alphabetically — it matches what the person
just did.

For more than ~10 options add a search field at the top of the panel, as Select
does.

## Provenance

**Derived in full.** The reference contains no multi-select, so nothing here is
extracted. Every part is assembled from components that *are* extracted — the
Input fill and shape, the Badge, the Toggle checkbox, and the overlay geometry
from the chart tooltip — but the composition is a decision, not a measurement.

Treat this spec as the most provisional of the ten. If a designer takes a view,
it should win.

## Not yet tokenised

Trigger min-height (32), chip height (20), remove icon (12), checkbox (16),
tick (14), option height (32).
