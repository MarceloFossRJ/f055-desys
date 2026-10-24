# Badge

A 20px pill carrying status, a count, or a short category label.

## Anatomy

| Part | Token |
|---|---|
| Height | 20px (not a token) |
| Shape | `radius-pill` |
| Horizontal padding | `space-8` |
| Gap to a leading dot or icon | `space-4` |
| Label | type style `badge` (12 / 16 / 500) |

Variants mirror Button: `primary`, `secondary`, `outline`, `destructive`.
`secondary` is the workhorse — most badges in the reference are neutral, with
colour reserved for the few that carry real state.

## Guidelines

A badge is **not** a button. It has no hover, no focus ring and no click target.
If it needs to be clickable, use a 20px Button instead and accept the small
target, or reconsider the interaction.

Use at most one coloured badge in a row. A list where every row carries a red
badge tells the reader nothing.

For a status dot, use a 6px circle at `radius-full` in a `chart-*` colour rather
than tinting the whole badge — it is quieter and keeps the label readable.

Numeric badges should use the `numeric` type style so digits align when badges
stack in a column.

## Not yet tokenised

Nothing — every dimension is a `--control-*` token.
