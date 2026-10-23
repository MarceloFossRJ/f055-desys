# Table

Rows separated by hairlines, with figures on tabular numerals so columns align.

## Anatomy

| Part | Token |
|---|---|
| Cell padding | `space-8` |
| Header row height | 40px |
| Row separator | 1px `border` |
| Header text | type style `text` at weight 500 |
| Cell text | type style `text` |
| Figures | `font-variant-numeric: tabular-nums` |

No zebra striping, no row fill, no outer border. Separation comes from the
hairline alone — consistent with how the rest of the system treats edges.

## Tabular numerals are not optional

Every numeric cell sets `tabular-nums`. Without it, proportional digits make
columns of currency visibly ragged, which is the single most common way a table
built from this system looks wrong. The `numeric` type style carries this
already if you are using the mono face; for sans figures set the property
directly, as the reference does.

Numeric columns are right-aligned, including their headers.

## Full-bleed inside a card

A table usually sits in a card whose body has `space-20` horizontal padding. The
reference keeps that padding, so cell content aligns with the card's other
sections. If you want the hairlines to run edge to edge instead, drop the
padding on that one section only — the card applies padding per section
precisely to allow this.

## The last row

Drop the separator on the final row (`tbody tr:last-child td { border-bottom: 0 }`).
A trailing hairline just above the card's own edge reads as a mistake.

For a totals row, weight 500 is enough. Do not add a fill or a heavier rule.

## Guidelines

Tables do not scroll horizontally in this system — at narrow widths, switch to a
stacked list of label/value rows instead. The reference uses that pattern for
its transaction lists.

## Not yet tokenised

The 40px header height and the 1px separator width.
